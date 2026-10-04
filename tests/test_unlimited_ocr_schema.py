"""Unit Tests for Unlimited-OCR Schemas."""

from src.baselines.unlimited_ocr.schemas import (
    UnlimitedOCRElement,
    UnlimitedOCRParsedOutput,
    UnlimitedOCRResult,
)


def test_unlimited_ocr_element_instantiation():
    """Verify UnlimitedOCRElement validates normalized coordinates."""
    elem = UnlimitedOCRElement(
        element_id="el_001",
        element_type="title",
        text="INVOICE 123",
        normalized_bbox=[50, 60, 400, 120],
        raw_bbox=[100, 120, 800, 240],
        confidence=1.0
    )
    assert elem.element_type == "title"
    assert elem.normalized_bbox == [50, 60, 400, 120]
    assert elem.raw_bbox == [100, 120, 800, 240]


def test_unlimited_ocr_result_raw_immutability():
    """Verify UnlimitedOCRResult stores raw_output separately from normalized_text."""
    res = UnlimitedOCRResult(
        baseline_id="B0-U",
        engine="Unlimited-OCR",
        model_revision="4f9b8c2e1d7a6053b8921e4c70d45f3a9e218c9b",
        document_id="doc_test_u",
        page_id="page_0",
        raw_output="title [10, 10, 100, 50]Header\ntext [10, 60, 200, 90]Body",
        normalized_text="Header\nBody",
        structured_elements=[{"type": "title", "text": "Header"}],
        bounding_boxes=[[10, 10, 100, 50]],
        confidence=1.0,
        spatial_evidence_status="SUPPORTED",
        latency_ms=25.4,
        gpu_peak_memory_mb=None,
        status="SUCCESS"
    )
    assert res.baseline_id == "B0-U"
    assert "title [" in res.raw_output
    assert "title [" not in res.normalized_text
    assert res.spatial_evidence_status == "SUPPORTED"
