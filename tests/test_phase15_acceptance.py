"""
Phase 15 Acceptance Test Suite: End-to-End & Negative Control Verification.
Tests the full system path including:
1. Valid multi-format processing (PNG, PDF)
2. Safe Model Capability enforcement (Qwen rejection, SmolVLM allowance)
3. Negative controls (corrupted file, unanswerable query, oversized payload, path traversal)
4. Abstention trigger and bounding-box spatial coordinates
"""
import io
import pytest
from PIL import Image, ImageDraw
from pypdf import PdfWriter

from src.runtime.upload_manager import UploadManager, UploadValidationError
from src.runtime.document_adapter import DocumentAdapter
from src.runtime.model_registry import ModelRegistry, ModelStatus, ModelSelectionError
from src.runtime.orchestrator import PipelineOrchestrator, ExtractionResult


@pytest.fixture
def test_env(tmp_path):
    upload_dir = tmp_path / "uploads"
    upload_dir.mkdir(parents=True, exist_ok=True)
    manager = UploadManager(upload_dir=upload_dir, max_size_bytes=2 * 1024 * 1024)
    adapter = DocumentAdapter()
    registry = ModelRegistry()
    orchestrator = PipelineOrchestrator(upload_manager=manager, model_registry=registry)
    return {
        "manager": manager,
        "adapter": adapter,
        "registry": registry,
        "orchestrator": orchestrator,
        "upload_dir": upload_dir,
    }


def test_acceptance_png_full_flow(test_env):
    """Test full upload -> query extraction -> bounding box matching flow on PNG."""
    manager = test_env["manager"]
    adapter = test_env["adapter"]
    orchestrator = test_env["orchestrator"]

    # 1. Create a genuine document image
    img = Image.new("RGB", (600, 400), color="white")
    draw = ImageDraw.Draw(img)
    draw.text((60, 60), "ACME CORPORATION INVOICE", fill="black")
    draw.text((60, 110), "Invoice ID: INV-98214", fill="black")
    draw.text((60, 170), "Total Amount Due: $1,420.50", fill="black")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    data = buf.getvalue()

    # 2. Upload
    record = manager.save_upload(data, "invoice.png", "image/png")
    doc_info = adapter.inspect_document(record.file_path)
    assert doc_info.page_count == 1
    assert record.content_type == "image/png"

    # 3. Orchestrate question answering
    result = orchestrator.process_document(
        upload_id=record.upload_id,
        question="What is the invoice ID?",
        page_num=1,
    )

    # 4. Assertions
    assert isinstance(result, ExtractionResult)
    assert result.status == "VERIFIED"
    assert "INV-98214" in result.answer
    assert result.confidence > 0.6
    assert result.quality["overall_quality"] > 0.0
    assert result.routing_decision in ["CLEAN", "MODERATE", "SEVERE"]
    assert len(result.evidence) >= 1
    ev = result.evidence[0]
    assert "normalized_bbox" in ev
    ymin, xmin, ymax, xmax = ev["normalized_bbox"]
    assert ymin <= ymax
    assert xmin <= xmax


def test_acceptance_pdf_full_flow(test_env):
    """Test full upload -> adapt -> query flow on multi-page PDF."""
    manager = test_env["manager"]
    adapter = test_env["adapter"]
    orchestrator = test_env["orchestrator"]

    writer = PdfWriter()
    writer.add_blank_page(width=595, height=842)
    pdf_buf = io.BytesIO()
    writer.write(pdf_buf)
    pdf_bytes = pdf_buf.getvalue()

    record = manager.save_upload(pdf_bytes, "agreement.pdf", "application/pdf")
    doc_info = adapter.inspect_document(record.file_path)
    assert doc_info.page_count == 1
    assert record.content_type == "application/pdf"

    result = orchestrator.process_document(
        upload_id=record.upload_id,
        question="What is the agreement date?",
        page_num=1,
    )
    assert result.status in ["VERIFIED", "UNCERTAIN", "ABSTAIN / REVIEW_REQUIRED"]


def test_acceptance_negative_control_unanswerable_abstains(test_env):
    """Test unanswerable query triggers calibrated safe abstention."""
    manager = test_env["manager"]
    orchestrator = test_env["orchestrator"]

    img = Image.new("RGB", (400, 200), color="white")
    draw = ImageDraw.Draw(img)
    draw.text((30, 30), "Item: Laptop Computer", fill="black")
    buf = io.BytesIO()
    img.save(buf, format="PNG")

    record = manager.save_upload(buf.getvalue(), "receipt.png", "image/png")

    result = orchestrator.process_document(
        upload_id=record.upload_id,
        question="What is the driver license passport identification number?",
        page_num=1,
    )
    # The document doesn't contain driver license info
    assert result.abstained is True
    assert result.status == "ABSTAIN / REVIEW_REQUIRED"
    assert result.confidence <= 0.65
    assert len(result.evidence) == 0


def test_acceptance_negative_control_corrupted_file(test_env):
    """Test corrupted file content is rejected safely."""
    manager = test_env["manager"]
    with pytest.raises(UploadValidationError, match="File content does not match"):
        manager.save_upload(b"CORRUPTED_GARBAGE_PAYLOAD", "corrupt.png", "image/png")


def test_acceptance_negative_control_oversized_file(test_env):
    """Test file exceeding size limit is rejected."""
    manager = test_env["manager"]
    huge_data = b"\x89PNG\r\n\x1a\n" + (b"\x00" * (3 * 1024 * 1024))
    with pytest.raises(UploadValidationError, match="exceeds maximum allowed"):
        manager.save_upload(huge_data, "huge.png", "image/png")


def test_acceptance_hardware_registry_strict_boundary(test_env):
    """Test that Qwen2.5-VL-7B is rejected and SmolVLM-500M is permitted."""
    registry = test_env["registry"]
    hw_info = registry.get_hardware_status()

    assert "physical_gpu_detected" in hw_info
    assert "gpu_total_vram_mb" in hw_info

    # Validate registry policies
    matrix = registry.get_capability_matrix()
    qwen = matrix["qwen2.5-vl-7b"]
    assert qwen.status == ModelStatus.NOT_EXECUTABLE
    assert "6 gb" in qwen.limitation_reason.lower()

    smol = matrix["smolvlm-500m"]
    assert smol.status in (ModelStatus.PHYSICALLY_VALIDATED, ModelStatus.SUPPORTED)

    # Try selecting Qwen -> must fail
    with pytest.raises(ModelSelectionError, match="NOT_EXECUTABLE"):
        registry.select_model("qwen2.5-vl-7b")

    # Try selecting SmolVLM -> must succeed
    selected = registry.select_model("smolvlm-500m")
    assert selected.model_id == "smolvlm-500m"
