"""Tests for Phase 15 Pipeline Orchestrator & Evidence Grounding."""

import pytest
from pathlib import Path
from PIL import Image, ImageDraw
from src.runtime.upload_manager import UploadManager
from src.runtime.orchestrator import PipelineOrchestrator, ExtractionResult

@pytest.fixture
def orchestrator(tmp_path):
    upload_mgr = UploadManager(upload_dir=tmp_path / "uploads")
    return PipelineOrchestrator(upload_manager=upload_mgr)

@pytest.fixture
def clean_invoice_upload(tmp_path, orchestrator):
    # Create an image invoice
    img_path = tmp_path / "invoice.png"
    img = Image.new("RGB", (800, 1000), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw.text((60, 60), "ACME CORPORATION INVOICE", fill=(0, 0, 0))
    draw.text((60, 120), "Invoice ID: INV-98214", fill=(0, 0, 0))
    draw.text((60, 180), "Total Amount Due: $1,420.50", fill=(0, 0, 0))
    draw.text((60, 240), "Due Date: 2026-11-15", fill=(0, 0, 0))
    img.save(img_path)

    record = orchestrator.upload_manager.save_upload(
        img_path.read_bytes(), "invoice.png", "image/png"
    )
    return record

def test_clean_document_extraction(orchestrator, clean_invoice_upload):
    result = orchestrator.process_document(
        upload_id=clean_invoice_upload.upload_id,
        question="What is the total amount due?",
        page_num=1
    )
    assert isinstance(result, ExtractionResult)
    assert result.status == "VERIFIED"
    assert result.abstained is False
    assert "$1,420.50" in result.answer
    assert result.confidence >= 0.70
    assert result.routing_decision in ("CLEAN", "MODERATE")
    assert len(result.evidence) > 0
    
    # Check evidence coordinates are valid normalized floats
    ev = result.evidence[0]
    assert 0.0 <= ev["normalized_bbox"][0] <= 1.0
    assert 0.0 <= ev["normalized_bbox"][1] <= 1.0
    assert ev["page"] == 1
    assert "Total Amount Due" in ev["text"] or "$1,420.50" in ev["text"]

def test_unanswerable_question_abstains(orchestrator, clean_invoice_upload):
    # Query for something completely absent from document
    result = orchestrator.process_document(
        upload_id=clean_invoice_upload.upload_id,
        question="What is the driver license passport number of the pilot?",
        page_num=1
    )
    assert result.abstained is True
    assert result.status == "ABSTAIN / REVIEW_REQUIRED"
    assert "ABSTAIN" in result.answer
    # No fake bounding box when evidence is absent
    assert len(result.evidence) == 0

def test_quality_and_routing_reported(orchestrator, clean_invoice_upload):
    result = orchestrator.process_document(
        upload_id=clean_invoice_upload.upload_id,
        question="What is the invoice ID?",
        page_num=1
    )
    assert "overall_quality" in result.quality
    assert "blur" in result.quality
    assert result.timing["total_ms"] > 0
