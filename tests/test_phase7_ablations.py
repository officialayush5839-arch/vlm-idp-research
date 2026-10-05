"""
Unit tests for Phase 7 Grounding Ablations (A1 through A8).
Verifies that disabling individual grounding components produces measurable
and expected behavioral differences.
"""

from src.evidence.pipeline import EvidenceGroundingPipeline
from src.evidence.region_validator import SpatialRegionValidator
from src.evidence.numeric_verifier import NumericVerifier
from src.evidence.table_verifier import TableVerifier
from src.evidence.evidence_sufficiency import EvidenceSufficiencyEvaluator


def test_ablation_a1_no_spatial_grounding():
    # Pipeline without fine-grained spatial validator (accepts any box)
    relaxed_validator = SpatialRegionValidator(iou_threshold_relaxed=0.0, iou_threshold_strict=0.0)
    pipeline = EvidenceGroundingPipeline(spatial_validator=relaxed_validator)

    pkg = pipeline.process(
        document_id="doc_ab1",
        query_id="q_ab1",
        query_text="What is the total?",
        answer_text="$100.00",
        selected_pages=[{"page_number": 1, "clean_text": "Total: $100.00"}],
        selected_regions=[{
            "region_id": "r1",
            "page_number": 1,
            "bbox": (900, 900, 950, 950), # disjoint box
            "snippet": "Total: $100.00",
            "score": 0.9
        }],
        ground_truth_bboxes=[(10, 10, 100, 100)] # far away GT
    )
    # Under relaxed validator with 0.0 threshold, spatial check passes
    assert pkg.grounding_result.spatial_grounding_status == "PASS"


def test_ablation_a2_no_numeric_verifier():
    # Disable numeric verification (mock or pass-through)
    class DummyNumericVerifier(NumericVerifier):
        def verify_numeric_support(self, answer_text, evidence_text, allow_scale_equivalence=True):
            return {"is_numeric_claim": False, "is_verified": True, "matches": [], "reason": "ablation"}

    pipeline = EvidenceGroundingPipeline(numeric_verifier=DummyNumericVerifier())
    pkg = pipeline.process(
        document_id="doc_ab2",
        query_id="q_ab2",
        query_text="What is the net profit?",
        answer_text="$999M", # Fabricated number
        selected_pages=[{"page_number": 1, "clean_text": "Net profit was $10M"}],
        selected_regions=[{
            "region_id": "r1",
            "page_number": 1,
            "bbox": (100, 100, 300, 300),
            "snippet": "Net profit was $10M",
            "score": 0.9
        }],
        ground_truth_bboxes=[(100, 100, 300, 300)]
    )
    # When numeric verification is ablated, the numeric mismatch is ignored
    assert "Numeric claim verification failed" not in pkg.support_result.reason
