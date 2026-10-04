"""Unit Tests for Unlimited-OCR Spatial Grounding and Coordinate Validation."""

from src.baselines.unlimited_ocr.parser import UnlimitedOCRParser
from src.ingestion.coordinates import compute_iou


def test_parser_extracts_valid_grounding_tags():
    """Verify parser extracts elements, types, and coordinates in [0, 1000] space."""
    raw = (
        "title [50, 100, 450, 180]INVOICE SUMMARY\n"
        "text [50, 200, 300, 240]Total Due: $500\n"
        "table [50, 300, 950, 700]| Item | Price |"
    )
    parser = UnlimitedOCRParser()
    out = parser.parse(raw, page_width=1000, page_height=1000)

    assert out.has_spatial_grounding is True
    assert len(out.elements) == 3
    assert out.detected_element_counts == {"title": 1, "text": 1, "table": 1}
    assert out.elements[0].normalized_bbox == [50, 100, 450, 180]
    assert out.elements[0].text == "INVOICE SUMMARY"
    assert "Total Due: $500" in out.full_transcription


def test_parser_rejects_out_of_bounds_and_inverted_coordinates():
    """Verify parser handles malformed or inverted coordinates gracefully."""
    # Out of bounds (>1000) and inverted (x1 > x2)
    raw = (
        "text [1200, 50, 1400, 80]Out of bounds text\n"
        "text [300, 50, 100, 80]Inverted coordinates text\n"
        "text [10, 20, 150, 40]Valid bounding box"
    )
    parser = UnlimitedOCRParser()
    out = parser.parse(raw)

    assert len(out.elements) == 1
    assert out.elements[0].normalized_bbox == [10, 20, 150, 40]
    # Text is still retained in transcription
    assert "Out of bounds text" in out.full_transcription
    assert "Inverted coordinates text" in out.full_transcription


def test_parser_handles_pure_markdown_without_grounding():
    """Verify parser flags absence of spatial grounding when only text is emitted."""
    raw = "# Invoice\nTotal: $1,200\nThank you for your business."
    parser = UnlimitedOCRParser()
    out = parser.parse(raw)

    assert out.has_spatial_grounding is False
    assert len(out.elements) == 0
    assert out.full_transcription == raw


def test_grounding_iou_calculation():
    """Verify IoU calculation on extracted Unlimited-OCR boxes against ground truth."""
    pred_box = [100, 100, 300, 300]
    gt_box = [100, 100, 300, 300]
    iou = compute_iou(pred_box, gt_box)
    assert iou == 1.0

    gt_half = [100, 100, 300, 500]
    iou_half = compute_iou(pred_box, gt_half)
    assert 0.4 < iou_half < 0.6
