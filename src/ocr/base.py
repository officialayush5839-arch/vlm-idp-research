"""Base OCR Engine Abstract Interface."""

from abc import ABC, abstractmethod
from PIL import Image

from src.ocr.schema import OCRResult


class OCRBackend(ABC):
    """Abstract Base Class for Document OCR Engines."""

    def __init__(self, config: dict):
        self.config = config

    @property
    @abstractmethod
    def engine_name(self) -> str:
        """Name of the OCR engine."""
        pass

    @property
    @abstractmethod
    def engine_version(self) -> str:
        """Version of the OCR engine."""
        pass

    @abstractmethod
    def extract(
        self,
        image: Image.Image,
        page_idx: int = 0,
        document_id: str = "doc_unknown"
    ) -> OCRResult:
        """Extract text and bounding boxes from an in-memory page image."""
        pass
