"""Image Preprocessing for Unlimited-OCR."""

from typing import Tuple, Optional
from PIL import Image
from src.vlm.processor import VLMImageProcessor, ImageTransformationRecord


class UnlimitedOCRImageProcessor:
    """Preprocesses input document images while recording complete transformation audit records."""

    def __init__(self, max_pixels: int = 16777216):
        self.processor = VLMImageProcessor(max_pixels=max_pixels)

    def process(
        self,
        image: Image.Image,
        target_max_dim: Optional[int] = None
    ) -> Tuple[Image.Image, ImageTransformationRecord]:
        """Converts to RGB and performs traceable scaling if requested."""
        return self.processor.process(image, target_max_dim=target_max_dim)
