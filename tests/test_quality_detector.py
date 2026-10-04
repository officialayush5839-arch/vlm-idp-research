"""Unit tests for Phase 3 Degradation Detector."""

import pytest

from src.quality.config import load_phase3_quality_config
from src.quality.detector import detect_degradations
from src.quality.schema import FeatureResult, FeatureStatus


@pytest.fixture
def quality_config():
    return load_phase3_quality_config()


def test_detector_clean_no_detections(quality_config):
    clean_features = {
        "blur": FeatureResult(raw_value=3000.0, severity=0, status=FeatureStatus.MEASURED),
        "noise": FeatureResult(raw_value=1.5, severity=0, status=FeatureStatus.MEASURED),
        "skew": FeatureResult(raw_value=0.1, severity=0, status=FeatureStatus.MEASURED),
    }
    detections, elapsed_ms = detect_degradations(clean_features, quality_config)
    assert len(detections) == 0
    assert elapsed_ms >= 0.0


def test_detector_single_degradation(quality_config):
    features = {
        "blur": FeatureResult(raw_value=30.0, severity=3, status=FeatureStatus.MEASURED),
        "noise": FeatureResult(raw_value=1.5, severity=0, status=FeatureStatus.MEASURED),
    }
    detections, _ = detect_degradations(features, quality_config)
    assert len(detections) == 1
    assert detections[0].family == "gaussian_blur"
    assert detections[0].severity == 3
    assert detections[0].severity_label == "S3_SEVERE"
    assert detections[0].evidence_feature == "blur"


def test_detector_mixed_composite_trigger(quality_config):
    features = {
        "blur": FeatureResult(raw_value=30.0, severity=3, status=FeatureStatus.MEASURED),
        "noise": FeatureResult(raw_value=15.0, severity=3, status=FeatureStatus.MEASURED),
        "skew": FeatureResult(raw_value=5.0, severity=3, status=FeatureStatus.MEASURED),
    }
    detections, _ = detect_degradations(features, quality_config)
    # 3 individual + 1 composite mixed degradation detection
    assert len(detections) == 4
    families = [d.family for d in detections]
    assert "mixed_degradation" in families
