"""
Unit tests for Phase 8 Schemas and Domain Models.
"""

import pytest
from src.uncertainty.schema import (
    UncertaintyFeatures,
    CalibrationArtifact,
    AbstentionDecision,
    UncertaintyPackage,
    CalibrationMetricsResult,
    SelectivePredictionMetricsResult
)


def test_uncertainty_features_valid():
    feat = UncertaintyFeatures(
        model_confidence=0.85,
        retrieval_margin=0.30,
        retrieval_entropy=0.15,
        semantic_support_score=0.90,
        entity_coverage=0.80,
        spatial_valid=1.0,
        sufficiency_status="SUFFICIENT",
        grounding_status="GROUNDED",
        citation_count=2,
        visual_quality_score=0.92,
        quality_blur=0.05,
        quality_noise=0.02,
        page_count=10,
        composite_raw_confidence=0.88
    )
    vec = feat.to_feature_vector()
    assert len(vec) == 16
    assert all(0.0 <= v <= 1.0 for v in vec)


def test_calibration_artifact_schema():
    art = CalibrationArtifact(
        method="temperature_scaling",
        training_partition="val",
        temperature=1.45,
        config_hash="cfg_hash_123",
        artifact_hash="art_hash_456",
        created_at_utc="2026-10-05T12:00:00Z"
    )
    assert art.temperature == 1.45
    assert art.method == "temperature_scaling"


def test_abstention_decision_schema():
    dec = AbstentionDecision(
        decision="ANSWER",
        calibrated_confidence=0.82,
        threshold=0.75,
        target_coverage=0.80,
        margin=0.07,
        abstention_reason="Confidence exceeds threshold"
    )
    assert dec.decision == "ANSWER"
    assert dec.margin == pytest.approx(0.07, 1e-4)


def test_uncertainty_package_schema():
    feat = UncertaintyFeatures()
    dec = AbstentionDecision(
        decision="ANSWER",
        calibrated_confidence=0.90,
        threshold=0.70,
        target_coverage=0.80,
        margin=0.20
    )
    pkg = UncertaintyPackage(
        package_id="pkg_u_01",
        document_id="doc_01",
        query_id="q_01",
        raw_confidence=0.85,
        calibrated_confidence=0.90,
        features=feat,
        decision=dec,
        calibration_method="isotonic_regression",
        provenance={"seed": 42},
        package_hash="hash_abc_123"
    )
    assert pkg.package_id == "pkg_u_01"
    assert pkg.calibrated_confidence == 0.90
