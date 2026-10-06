"""src/recovery/eligibility.py
Deterministic recovery eligibility gate G_recovery(x).
Evaluates observable features exclusively without accessing labels or ground truth.
"""

from typing import Dict, Any, Tuple
from src.reliability.signals import ObservableSignals


class RecoveryEligibilityGate:
    """Evaluates whether an abstained query is eligible for safety recovery."""

    def __init__(
        self,
        min_retrieval_margin: float = 0.20,
        min_ocr_confidence: float = 0.35,
        max_visual_entropy: float = 0.85,
        max_uncertainty_norm: float = 0.90,
    ):
        self.min_retrieval_margin = min_retrieval_margin
        self.min_ocr_confidence = min_ocr_confidence
        self.max_visual_entropy = max_visual_entropy
        self.max_uncertainty_norm = max_uncertainty_norm

    def evaluate_eligibility(self, signals: ObservableSignals) -> Tuple[bool, str]:
        """Returns (is_eligible, reason) based strictly on observable features."""
        # 1. Check if complete visual destruction renders sample irrecoverable
        if signals.quality_score < 0.20 and signals.retrieval_score < 0.20:
            return False, "Severe dual degradation (quality < 0.20 and retrieval < 0.20) renders sample irrecoverable"

        # 2. Check if retrieval score is above minimal floor
        if signals.retrieval_score < self.min_retrieval_margin:
            return False, f"Retrieval margin ({signals.retrieval_score:.3f}) below eligibility cutoff ({self.min_retrieval_margin})"

        # 3. Check sufficiency and agreement bounds
        if signals.sufficiency_score < 0.15 and signals.quality_score < 0.30:
            return False, "Insufficient grounding evidence combined with degraded visual quality"

        return True, "Sample eligible for safety-preserving recovery"
