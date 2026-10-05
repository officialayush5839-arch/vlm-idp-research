"""
Unit tests for Phase 7 Evidence Sufficiency Evaluator.
"""

from src.evidence.schema import EvidenceUnit
from src.evidence.evidence_sufficiency import EvidenceSufficiencyEvaluator


def test_evidence_sufficiency_sufficient():
    evaluator = EvidenceSufficiencyEvaluator(min_coverage_sufficient=0.70)
    units = [
        EvidenceUnit(
            evidence_id="ev_1",
            document_id="doc_1",
            page_id=1,
            region_id="reg_1",
            bbox_1000=(100, 100, 500, 500),
            text="The annual total operating revenue for Acme was $50M in 2023.",
            provenance_hash="h1"
        )
    ]

    res = evaluator.evaluate_sufficiency(
        query_text="What was the operating revenue for Acme?",
        evidence_units=units
    )
    assert res["sufficiency_status"] == "SUFFICIENT"
    assert res["coverage_score"] >= 0.70
    assert len(res["missing_tokens"]) == 0


def test_evidence_sufficiency_insufficient():
    evaluator = EvidenceSufficiencyEvaluator(min_coverage_partial=0.40)
    units = [
        EvidenceUnit(
            evidence_id="ev_1",
            document_id="doc_1",
            page_id=1,
            region_id="reg_1",
            bbox_1000=(100, 100, 500, 500),
            text="Table of Contents and General Legal Notices.",
            provenance_hash="h1"
        )
    ]

    res = evaluator.evaluate_sufficiency(
        query_text="What was the net profit margin in Germany for fiscal year 2021?",
        evidence_units=units
    )
    assert res["sufficiency_status"] == "INSUFFICIENT"
    assert res["coverage_score"] < 0.40
    assert len(res["missing_tokens"]) > 0
