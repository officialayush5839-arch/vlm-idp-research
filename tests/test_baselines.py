"""Unit Tests for B0, B1, and B2 Baseline Pipelines."""

from PIL import Image
from src.baselines.base import BaselineSample
from src.baselines.b0_ocr import B0OCRBaseline
from src.baselines.b1_ocr_vlm import B1OCRVLMBaseline
from src.baselines.b2_vlm import B2VLMBaseline
from src.vlm.loader import VLMLoader
from src.vlm.inference import VLMInferenceEngine
from src.ocr.paddle import PaddleOCRBackend


def test_b0_ocr_baseline_execution():
    """Verify B0 baseline runs end-to-end on synthetic sample."""
    img = Image.new("RGB", (400, 300), color=(255, 255, 255))
    sample = BaselineSample(
        sample_id="q001",
        document_id="doc_test_b0",
        page_idx=0,
        image=img,
        question="What is the total amount?",
        ground_truth_answers=["$500"]
    )
    b0 = B0OCRBaseline()
    result = b0.run(sample, run_id="run_smoke_001", seed=42)

    assert result.baseline == "B0"
    assert result.document_id == "doc_test_b0"
    assert result.status == "SUCCESS"
    assert result.latency_ms is not None


def test_b1_ocr_vlm_baseline_execution():
    """Verify B1 baseline runs end-to-end with mock VLM engine."""
    loader = VLMLoader()
    model, processor, metadata = loader.load_model_and_processor(mock_mode=True)
    engine = VLMInferenceEngine(model, processor, metadata, device="cpu", mock_mode=True)

    b1 = B1OCRVLMBaseline(vlm_engine=engine)
    img = Image.new("RGB", (500, 500), color=(240, 240, 240))
    sample = BaselineSample(
        sample_id="q002",
        document_id="doc_test_b1",
        page_idx=0,
        image=img,
        question="What is the vendor name?",
        ground_truth_answers=["Acme Corp"]
    )
    result = b1.run(sample, run_id="run_smoke_002", seed=42)

    assert result.baseline == "B1"
    assert result.document_id == "doc_test_b1"
    assert result.status == "SUCCESS"
    assert result.prompt_version == "v1.0-b1"
    assert result.prompt_hash is not None
    assert result.latency_ms is not None


def test_b2_vlm_baseline_execution():
    """Verify B2 baseline runs end-to-end with mock VLM engine."""
    loader = VLMLoader()
    model, processor, metadata = loader.load_model_and_processor(mock_mode=True)
    engine = VLMInferenceEngine(model, processor, metadata, device="cpu", mock_mode=True)

    b2 = B2VLMBaseline(vlm_engine=engine)
    img = Image.new("RGB", (500, 500), color=(240, 240, 240))
    sample = BaselineSample(
        sample_id="q003",
        document_id="doc_test_b2",
        page_idx=0,
        image=img,
        question="What is the invoice number?",
        ground_truth_answers=["INV-990"]
    )
    result = b2.run(sample, run_id="run_smoke_003", seed=42)

    assert result.baseline == "B2"
    assert result.document_id == "doc_test_b2"
    assert result.status == "SUCCESS"
    assert result.prompt_version == "v1.0-b2"
    assert result.prompt_hash is not None
    assert result.latency_ms is not None
