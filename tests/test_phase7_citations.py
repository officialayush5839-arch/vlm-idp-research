"""
Unit tests for Phase 7 Citation Generator and Verifier.
"""

from src.evidence.schema import EvidenceUnit
from src.evidence.citation import CitationGenerator


def test_generate_and_format_citation():
    unit = EvidenceUnit(
        evidence_id="ev_001",
        document_id="doc_report_99",
        page_id=3,
        region_id="reg_summary",
        bbox_1000=(100, 200, 800, 400),
        text="The consolidated revenue for Q4 reached $12.4M.",
        provenance_hash="abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789"
    )

    cit = CitationGenerator.generate_citation(unit)
    assert cit.document_id == "doc_report_99"
    assert cit.page_number == 3
    assert cit.region_id == "reg_summary"
    assert cit.bbox == (100, 200, 800, 400)
    assert cit.provenance_hash == unit.provenance_hash

    inline_str = CitationGenerator.format_inline_citation(cit)
    assert "[Doc: doc_report_99, Page: 3" in inline_str
    assert "Hash: abcdef01" in inline_str

    assert CitationGenerator.verify_citation_integrity(cit, unit) is True


def test_citation_integrity_tamper():
    unit = EvidenceUnit(
        evidence_id="ev_001",
        document_id="doc_report_99",
        page_id=3,
        region_id="reg_summary",
        bbox_1000=(100, 200, 800, 400),
        text="The consolidated revenue for Q4 reached $12.4M.",
        provenance_hash="abcdef0123456789"
    )
    cit = CitationGenerator.generate_citation(unit)

    # Tamper with bbox
    cit_tampered = cit.model_copy(update={"bbox": (100, 200, 800, 999)})
    assert CitationGenerator.verify_citation_integrity(cit_tampered, unit) is False
