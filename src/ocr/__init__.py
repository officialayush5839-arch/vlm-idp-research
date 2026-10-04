"""OCR Module Exports."""

from src.ocr.schema import OCRResult, OCRLine, OCRWord
from src.ocr.base import OCRBackend
from src.ocr.paddle import PaddleOCRBackend
from src.ocr.tesseract import TesseractBackend

__all__ = [
    "OCRResult",
    "OCRLine",
    "OCRWord",
    "OCRBackend",
    "PaddleOCRBackend",
    "TesseractBackend",
]
