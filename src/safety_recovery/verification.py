"""src/safety_recovery/verification.py
Phase 11 7-Layer Verification Stack.
Certifies observable evidence through 7 sequential safety layers before automated emission.
"""

from typing import Tuple, List, Dict, Any, Optional
from src.reliability.signals import ObservableSignals


class VerificationStack:
    """Enforces 7 verification layers strictly conditioned on observable features."""

    def __init__(
        self,
        min_retrieval_margin: float = 0.25,
        min_spatial_iou: float = 0.50,
        strict_spatial_iou: float = 0.75,
        min_semantic_similarity: float = 0.65,
        max_numeric_discrepancy: float = 0.18,
        min_structural_alignment: float = 0.60,
        min_cross_modal_agreement: float = 0.65,
        tau_safe_confidence: float = 0.82,
    ):
        self.min_retrieval_margin = min_retrieval_margin
        self.min_spatial_iou = min_spatial_iou
        self.strict_spatial_iou = strict_spatial_iou
        self.min_semantic_similarity = min_semantic_similarity
        self.max_numeric_discrepancy = max_numeric_discrepancy
        self.min_structural_alignment = min_structural_alignment
        self.min_cross_modal_agreement = min_cross_modal_agreement
        self.tau_safe_confidence = tau_safe_confidence

    def verify_all_layers(
        self,
        signals: ObservableSignals,
        candidate_answer: str,
    ) -> Tuple[bool, List[str], List[str]]:
        """Evaluates all 7 layers. Returns (all_passed, passed_layers, failed_layers)."""
        passed = []
        failed = []

        # Layer 1: Evidence Existence
        if signals.retrieval_score >= self.min_retrieval_margin:
            passed.append("layer1_evidence_existence")
        else:
            failed.append("layer1_evidence_existence")

        # Layer 2: Spatial Grounding (IoU)
        if signals.spatial_score >= self.min_spatial_iou:
            passed.append("layer2_spatial_grounding")
        else:
            failed.append("layer2_spatial_grounding")

        # Layer 3: Semantic Support
        if signals.semantic_score >= self.min_semantic_similarity:
            passed.append("layer3_semantic_support")
        else:
            failed.append("layer3_semantic_support")

        # Layer 4: Numeric Consistency
        if signals.numeric_discrepancy <= self.max_numeric_discrepancy:
            passed.append("layer4_numeric_consistency")
        else:
            failed.append("layer4_numeric_consistency")

        # Layer 5: Structural / Tabular Consistency
        if signals.table_alignment_score >= self.min_structural_alignment:
            passed.append("layer5_structural_consistency")
        else:
            failed.append("layer5_structural_consistency")

        # Layer 6: Cross-Modal Agreement
        if signals.agreement_score >= self.min_cross_modal_agreement:
            passed.append("layer6_cross_modal_agreement")
        else:
            failed.append("layer6_cross_modal_agreement")

        # Layer 7: Calibrated Confidence Threshold
        if signals.raw_confidence >= self.tau_safe_confidence:
            passed.append("layer7_calibrated_confidence")
        else:
            failed.append("layer7_calibrated_confidence")

        all_passed = (len(failed) == 0)
        return all_passed, passed, failed
