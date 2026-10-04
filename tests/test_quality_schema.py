"""Unit tests for Phase 3 Quality and Degradation Schemas."""

import pytest
from src.quality.schema import (
    DegradationDetection,
    DocumentQualityAssessment,
    FeatureResult,
    FeatureStatus,
    PageQualityAssessment,
    RuntimeBreakdown,
    SeverityLevel,
)


def test_feature_status_enum():
    assert FeatureStatus.MEASURED.value == "MEASURED"
    assert FeatureStatus.FAILED.value == "FAILED"
    assert FeatureStatus.NOT_AVAILABLE.value == "NOT_AVAILABLE"
    assert FeatureStatus.INVALID_INPUT.value == "INVALID_INPUT"
    assert FeatureStatus.NOT_APPLICABLE.value == "NOT_APPLICABLE"


def test_severity_level_enum():
    assert SeverityLevel.S0_CLEAN == 0
    assert SeverityLevel.S1_MILD == 1
    assert SeverityLevel.S2_MODERATE == 2
    assert SeverityLevel.S3_SEVERE == 3
    assert SeverityLevel.S4_EXTREME == 4


def test_feature_result_defaults():
    res = FeatureResult(raw_value=12.5, severity=1, status=FeatureStatus.MEASURED)
    assert res.raw_value == 12.5
    assert res.severity == 1
    assert res.status == FeatureStatus.MEASURED
    assert res.normalized_value is None
    assert res.direction == "higher_is_worse"


def test_page_quality_assessment_schema():
    runtime = RuntimeBreakdown(
        preprocessing_ms=5.0,
        feature_extraction_ms=25.0,
        detection_ms=1.0,
        aggregation_ms=0.0,
        total_latency_ms=31.0,
    )
    page_res = PageQualityAssessment(
        document_id="doc_123",
        page_id="p_123_001",
        page_number=1,
        width=600,
        height=400,
        features={
            "blur": FeatureResult(raw_value=500.0, severity=0, status=FeatureStatus.MEASURED),
        },
        detected_degradations=[],
        overall_quality_score=None,
        overall_quality_status="NOT_DEFINED",
        runtime=runtime,
        algorithm_version="1.0.0",
        config_hash="abc123hash",
        timestamp_utc="2026-10-05T00:00:00Z",
        status="SUCCESS",
    )
    assert page_res.document_id == "doc_123"
    assert page_res.overall_quality_score is None
    assert page_res.overall_quality_status == "NOT_DEFINED"
    data = page_res.model_dump()
    assert data["document_id"] == "doc_123"
    assert "features" in data
    assert data["features"]["blur"]["raw_value"] == 500.0


def test_document_quality_assessment_schema():
    runtime = RuntimeBreakdown(
        preprocessing_ms=5.0,
        feature_extraction_ms=25.0,
        detection_ms=1.0,
        aggregation_ms=0.5,
        total_latency_ms=31.5,
    )
    page1 = PageQualityAssessment(
        document_id="doc_multi",
        page_id="doc_multi_p1",
        page_number=1,
        width=600,
        height=400,
        features={"blur": FeatureResult(raw_value=500.0, severity=0, status=FeatureStatus.MEASURED)},
        runtime=runtime,
        algorithm_version="1.0.0",
        config_hash="hash",
        timestamp_utc="2026-10-05T00:00:00Z",
    )
    doc_res = DocumentQualityAssessment(
        document_id="doc_multi",
        page_count=1,
        pages=[page1],
        summary_statistics={"blur": {"mean": 500.0, "std": 0.0}},
        worst_page_id="doc_multi_p1",
        worst_page_number=1,
        highest_severity_detected=0,
        algorithm_version="1.0.0",
        config_hash="hash",
        timestamp_utc="2026-10-05T00:00:00Z",
    )
    assert doc_res.page_count == 1
    assert doc_res.worst_page_id == "doc_multi_p1"
    assert doc_res.status == "SUCCESS"
