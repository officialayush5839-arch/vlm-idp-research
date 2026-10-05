"""
Unit tests for Phase 7 Evidence Grounding Schemas.
"""

import pytest
from pydantic import ValidationError
from src.evidence.schema import (
    EvidenceUnit,
    EvidenceSupportResult,
    GroundingResult,
    CitationRecord,
    Phase7EvidencePackage,
    GroundingMetricsResult
)


def test_evidence_unit_valid():
    unit = EvidenceUnit(
        evidence_id="ev_001",
        document_id="doc_mp_001",
        page_id=2,
        region_id="doc_mp_001_p2_tbl1",
        bbox_1000=(80, 120, 920, 580),
        text="Consolidated Table for revenue: Total = $48.7M",
        entity_type="table",
        source_type="table",
        retrieval_score=0.95,
        retrieval_rank=1,
        page_rank=1,
        region_rank=1,
        provenance_hash="abc1234def5678"
    )
    assert unit.evidence_id == "ev_001"
    assert unit.bbox_1000 == (80, 120, 920, 580)
    assert unit.page_id == 2


def test_evidence_unit_invalid_bbox():
    # Out of bounds
    with pytest.raises(ValidationError):
        EvidenceUnit(
            evidence_id="ev_bad",
            document_id="doc_1",
            page_id=1,
            region_id="r1",
            bbox_1000=(0, 0, 1500, 500),
            provenance_hash="hash"
        )

    # Inverted
    with pytest.raises(ValidationError):
        EvidenceUnit(
            evidence_id="ev_bad",
            document_id="doc_1",
            page_id=1,
            region_id="r1",
            bbox_1000=(500, 100, 400, 200),
            provenance_hash="hash"
        )


def test_evidence_support_result():
    res = EvidenceSupportResult(
        support_status="SUPPORTED",
        semantic_score=0.88,
        spatial_score=0.92,
        coverage_score=0.80,
        sufficiency_score=0.90,
        reason="Target revenue table localized with exact numerical figure",
        evidence_ids=["ev_001"]
    )
    assert res.support_status == "SUPPORTED"
    assert res.semantic_score == 0.88


def test_grounding_result():
    gr = GroundingResult(
        grounding_status="GROUNDED",
        answer_support_status="SUPPORTED",
        spatial_grounding_status="PASS",
        evidence_sufficiency_status="SUFFICIENT",
        grounding_score=0.89,
        evidence_ids=["ev_001"]
    )
    assert gr.grounding_status == "GROUNDED"
    assert gr.spatial_grounding_status == "PASS"


def test_citation_record():
    cit = CitationRecord(
        citation_id="cit_01",
        document_id="doc_mp_001",
        page_number=2,
        region_id="tbl1",
        bbox=(80, 120, 920, 580),
        evidence_id="ev_001",
        provenance_hash="hash123",
        text_snippet="Total = $48.7M"
    )
    assert cit.page_number == 2
    assert cit.citation_id == "cit_01"


def test_phase7_evidence_package():
    supp = EvidenceSupportResult(
        support_status="SUPPORTED",
        semantic_score=0.9,
        spatial_score=0.9,
        coverage_score=0.9,
        sufficiency_score=0.9,
        reason="Exact match",
        evidence_ids=["ev_01"]
    )
    gr = GroundingResult(
        grounding_status="GROUNDED",
        answer_support_status="SUPPORTED",
        spatial_grounding_status="PASS",
        evidence_sufficiency_status="SUFFICIENT",
        grounding_score=0.9,
        evidence_ids=["ev_01"]
    )
    pkg = Phase7EvidencePackage(
        package_id="pkg_p7_test",
        document_id="doc_mp_001",
        query_id="q1",
        query_text="What is total revenue?",
        retrieval_method="B7-5",
        selected_pages=[2],
        selected_regions=["r1"],
        evidence_units=[],
        support_result=supp,
        grounding_result=gr,
        citations=[],
        provenance={"run_id": "test_run"},
        package_hash="hash_p7_test"
    )
    assert pkg.package_id == "pkg_p7_test"
    assert pkg.support_result.support_status == "SUPPORTED"
