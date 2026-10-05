"""
Grounding Classifier and Decision State Machine for Phase 7 Evidence Grounding.
Enforces the 4-state decision tree:
- SUPPORTED
- PARTIALLY_SUPPORTED
- NOT_SUPPORTED
- INSUFFICIENT_EVIDENCE
and composite grounding statuses:
- GROUNDED
- PARTIALLY_GROUNDED
- UNSUPPORTED
"""

from typing import List, Dict, Any, Optional, Tuple
from src.evidence.schema import EvidenceUnit, GroundingResult, EvidenceSupportResult
from src.evidence.region_validator import SpatialRegionValidator, is_valid_bbox_1000
from src.evidence.semantic_support import SemanticSupportVerifier
from src.evidence.numeric_verifier import NumericVerifier
from src.evidence.table_verifier import TableVerifier
from src.evidence.evidence_sufficiency import EvidenceSufficiencyEvaluator


class GroundingClassifier:
    """
    Orchestrates evidence evaluation across spatial, semantic, numeric,
    and sufficiency dimensions into a deterministic grounding outcome.
    """

    def __init__(
        self,
        spatial_validator: Optional[SpatialRegionValidator] = None,
        semantic_verifier: Optional[SemanticSupportVerifier] = None,
        numeric_verifier: Optional[NumericVerifier] = None,
        table_verifier: Optional[TableVerifier] = None,
        sufficiency_evaluator: Optional[EvidenceSufficiencyEvaluator] = None
    ):
        self.spatial_validator = spatial_validator or SpatialRegionValidator()
        self.semantic_verifier = semantic_verifier or SemanticSupportVerifier()
        self.numeric_verifier = numeric_verifier or NumericVerifier()
        self.table_verifier = table_verifier or TableVerifier()
        self.sufficiency_evaluator = sufficiency_evaluator or EvidenceSufficiencyEvaluator()

    def classify_grounding(
        self,
        query_text: str,
        answer_text: str,
        evidence_units: List[EvidenceUnit],
        ground_truth_bboxes: Optional[List[Tuple[int, int, int, int]]] = None
    ) -> Tuple[GroundingResult, EvidenceSupportResult]:
        """
        Execute deterministic 4-state grounding decision tree.
        """
        # Step 1: Check empty evidence
        if not evidence_units:
            g_res = GroundingResult(
                grounding_status="UNSUPPORTED",
                answer_support_status="INSUFFICIENT_EVIDENCE",
                spatial_grounding_status="FAIL",
                evidence_sufficiency_status="INSUFFICIENT",
                grounding_score=0.0,
                evidence_ids=[]
            )
            s_res = EvidenceSupportResult(
                support_status="INSUFFICIENT_EVIDENCE",
                semantic_score=0.0,
                spatial_score=0.0,
                coverage_score=0.0,
                sufficiency_score=0.0,
                reason="No candidate evidence units provided",
                evidence_ids=[]
            )
            return g_res, s_res

        # Step 2: Sufficiency check
        suff_res = self.sufficiency_evaluator.evaluate_sufficiency(query_text, evidence_units)
        suff_status = suff_res["sufficiency_status"]
        cov_score = suff_res["coverage_score"]

        if suff_status == "INSUFFICIENT":
            g_res = GroundingResult(
                grounding_status="UNSUPPORTED",
                answer_support_status="INSUFFICIENT_EVIDENCE",
                spatial_grounding_status="FAIL",
                evidence_sufficiency_status="INSUFFICIENT",
                grounding_score=0.0,
                evidence_ids=[u.evidence_id for u in evidence_units]
            )
            s_res = EvidenceSupportResult(
                support_status="INSUFFICIENT_EVIDENCE",
                semantic_score=0.0,
                spatial_score=0.0,
                coverage_score=cov_score,
                sufficiency_score=cov_score,
                reason="Evidence does not contain sufficient query entities",
                evidence_ids=[u.evidence_id for u in evidence_units]
            )
            return g_res, s_res

        # Step 3: Numeric verification
        combined_text = " ".join(u.text for u in evidence_units)
        num_res = self.numeric_verifier.verify_numeric_support(answer_text, combined_text)
        if num_res["is_numeric_claim"] and not num_res["is_verified"]:
            g_res = GroundingResult(
                grounding_status="UNSUPPORTED",
                answer_support_status="NOT_SUPPORTED",
                spatial_grounding_status="FAIL",
                evidence_sufficiency_status=suff_status,
                grounding_score=0.0,
                evidence_ids=[u.evidence_id for u in evidence_units]
            )
            s_res = EvidenceSupportResult(
                support_status="NOT_SUPPORTED",
                semantic_score=0.0,
                spatial_score=0.0,
                coverage_score=cov_score,
                sufficiency_score=cov_score,
                reason=f"Numeric claim verification failed: {num_res['reason']}",
                evidence_ids=[u.evidence_id for u in evidence_units]
            )
            return g_res, s_res

        # Step 4: Semantic verification across units
        best_sem_score = 0.0
        best_unit_id = None
        contributing_ids = []

        for unit in evidence_units:
            sem_eval = self.semantic_verifier.verify_support(query_text, answer_text, unit.text)
            score = sem_eval["heuristic_support_score"]
            if score > best_sem_score:
                best_sem_score = score
                best_unit_id = unit.evidence_id
            if score >= self.semantic_verifier.min_support_threshold:
                contributing_ids.append(unit.evidence_id)

        if not contributing_ids and best_sem_score < self.semantic_verifier.min_support_threshold:
            # Semantic support failed
            g_res = GroundingResult(
                grounding_status="UNSUPPORTED",
                answer_support_status="NOT_SUPPORTED",
                spatial_grounding_status="FAIL",
                evidence_sufficiency_status=suff_status,
                grounding_score=0.0,
                evidence_ids=[u.evidence_id for u in evidence_units]
            )
            s_res = EvidenceSupportResult(
                support_status="NOT_SUPPORTED",
                semantic_score=best_sem_score,
                spatial_score=0.0,
                coverage_score=cov_score,
                sufficiency_score=cov_score,
                reason="Evidence units do not semantically support the candidate answer",
                evidence_ids=[u.evidence_id for u in evidence_units]
            )
            return g_res, s_res

        if not contributing_ids:
            contributing_ids = [best_unit_id] if best_unit_id else [evidence_units[0].evidence_id]

        # Step 5: Spatial validation
        spatial_score = 1.0
        spatial_status = "PASS"

        if ground_truth_bboxes is not None:
            # Evaluation mode: check max IoU against GT
            best_iou = 0.0
            for unit in evidence_units:
                if unit.evidence_id in contributing_ids:
                    val_out = self.spatial_validator.validate_region(unit.bbox_1000, ground_truth_bboxes)
                    if val_out["max_iou"] > best_iou:
                        best_iou = val_out["max_iou"]
            spatial_score = best_iou
            if best_iou >= self.spatial_validator.iou_threshold_strict:
                spatial_status = "PASS"
            elif best_iou >= self.spatial_validator.iou_threshold_relaxed:
                spatial_status = "PARTIAL"
            else:
                spatial_status = "FAIL"
        else:
            # Runtime zero-leakage mode: check geometric validity of candidate boxes
            all_valid_geom = all(
                is_valid_bbox_1000(u.bbox_1000) for u in evidence_units if u.evidence_id in contributing_ids
            )
            spatial_status = "PASS" if all_valid_geom else "FAIL"
            spatial_score = 1.0 if all_valid_geom else 0.0

        if spatial_status == "FAIL" and ground_truth_bboxes is not None:
            # Spatial grounding failed against ground truth
            g_res = GroundingResult(
                grounding_status="UNSUPPORTED",
                answer_support_status="NOT_SUPPORTED",
                spatial_grounding_status="FAIL",
                evidence_sufficiency_status=suff_status,
                grounding_score=0.0,
                evidence_ids=contributing_ids
            )
            s_res = EvidenceSupportResult(
                support_status="NOT_SUPPORTED",
                semantic_score=best_sem_score,
                spatial_score=spatial_score,
                coverage_score=cov_score,
                sufficiency_score=cov_score,
                reason="Spatial IoU overlap below required threshold",
                evidence_ids=contributing_ids
            )
            return g_res, s_res

        # Step 6: Synthesis
        composite_score = round(
            0.40 * best_sem_score + 0.30 * spatial_score + 0.30 * cov_score, 6
        )

        is_partial = (
            suff_status == "PARTIALLY_SUFFICIENT" or
            spatial_status == "PARTIAL" or
            best_sem_score < 0.85
        )

        if is_partial:
            grounding_status = "PARTIALLY_GROUNDED"
            answer_support_status = "PARTIALLY_SUPPORTED"
            reason = "Answer is partially supported by available evidence"
        else:
            grounding_status = "GROUNDED"
            answer_support_status = "SUPPORTED"
            reason = "Answer is fully grounded and supported by evidence"

        g_res = GroundingResult(
            grounding_status=grounding_status,
            answer_support_status=answer_support_status,
            spatial_grounding_status=spatial_status,
            evidence_sufficiency_status=suff_status,
            grounding_score=composite_score,
            evidence_ids=contributing_ids
        )
        s_res = EvidenceSupportResult(
            support_status=answer_support_status,
            semantic_score=best_sem_score,
            spatial_score=spatial_score,
            coverage_score=cov_score,
            sufficiency_score=cov_score,
            reason=reason,
            evidence_ids=contributing_ids
        )
        return g_res, s_res
