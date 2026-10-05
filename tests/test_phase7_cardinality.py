"""
Unit tests for Phase 7 Cardinality and Entity Integrity.
"""

from src.evidence.pipeline import EvidenceGroundingPipeline


def test_citation_cardinality_invariants():
    pipeline = EvidenceGroundingPipeline()

    doc_id = "doc_card_001"
    query_id = "q_card_001"
    query = "What is the vendor address?"
    answer = "123 Main Street"
    pages = [{"page_number": 1, "score": 0.9, "clean_text": "Vendor: 123 Main Street"}]
    regions = [
        {"region_id": "r1", "page_number": 1, "bbox": (10, 10, 500, 100), "snippet": "Vendor: 123 Main Street", "score": 0.9},
        {"region_id": "r2", "page_number": 1, "bbox": (10, 120, 500, 200), "snippet": "Invoice Date: 2024-01-01", "score": 0.6}
    ]

    pkg = pipeline.process(
        document_id=doc_id,
        query_id=query_id,
        query_text=query,
        answer_text=answer,
        selected_pages=pages,
        selected_regions=regions,
        baseline_id="B7-5",
        dataset="docvqa",
        condition="clean",
        seed=42
    )

    ev_ids = {u.evidence_id for u in pkg.evidence_units}
    assert len(pkg.evidence_units) == 2

    # All citations must correspond to known evidence units
    for cit in pkg.citations:
        assert cit.evidence_id in ev_ids


def test_empty_candidate_cardinality():
    pipeline = EvidenceGroundingPipeline()
    pkg = pipeline.process(
        document_id="doc_empty",
        query_id="q_empty",
        query_text="What is this?",
        answer_text="Nothing",
        selected_pages=[],
        selected_regions=[],
        baseline_id="B7-5",
        dataset="docvqa",
        condition="clean",
        seed=42
    )
    assert len(pkg.evidence_units) == 0
    assert len(pkg.citations) == 0
    assert pkg.grounding_result.grounding_status == "UNSUPPORTED"
    assert pkg.support_result.support_status == "INSUFFICIENT_EVIDENCE"
