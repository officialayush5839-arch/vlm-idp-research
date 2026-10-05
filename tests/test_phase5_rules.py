"""
Tests for Phase 5 Feature Adapter and Rule-Based Routing Engine.
Verifies deterministic mapping from visual features to model selection without label leakage.
"""

import pytest
from src.quality.schema import (
    PageQualityAssessment,
    FeatureResult,
    FeatureStatus,
    RuntimeBreakdown,
)
from src.routing.feature_adapter import QualityFeatureAdapter
from src.routing.rule_engine import RuleBasedQualityRouter


@pytest.fixture
def clean_page_assessment() -> PageQualityAssessment:
    """Fixture providing an assessment of a pristine document."""
    features = {
        "blur": FeatureResult(raw_value=1200.0, normalized_value=0.05, severity=0, status=FeatureStatus.MEASURED),
        "noise": FeatureResult(raw_value=1.5, normalized_value=0.04, severity=0, status=FeatureStatus.MEASURED),
        "skew": FeatureResult(raw_value=0.2, normalized_value=0.02, severity=0, status=FeatureStatus.MEASURED),
        "glare": FeatureResult(raw_value=0.01, normalized_value=0.01, severity=0, status=FeatureStatus.MEASURED),
        "contrast": FeatureResult(raw_value=65.0, normalized_value=0.05, severity=0, status=FeatureStatus.MEASURED),
        "resolution": FeatureResult(raw_value=300.0, normalized_value=0.02, severity=0, status=FeatureStatus.MEASURED),
        "compression": FeatureResult(raw_value=0.05, normalized_value=0.05, severity=0, status=FeatureStatus.MEASURED),
        "illumination": FeatureResult(raw_value=180.0, normalized_value=0.03, severity=0, status=FeatureStatus.MEASURED),
        "occlusion": FeatureResult(raw_value=0.0, normalized_value=0.0, severity=0, status=FeatureStatus.MEASURED),
        "perspective": FeatureResult(raw_value=0.02, normalized_value=0.02, severity=0, status=FeatureStatus.MEASURED),
    }
    return PageQualityAssessment(
        document_id="doc_clean_01",
        page_id="doc_clean_01_p0",
        page_number=1,
        width=1000,
        height=1400,
        features=features,
        runtime=RuntimeBreakdown(
            preprocessing_ms=1.0,
            feature_extraction_ms=5.0,
            detection_ms=1.0,
            total_latency_ms=7.0,
        ),
        config_hash="abc1234",
        timestamp_utc="2026-10-05T00:00:00Z",
    )


def test_feature_adapter_clean_extraction(clean_page_assessment):
    adapter = QualityFeatureAdapter()
    features = adapter.extract_features(clean_page_assessment)
    assert len(features) == 10
    assert features["blur"] == pytest.approx(0.05)
    assert features["skew"] == pytest.approx(0.02)
    for k, v in features.items():
        assert 0.0 <= v <= 1.0


def test_feature_adapter_handles_missing_fields():
    adapter = QualityFeatureAdapter()
    empty_assessment = PageQualityAssessment(
        document_id="doc_empty_01",
        page_id="doc_empty_01_p0",
        page_number=1,
        width=100,
        height=100,
        features={},
        runtime=RuntimeBreakdown(
            preprocessing_ms=0.0,
            feature_extraction_ms=0.0,
            detection_ms=0.0,
            total_latency_ms=0.0,
        ),
        config_hash="none",
        timestamp_utc="2026-10-05T00:00:00Z",
    )
    features = adapter.extract_features(empty_assessment)
    assert len(features) == 10
    assert all(v == 0.0 for v in features.values())


def test_rule_engine_clean_route(clean_page_assessment):
    router = RuleBasedQualityRouter.from_config()
    adapter = QualityFeatureAdapter()
    features = adapter.extract_features(clean_page_assessment)
    model, reason, conf = router.route(features)
    assert model in ["B0", "B1"]
    assert "clean" in reason.lower()
    assert conf >= 0.80


def test_rule_engine_geometric_distortion(clean_page_assessment):
    router = RuleBasedQualityRouter.from_config()
    adapter = QualityFeatureAdapter()
    features = adapter.extract_features(clean_page_assessment)
    # Inject severe skew
    features["skew"] = 0.65
    model, reason, conf = router.route(features)
    assert model == "B2"
    assert "geometric" in reason.lower() or "skew" in reason.lower()
    assert conf >= 0.85


def test_rule_engine_severe_blur(clean_page_assessment):
    router = RuleBasedQualityRouter.from_config()
    adapter = QualityFeatureAdapter()
    features = adapter.extract_features(clean_page_assessment)
    features["blur"] = 0.70
    model, reason, conf = router.route(features)
    assert model == "B2"
    assert "blur" in reason.lower() or "noise" in reason.lower()


def test_rule_engine_compression_and_illumination(clean_page_assessment):
    router = RuleBasedQualityRouter.from_config()
    adapter = QualityFeatureAdapter()
    features = adapter.extract_features(clean_page_assessment)
    features["compression"] = 0.68
    model, reason, conf = router.route(features)
    assert model == "B0-U"
    assert "compression" in reason.lower() or "illumination" in reason.lower()


def test_rule_engine_occlusion_route(clean_page_assessment):
    router = RuleBasedQualityRouter.from_config()
    adapter = QualityFeatureAdapter()
    features = adapter.extract_features(clean_page_assessment)
    features["occlusion"] = 0.50
    model, reason, conf = router.route(features)
    assert model == "B2"
    assert "occlusion" in reason.lower()
