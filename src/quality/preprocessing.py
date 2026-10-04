"""
Non-destructive image preprocessing for document quality feature extraction.
Handles format normalization, alpha channel compositing, and multi-color-space views.
"""

from __future__ import annotations

import io
from pathlib import Path
from typing import Optional, Tuple, Union
import cv2
import numpy as np
from PIL import Image

from src.core.logging import get_logger

logger = get_logger(__name__)


class PreprocessedPage:
    """Immutable preprocessed page container providing multiple color-space representations."""

    def __init__(
        self,
        rgb: np.ndarray,
        gray: np.ndarray,
        width: int,
        height: int,
        source_format: str = "PIL",
    ):
        self.rgb = rgb
        self.gray = gray
        self.width = width
        self.height = height
        self.source_format = source_format

    @property
    def shape(self) -> Tuple[int, int]:
        return (self.height, self.width)


def preprocess_image_input(
    image_input: Union[Image.Image, np.ndarray, str, Path],
    max_dimension: Optional[int] = None,
) -> PreprocessedPage:
    """
    Standardize any input image into clean RGB and Grayscale representations.
    Non-destructive: original source image is never mutated.

    Args:
        image_input: PIL Image, numpy array, or file path
        max_dimension: Optional maximum edge length for downsampling during analysis

    Returns:
        PreprocessedPage object
    """
    source_format = "unknown"

    if isinstance(image_input, (str, Path)):
        path = Path(image_input)
        if not path.is_file():
            raise FileNotFoundError(f"Image file does not exist: {path.resolve()}")
        pil_img = Image.open(path)
        source_format = pil_img.format or "FILE"
    elif isinstance(image_input, Image.Image):
        pil_img = image_input
        source_format = "PIL"
    elif isinstance(image_input, np.ndarray):
        # Convert numpy array to PIL
        if image_input.size == 0:
            raise ValueError("Input numpy image array is empty.")
        if image_input.ndim == 2:
            pil_img = Image.fromarray(image_input, mode="L")
        elif image_input.ndim == 3 and image_input.shape[2] == 3:
            pil_img = Image.fromarray(image_input, mode="RGB")
        elif image_input.ndim == 3 and image_input.shape[2] == 4:
            pil_img = Image.fromarray(image_input, mode="RGBA")
        else:
            raise ValueError(f"Unsupported numpy image shape: {image_input.shape}")
        source_format = "NUMPY"
    else:
        raise TypeError(f"Unsupported image input type: {type(image_input)}")

    # Check for empty / zero dimension images
    if pil_img.width <= 0 or pil_img.height <= 0:
        raise ValueError(f"Invalid image dimensions: {pil_img.width}x{pil_img.height}")

    # Handle Alpha channel by compositing onto a crisp white document background
    if pil_img.mode in ("RGBA", "LA") or (pil_img.mode == "P" and "transparency" in pil_img.info):
        rgba_img = pil_img.convert("RGBA")
        white_bg = Image.new("RGBA", rgba_img.size, (255, 255, 255, 255))
        composite = Image.alpha_composite(white_bg, rgba_img)
        rgb_pil = composite.convert("RGB")
    else:
        rgb_pil = pil_img.convert("RGB")

    width, height = rgb_pil.size

    # Optional resize for extreme images to keep latency strictly bounded
    if max_dimension and max(width, height) > max_dimension:
        scale = max_dimension / max(width, height)
        new_w, new_h = int(width * scale), int(height * scale)
        rgb_pil = rgb_pil.resize((new_w, new_h), Image.Resampling.LANCZOS)
        width, height = new_w, new_h

    rgb_array = np.array(rgb_pil, dtype=np.uint8)
    gray_array = cv2.cvtColor(rgb_array, cv2.COLOR_RGB2GRAY)

    return PreprocessedPage(
        rgb=rgb_array,
        gray=gray_array,
        width=width,
        height=height,
        source_format=source_format,
    )
