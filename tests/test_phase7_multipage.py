"""
Unit tests for Phase 7 Multi-Page Evidence Aggregator.
"""

from src.evidence.schema import EvidenceUnit
from src.evidence.multipage_aggregator import MultiPageAggregator


def test_multipage_aggregator():
    aggregator = MultiPageAggregator()

    units = [
        EvidenceUnit(
            evidence_id="ev_p1_1",
            document_id="doc_multi_01",
            page_id=1,
            region_id="reg_1",
            bbox_1000=(100, 100, 900, 200),
            text="Executive summary of quarterly earnings.",
            provenance_hash="hash1",
            retrieval_score=0.9
        ),
        EvidenceUnit(
            evidence_id="ev_p3_1",
            document_id="doc_multi_01",
            page_id=3,
            region_id="reg_3",
            bbox_1000=(100, 300, 900, 500),
            text="Detailed breakdown: operating expense was $500k.",
            provenance_hash="hash2",
            retrieval_score=0.8
        )
    ]

    out = aggregator.aggregate_evidence(units)
    assert out["page_count"] == 2
    assert out["distinct_pages"] == [1, 3]
    assert out["primary_page"] == 1
    assert "Executive summary" in out["combined_text"]
    assert "Detailed breakdown" in out["combined_text"]
    assert out["cross_page_score"] > 0.0


def test_multipage_aggregator_empty():
    aggregator = MultiPageAggregator()
    out = aggregator.aggregate_evidence([])
    assert out["page_count"] == 0
    assert out["distinct_pages"] == []
    assert out["combined_text"] == ""
