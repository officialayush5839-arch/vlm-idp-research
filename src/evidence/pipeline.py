"""
Master Evidence Grounding Pipeline for Phase 7.
Coordinates extraction, spatial validation, multi-page aggregation,
semantic/numeric/table verification, sufficiency assessment, decision state machine,
and cryptographic citation generation.
"""

from typing import List, Dict, Any, Optional, Tuple
from src.evidence.schema import (
    EvidenceUnit,
    GroundingResult,
    EvidenceSupportResult,
    CitationRecord,
    Phase7EvidencePackage
)
from src.evidence.extractor import EvidenceExtractor
from src.evidence.region_validator import SpatialRegionValidator
from src.evidence.semantic_support import SemanticSupportVerifier
from src.evidence.numeric_verifier import NumericVerifier
from src.evidence.table_verifier import TableVerifier
from src.evidence.evidence_sufficiency import EvidenceSufficiencyEvaluator
from src.evidence.multipage_aggregator import MultiPageAggregator
from src.evidence.grounding_classifier import GroundingClassifier
from src.evidence.citation import CitationGenerator
from src.evidence.provenance import build_provenance_record
from src.evidence.baselines import get_baseline_config


class EvidenceGroundingPipeline:
    """
    End-to-end evidence grounding and answer support validation pipeline.
    """

    def __init__(
        self,
        spatial_validator: Optional[SpatialRegionValidator] = None,
        semantic_verifier: Optional[SemanticSupportVerifier] = None,
        numeric_verifier: Optional[NumericVerifier] = None,
        table_verifier: Optional[TableVerifier] = None,
        sufficiency_evaluator: Optional[EvidenceSufficiencyEvaluator] = None,
        multipage_aggregator: Optional[MultiPageAggregator] = None,
        extractor: Optional[EvidenceExtractor] = None
    ):
        self.spatial_validator = spatial_validator or SpatialRegionValidator()
        self.semantic_verifier = semantic_verifier or SemanticSupportVerifier()
        self.numeric_verifier = numeric_verifier or NumericVerifier()
        self.table_verifier = table_verifier or TableVerifier()
        self.sufficiency_evaluator = sufficiency_evaluator or EvidenceSufficiencyEvaluator()
        self.multipage_aggregator = multipage_aggregator or MultiPageAggregator()
        self.extractor = extractor or EvidenceExtractor()

        self.classifier = GroundingClassifier(
            spatial_validator=self.spatial_validator,
            semantic_verifier=self.semantic_verifier,
            numeric_verifier=self.numeric_verifier,
            table_verifier=self.table_verifier,
            sufficiency_evaluator=self.sufficiency_evaluator
        )

    def process(
        self,
        document_id: str,
        query_id: str,
        query_text: str,
        answer_text: str,
        selected_pages: List[Dict[str, Any]],
        selected_regions: List[Dict[str, Any]],
        baseline_id: str = "B7-5",
        dataset: str = "docvqa",
        condition: str = "clean",
        seed: int = 42,
        ground_truth_bboxes: Optional[List[Tuple[int, int, int, int]]] = None,
        page_dimensions: Optional[Dict[int, Tuple[int, int]]] = None
    ) -> Phase7EvidencePackage:
        """
        Execute full grounding pipeline and return structured Phase7EvidencePackage.
        """
        base_cfg = get_baseline_config(baseline_id)
        package_id = f"pkg_{baseline_id}_{document_id}_{query_id}_s{seed}"

        # Step 1: Extract candidate evidence units
        evidence_units = self.extractor.extract_from_phase6_package(
            package_id=package_id,
            document_id=document_id,
            selected_pages=selected_pages,
            selected_regions=selected_regions,
            page_dimensions=page_dimensions
        )

        # Baseline specific adjustments:
        # B7-0 (Random) has degraded units or random noise
        # B7-1/B7-2 do not use fine-grained layout bboxes (revert to full page bboxes)
        if not base_cfg["uses_layout"]:
            for u in evidence_units:
                u.bbox_1000 = (0, 0, 1000, 1000)

        # Step 2: Multi-page aggregation
        agg_out = self.multipage_aggregator.aggregate_evidence(evidence_units)

        # Step 3: Grounding classification
        grounding_result, support_result = self.classifier.classify_grounding(
            query_text=query_text,
            answer_text=answer_text,
            evidence_units=evidence_units,
            ground_truth_bboxes=ground_truth_bboxes
        )

        # Step 4: Citations for contributing evidence units
        citations = []
        contributing_units = [u for u in evidence_units if u.evidence_id in grounding_result.evidence_ids]
        if not contributing_units and evidence_units:
            contributing_units = [evidence_units[0]]

        for u in contributing_units:
            cit = CitationGenerator.generate_citation(u)
            citations.append(cit)

        # Step 5: Provenance
        provenance = build_provenance_record(
            dataset=dataset,
            baseline=baseline_id,
            document_id=document_id,
            query_id=query_id,
            condition=condition,
            seed=seed,
            extra_metadata={
                "upstream_retrieval": base_cfg["upstream_retrieval"],
                "evidence_count": len(evidence_units),
                "citation_count": len(citations),
                "grounding_status": grounding_result.grounding_status,
                "answer_support_status": support_result.support_status
            }
        )

        # Step 6: Compute package hash and collect page/region lists
        pages_list = sorted(list({u.page_id for u in evidence_units})) if evidence_units else [p.get("page_number", 1) for p in selected_pages]
        regions_list = [u.region_id for u in evidence_units] if evidence_units else [r.get("region_id", "") for r in selected_regions]
        raw_pkg_str = f"{package_id}|{document_id}|{query_id}|{grounding_result.grounding_status}|{support_result.support_status}"
        from src.evidence.provenance import compute_sha256
        pkg_hash = compute_sha256(raw_pkg_str)

        return Phase7EvidencePackage(
            package_id=package_id,
            document_id=document_id,
            query_id=query_id,
            query_text=query_text,
            retrieval_method=base_cfg["upstream_retrieval"],
            selected_pages=pages_list,
            selected_regions=regions_list,
            evidence_units=evidence_units,
            support_result=support_result,
            grounding_result=grounding_result,
            citations=citations,
            provenance=provenance,
            package_hash=pkg_hash
        )
