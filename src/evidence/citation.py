"""
Evidence Citation Generator and Verifier for Phase 7 Evidence Grounding.
Produces deterministic, tamper-evident citations linking answer claims
to underlying document pages, coordinates, and cryptographic hashes.
"""

from typing import List, Dict, Any, Optional, Tuple
from src.evidence.schema import EvidenceUnit, CitationRecord
from src.evidence.provenance import compute_sha256


class CitationGenerator:
    """
    Generates structured, verifiable citations from evidence units.
    """

    @classmethod
    def generate_citation(cls, unit: EvidenceUnit) -> CitationRecord:
        """
        Create a CitationRecord for an atomic EvidenceUnit.
        """
        short_hash = unit.provenance_hash[:8]
        cit_id = f"cit_{unit.document_id}_p{unit.page_id}_{unit.region_id}_{short_hash}"

        return CitationRecord(
            citation_id=cit_id,
            document_id=unit.document_id,
            page_number=unit.page_id,
            region_id=unit.region_id,
            bbox=unit.bbox_1000,
            evidence_id=unit.evidence_id,
            provenance_hash=unit.provenance_hash,
            text_snippet=unit.text[:120]
        )

    @classmethod
    def format_inline_citation(cls, citation: CitationRecord) -> str:
        """
        Deterministic string representation for inline text output.
        """
        return (
            f"[Doc: {citation.document_id}, Page: {citation.page_number}, "
            f"Region: {citation.region_id}, BBox: {list(citation.bbox)}, "
            f"Hash: {citation.provenance_hash[:8]}]"
        )

    @classmethod
    def verify_citation_integrity(
        cls,
        citation: CitationRecord,
        unit: EvidenceUnit
    ) -> bool:
        """
        Verify that a citation record strictly matches the referenced evidence unit.
        """
        if citation.evidence_id != unit.evidence_id:
            return False
        if citation.document_id != unit.document_id:
            return False
        if citation.page_number != unit.page_id:
            return False
        if citation.region_id != unit.region_id:
            return False
        if citation.bbox != unit.bbox_1000:
            return False
        if citation.provenance_hash != unit.provenance_hash:
            return False
        return True
