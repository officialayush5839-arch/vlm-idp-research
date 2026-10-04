"""Integration tests validating Phase 3 degradation detection on synthetic corruptions."""

import pytest
from src.quality.pipeline import DocumentQualityPipeline
from src.quality.synthetic import apply_degradation, create_clean_document_fixture


@pytest.fixture
def pipeline():
    return DocumentQualityPipeline()


@pytest.fixture
def clean_image():
    return create_clean_document_fixture()


def test_detects_severe_blur(pipeline, clean_image):
    blurred = apply_degradation(clean_image, "gaussian_blur", 3, seed=42)
    res = pipeline.assess_page(blurred, "doc_b", "p1")
    dets = [d for d in res.detected_degradations if d.family == "gaussian_blur"]
    assert len(dets) == 1
    assert dets[0].severity >= 3


def test_detects_severe_noise(pipeline, clean_image):
    noisy = apply_degradation(clean_image, "gaussian_noise", 3, seed=42)
    res = pipeline.assess_page(noisy, "doc_n", "p1")
    dets = [d for d in res.detected_degradations if d.family == "gaussian_noise"]
    assert len(dets) == 1
    assert dets[0].severity >= 3


def test_detects_severe_skew(pipeline, clean_image):
    skewed = apply_degradation(clean_image, "skew_rotation", 3, seed=42)
    res = pipeline.assess_page(skewed, "doc_s", "p1")
    dets = [d for d in res.detected_degradations if d.family == "skew_rotation"]
    assert len(dets) == 1
    assert dets[0].severity >= 3


def test_detects_severe_illumination_attenuation(pipeline, clean_image):
    dim = apply_degradation(clean_image, "illumination", 3, seed=42)
    res = pipeline.assess_page(dim, "doc_i", "p1")
    dets = [d for d in res.detected_degradations if d.family == "illumination"]
    assert len(dets) == 1
    assert dets[0].severity >= 3


def test_detects_severe_occlusion(pipeline, clean_image):
    occluded = apply_degradation(clean_image, "occlusion", 3, seed=42)
    res = pipeline.assess_page(occluded, "doc_o", "p1")
    dets = [d for d in res.detected_degradations if d.family == "occlusion"]
    assert len(dets) == 1
    assert dets[0].severity >= 3


def test_detects_severe_resolution_reduction(pipeline, clean_image):
    downsampled = apply_degradation(clean_image, "resolution_reduction", 3, seed=42)
    res = pipeline.assess_page(downsampled, "doc_r", "p1")
    dets = [d for d in res.detected_degradations if d.family == "resolution_reduction"]
    assert len(dets) == 1
    assert dets[0].severity >= 3


def test_detects_severe_perspective_distortion(pipeline, clean_image):
    warped = apply_degradation(clean_image, "perspective_distortion", 3, seed=42)
    res = pipeline.assess_page(warped, "doc_p", "p1")
    dets = [d for d in res.detected_degradations if d.family == "perspective_distortion"]
    assert len(dets) == 1
    assert dets[0].severity >= 3
