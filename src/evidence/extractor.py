"""
Evidence Extraction Module for Phase 7 Evidence Grounding.
Transforms upstream retrieval packages and document representations into standardized
atomic EvidenceUnit objects.
"""

from typing import List, Dict, Any, Optional, Tuple
from src.evidence.schema import EvidenceUnit
from src.evidence.region_validator import clip_bbox_1000, bbox_1000_to_pixel, is_valid_bbox_1000
from src.evidence.provenance import compute_evidence_unit_hash


class EvidenceExtractor:
    """
    Extracts, normalizes, and validates atomic EvidenceUnit objects
    from upstream retrieval packages and page records.
    """

    def __init__(self, default_entity_type: str = "text"):
        self.default_entity_type = default_entity_type

    def extract_from_phase6_package(
        self,
        package_id: str,
        document_id: str,
        selected_pages: List[Dict[str, Any]],
        selected_regions: List[Dict[str, Any]],
        page_dimensions: Optional[Dict[int, Tuple[int, int]]] = None
    ) -> List[EvidenceUnit]:
        """
        Convert Phase 6 selected_pages and selected_regions into a list of EvidenceUnit objects.
        """
        evidence_units: List[EvidenceUnit] = []
        page_dimensions = page_dimensions or {}

        # 1. Process selected regions (fine-grained units)
        for rank, reg in enumerate(selected_regions, start=1):
            reg_id = reg.get("region_id", f"reg_{rank}")
            page_num = reg.get("page_number", 1)
            raw_bbox = reg.get("bbox", (0, 0, 1000, 1000))
            bbox_1000 = clip_bbox_1000(raw_bbox)
            text = reg.get("snippet", reg.get("text_content", "")).strip()
            score = float(reg.get("score", 0.0))
            source_type = reg.get("source_type", "multimodal")
            if source_type not in ["text", "table", "figure", "form", "layout", "multimodal"]:
                source_type = "multimodal"

            bbox_pixel = None
            if page_num in page_dimensions:
                w, h = page_dimensions[page_num]
                bbox_pixel = bbox_1000_to_pixel(bbox_1000, w, h)

            ev_id = f"ev_{package_id}_p{page_num}_{reg_id}"
            ev_hash = compute_evidence_unit_hash(document_id, page_num, reg_id, bbox_1000, text)

            unit = EvidenceUnit(
                evidence_id=ev_id,
                document_id=document_id,
                page_id=page_num,
                region_id=reg_id,
                bbox_1000=bbox_1000,
                bbox_pixel=bbox_pixel,
                text=text,
                entity_type=reg.get("entity_type", self.default_entity_type),
                source_type=source_type,
                retrieval_score=score,
                retrieval_rank=rank,
                page_rank=reg.get("page_rank", 1),
                region_rank=reg.get("region_rank", rank),
                provenance_hash=ev_hash
            )
            evidence_units.append(unit)

        # 2. If no regions provided, create coarse page-level evidence units
        if not evidence_units and selected_pages:
            for rank, page_rec in enumerate(selected_pages, start=1):
                page_num = page_rec.get("page_number", 1)
                text = page_rec.get("clean_text", page_rec.get("raw_text", page_rec.get("snippet", ""))).strip()
                score = float(page_rec.get("score", 0.0))
                reg_id = f"page_full_{page_num}"
                bbox_1000 = (0, 0, 1000, 1000)

                bbox_pixel = None
                if page_num in page_dimensions:
                    w, h = page_dimensions[page_num]
                    bbox_pixel = (0, 0, w, h)

                ev_id = f"ev_{package_id}_p{page_num}_{reg_id}"
                ev_hash = compute_evidence_unit_hash(document_id, page_num, reg_id, bbox_1000, text)

                unit = EvidenceUnit(
                    evidence_id=ev_id,
                    document_id=document_id,
                    page_id=page_num,
                    region_id=reg_id,
                    bbox_1000=bbox_1000,
                    bbox_pixel=bbox_pixel,
                    text=text,
                    entity_type="text",
                    source_type="multimodal",
                    retrieval_score=score,
                    retrieval_rank=rank,
                    page_rank=rank,
                    region_rank=1,
                    provenance_hash=ev_hash
                )
                evidence_units.append(unit)

        return evidence_units
