"""Unit tests for Phase 3 Image Preprocessing."""

import numpy as np
from PIL import Image
import pytest

from src.quality.preprocessing import preprocess_image_input


def test_preprocessing_pil_rgb():
    img = Image.new("RGB", (300, 200), color=(255, 255, 255))
    prep = preprocess_image_input(img)
    assert prep.width == 300
    assert prep.height == 200
    assert prep.rgb.shape == (200, 300, 3)
    assert prep.gray.shape == (200, 300)
    assert prep.source_format == "PIL"


def test_preprocessing_rgba_compositing():
    # RGBA with transparent background
    img = Image.new("RGBA", (100, 100), color=(0, 0, 0, 0))
    prep = preprocess_image_input(img)
    # Transparent background should be composited onto white (255)
    assert np.all(prep.rgb == 255)
    assert np.all(prep.gray == 255)


def test_preprocessing_grayscale_input():
    gray_np = np.zeros((150, 100), dtype=np.uint8)
    prep = preprocess_image_input(gray_np)
    assert prep.width == 100
    assert prep.height == 150
    assert prep.rgb.shape == (150, 100, 3)
    assert prep.gray.shape == (150, 100)


def test_preprocessing_max_dimension():
    img = Image.new("RGB", (4000, 2000), color=(255, 255, 255))
    prep = preprocess_image_input(img, max_dimension=1000)
    assert max(prep.width, prep.height) == 1000
    assert prep.width == 1000
    assert prep.height == 500


def test_preprocessing_invalid_inputs():
    with pytest.raises(ValueError):
        preprocess_image_input(np.array([]))

    with pytest.raises(FileNotFoundError):
        preprocess_image_input("non_existent_file_path_12345.png")

    with pytest.raises(TypeError):
        preprocess_image_input(12345)  # type: ignore
