"""Traceable Image Preprocessor for Vision-Language Inference."""

from typing import Tuple, Dict, Any, Optional
from PIL import Image
from pydantic import BaseModel


class ImageTransformationRecord(BaseModel):
    """Explicit audit record of all spatial and format transformations applied to an image."""
    original_width: int
    original_height: int
    processed_width: int
    processed_height: int
    resize_factor: float
    cropped: bool
    crop_box: Optional[Tuple[int, int, int, int]] = None
    color_mode: str
    format: str


class VLMImageProcessor:
    """Preprocesses document images while preserving complete provenance."""

    def __init__(self, min_pixels: int = 3136, max_pixels: int = 12845056):
        self.min_pixels = min_pixels
        self.max_pixels = max_pixels

    def process(
        self,
        image: Image.Image,
        target_max_dim: Optional[int] = None
    ) -> Tuple[Image.Image, ImageTransformationRecord]:
        """
        Validate, format, and optionally scale image while recording transformation metrics.
        No silent modifications: RGB conversion and any scaling are explicitly recorded.
        """
        orig_w, orig_h = image.size
        curr_img = image.convert("RGB")
        color_mode = "RGB"

        resize_factor = 1.0
        if target_max_dim and max(orig_w, orig_h) > target_max_dim:
            resize_factor = target_max_dim / float(max(orig_w, orig_h))
            new_w = max(1, int(round(orig_w * resize_factor)))
            new_h = max(1, int(round(orig_h * resize_factor)))
            curr_img = curr_img.resize((new_w, new_h), resample=Image.Resampling.LANCZOS)
        else:
            new_w, new_h = orig_w, orig_h

        record = ImageTransformationRecord(
            original_width=orig_w,
            original_height=orig_h,
            processed_width=new_w,
            processed_height=new_h,
            resize_factor=round(resize_factor, 6),
            cropped=False,
            crop_box=None,
            color_mode=color_mode,
            format=image.format or "PNG"
        )
        return curr_img, record
