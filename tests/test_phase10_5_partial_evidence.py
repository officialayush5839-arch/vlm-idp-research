"""tests/test_phase10_5_partial_evidence.py
Unit tests for partial evidence extraction and verifiable subspan grounding.
"""

from src.recovery.partial_evidence import PartialEvidenceExtractor
from src.reliability.signals import ObservableSignals


def test_partial_evidence_extraction():
    extractor = PartialEvidenceExtractor()
    sig = ObservableSignals(sufficiency_score=0.60, semantic_score=0.70)
    cand = "Total Invoice Amount $500.00"
    res = extractor.extract_partial(cand, sig)
    assert res.is_partial is True
    assert len(res.extracted_subspan) > 0
    assert res.extracted_subspan in cand


def test_partial_evidence_insufficient():
    extractor = PartialEvidenceExtractor()
    sig = ObservableSignals(sufficiency_score=0.20, semantic_score=0.20)
    cand = "Total Invoice Amount $500.00"
    res = extractor.extract_partial(cand, sig)
    assert res.is_partial is False
    assert res.extracted_subspan == ""
