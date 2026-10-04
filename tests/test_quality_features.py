"""Unit tests for individual Phase 3 visual feature extractors."""

import numpy as np
import pytest

from src.quality.blur import measure_blur
from src.quality.compression import measure_compression
from src.quality.contrast import measure_contrast
from src.quality.glare import measure_glare
from src.quality.illumination import measure_illumination
from src.quality.noise import measure_noise
from src.quality.occlusion import measure_occlusion
from src.quality.perspective import measure_perspective
from src.quality.resolution import measure_resolution
from src.quality.schema import FeatureStatus
from src.quality.skew import measure_skew
from src.quality.synthetic import create_clean_document_fixture


@pytest.fixture
def clean_gray():
    pil_img = create_clean_document_fixture()
    return np.array(pil_img.convert("L"))


def test_measure_blur(clean_gray):
    res = measure_blur(clean_gray, {"cutoffs": [2500.0, 500.0, 100.0, 25.0]})
    assert res.status == FeatureStatus.MEASURED
    assert res.raw_value is not None and res.raw_value > 1000.0
    assert res.severity == 0


def test_measure_noise(clean_gray):
    res = measure_noise(clean_gray, {"cutoffs": [3.0, 6.0, 11.0, 18.0]})
    assert res.status == FeatureStatus.MEASURED
    assert res.raw_value is not None and res.raw_value < 3.0
    assert res.severity == 0


def test_measure_skew(clean_gray):
    res = measure_skew(clean_gray, {"cutoffs": [0.5, 2.0, 4.0, 7.5]})
    assert res.status == FeatureStatus.MEASURED
    assert res.raw_value is not None and res.raw_value <= 0.5
    assert res.severity == 0


def test_measure_glare(clean_gray):
    res = measure_glare(clean_gray, {"cutoffs": [0.02, 0.06, 0.12, 0.22]})
    assert res.status == FeatureStatus.MEASURED
    assert res.raw_value is not None and res.raw_value < 0.02
    assert res.severity == 0


def test_measure_contrast(clean_gray):
    res = measure_contrast(clean_gray, {"cutoffs": [0.70, 0.50, 0.30, 0.15]})
    assert res.status == FeatureStatus.MEASURED
    assert res.raw_value is not None and res.raw_value >= 0.70
    assert res.severity == 0


def test_measure_resolution(clean_gray):
    res = measure_resolution(clean_gray, {"cutoffs": [0.80, 0.65, 0.35, 0.05]})
    assert res.status == FeatureStatus.MEASURED
    assert res.raw_value is not None and res.raw_value >= 0.80
    assert res.severity == 0


def test_measure_compression(clean_gray):
    res = measure_compression(clean_gray, {"cutoffs": [0.095, 0.110, 0.150, 0.200]})
    assert res.status == FeatureStatus.MEASURED
    assert res.raw_value is not None and res.raw_value <= 0.095
    assert res.severity == 0


def test_measure_illumination(clean_gray):
    res = measure_illumination(clean_gray, {"cutoffs": [195.0, 145.0, 95.0, 50.0]})
    assert res.status == FeatureStatus.MEASURED
    assert res.raw_value is not None and res.raw_value >= 195.0
    assert res.severity == 0


def test_measure_occlusion(clean_gray):
    res = measure_occlusion(clean_gray, {"cutoffs": [0.02, 0.075, 0.15, 0.25]})
    assert res.status == FeatureStatus.MEASURED
    assert res.raw_value is not None and res.raw_value <= 0.02
    assert res.severity == 0


def test_measure_perspective(clean_gray):
    res = measure_perspective(clean_gray, {"cutoffs": [2.5, 10.0, 25.0, 40.0]})
    assert res.status == FeatureStatus.MEASURED
    assert res.raw_value is not None and res.raw_value <= 2.5
    assert res.severity == 0


def test_invalid_input_handling():
    empty_arr = np.array([], dtype=np.uint8)
    assert measure_blur(empty_arr, {}).status == FeatureStatus.INVALID_INPUT
    assert measure_noise(empty_arr, {}).status == FeatureStatus.INVALID_INPUT
    assert measure_skew(empty_arr, {}).status == FeatureStatus.INVALID_INPUT
    assert measure_glare(empty_arr, {}).status == FeatureStatus.INVALID_INPUT
    assert measure_contrast(empty_arr, {}).status == FeatureStatus.INVALID_INPUT
    assert measure_resolution(empty_arr, {}).status == FeatureStatus.INVALID_INPUT
    assert measure_compression(empty_arr, {}).status == FeatureStatus.INVALID_INPUT
    assert measure_illumination(empty_arr, {}).status == FeatureStatus.INVALID_INPUT
    assert measure_occlusion(empty_arr, {}).status == FeatureStatus.INVALID_INPUT
    assert measure_perspective(empty_arr, {}).status == FeatureStatus.INVALID_INPUT
