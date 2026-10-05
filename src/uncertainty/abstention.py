"""
Abstention Policy and Selective Prediction Logic for Phase 8.
Determines whether the system should answer or abstain based on calibrated confidence
and evidence sufficiency, and assigns verification status.
"""

from typing import Dict, Any, List, Optional
import math
from src.uncertainty.schema import UncertaintyFeatures, AbstentionDecision


class AbstentionPolicy:
    """
    Evaluates calibrated confidence and observable signals to make selective abstention decisions.
    Thresholds are strictly calibrated on the validation partition.
    """

    def __init__(self, default_threshold: float = 0.5):
        self.default_threshold = default_threshold
        self.threshold = default_threshold
        self.coverage_thresholds: Dict[float, float] = {}

    def fit_coverage_thresholds(
        self,
        val_confidences: List[float],
        target_coverages: Optional[List[float]] = None
    ) -> Dict[float, float]:
        """
        Fit thresholds corresponding to target empirical coverages on validation confidences.
        """
        if not val_confidences:
            raise ValueError("Cannot fit thresholds on empty validation confidences")

        if target_coverages is None:
            target_coverages = [1.0, 0.95, 0.90, 0.80, 0.70, 0.60, 0.50]

        sorted_confs = sorted(val_confidences, reverse=True)
        n = len(sorted_confs)
        thresholds: Dict[float, float] = {}

        for cov in target_coverages:
            if cov >= 1.0:
                thresholds[1.0] = 0.0
            elif cov <= 0.0:
                thresholds[0.0] = 1.0
            else:
                k = min(n - 1, max(0, math.ceil(cov * n) - 1))
                thresholds[float(cov)] = round(float(sorted_confs[k]), 4)

        self.coverage_thresholds = thresholds
        return thresholds

    def set_threshold(self, threshold: float) -> None:
        self.threshold = float(threshold)

    def decide(
        self,
        confidence: float,
        features: UncertaintyFeatures,
        threshold: Optional[float] = None,
        target_coverage: float = 1.0
    ) -> AbstentionDecision:
        """
        Make an ANSWER or ABSTAIN decision given calibrated confidence and observable features.
        """
        th = threshold if threshold is not None else self.threshold

        margin = round(float(confidence - th), 6)
        is_accepted = confidence >= th

        if is_accepted:
            decision = "ANSWER"
            reason = ""
        else:
            decision = "ABSTAIN"
            if features.sufficiency_status == "INSUFFICIENT":
                reason = "INSUFFICIENT_EVIDENCE"
            elif confidence < 0.40 or features.visual_quality_score < 0.40:
                reason = "LOW_CONFIDENCE_OR_QUALITY"
            else:
                reason = "CONFIDENCE_BELOW_THRESHOLD"

        return AbstentionDecision(
            decision=decision,
            calibrated_confidence=round(float(confidence), 6),
            threshold=round(float(th), 4),
            target_coverage=round(float(target_coverage), 4),
            margin=margin,
            abstention_reason=reason
        )
