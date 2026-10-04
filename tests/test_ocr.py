"""Unit Tests for OCR Backends and Normalization."""

import pytest
from PIL import Image
from src.ocr.schema import OCRResult, OCRLine, OCRWord
from src.ocr.paddle import PaddleOCRBackend
from src.ocr.tesseract import TesseractBackend


def test_ocr_schema_instantiation():
    """Verify OCR models can be populated and validated."""
    word = OCRWord(
        word_id="w1",
        text="Invoice",
        confidence=0.98,
        raw_bbox=[10, 20, 100, 50],
        normalized_bbox=[10, 20, 100, 50]
    )
    line = OCRLine(
        line_id="l1",
        text="Invoice #1234",
        confidence=0.95,
        raw_bbox=[10, 20, 200, 50],
        normalized_bbox=[10, 20, 200, 50],
        words=[word]
    )
    res = OCRResult(
        document_id="doc_test_123",
        page_idx=0,
        full_text="Invoice #1234",
        confidence=0.95,
        lines=[line],
        engine="paddleocr",
        engine_version="2.8.1",
        latency_ms=12.5
    )
    assert res.document_id == "doc_test_123"
    assert len(res.lines) == 1
    assert res.lines[0].words[0].text == "Invoice"
    assert res.latency_ms == 12.5


def test_paddle_ocr_fallback_on_clean_image():
    """Verify PaddleOCR backend handles image extraction gracefully."""
    img = Image.new("RGB", (400, 400), color=(255, 255, 255))
    backend = PaddleOCRBackend()
    res = backend.extract(img, page_idx=0, document_id="doc_mock")

    assert res.engine == "paddleocr"
    assert res.document_id == "doc_mock"
    assert res.latency_ms is not None
    assert res.latency_ms >= 0.0


def test_tesseract_ocr_fallback_on_clean_image():
    """Verify Tesseract backend handles image extraction gracefully."""
    img = Image.new("RGB", (300, 300), color=(255, 255, 255))
    backend = TesseractBackend()
    res = backend.extract(img, page_idx=1, document_id="doc_tess")

    assert res.engine == "tesseract"
    assert res.document_id == "doc_tess"
    assert res.page_idx == 1
    assert res.latency_ms is not None
