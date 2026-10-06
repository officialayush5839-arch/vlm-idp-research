"""src/reliability/confidence.py
Confidence models for Phase 9:
- C0: Raw Confidence (baseline)
- C1: Weighted Composite Confidence
- C2: Calibrated Composite Confidence
"""

import math
from typing import Dict, Optional
from src.reliability.schema import UncertaintyVector


class RawConfidenceModel:
    """C0 Baseline: Consumes only the raw uncalibrated prediction confidence."""

    def compute(self, raw_confidence: float) -> float:
        return max(0.0, min(1.0, float(raw_confidence)))


class WeightedConfidenceModel:
    """C1: Linear combination of complementary confidence signals (1 - u_i)."""

    def __init__(self, weights: Optional[Dict[str, float]] = None):
        default_weights = {
            "w_retrieval": 0.15,
            "w_semantic": 0.15,
            "w_spatial": 0.15,
            "w_numeric": 0.15,
            "w_table": 0.10,
            "w_sufficiency": 0.15,
            "w_quality": 0.10,
            "w_agreement": 0.05,
        }
        self.weights = weights or default_weights
        # Normalize weights to sum to 1.0
        total = sum(self.weights.values())
        if total > 0:
            self.weights = {k: v / total for k, v in self.weights.items()}

    def compute(self, uncertainty_vector: UncertaintyVector) -> float:
        # Complementary confidence = 1.0 - uncertainty
        conf = (
            self.weights.get("w_retrieval", 0.0) * (1.0 - uncertainty_vector.u_retrieval)
            + self.weights.get("w_semantic", 0.0) * (1.0 - uncertainty_vector.u_semantic)
            + self.weights.get("w_spatial", 0.0) * (1.0 - uncertainty_vector.u_spatial)
            + self.weights.get("w_numeric", 0.0) * (1.0 - uncertainty_vector.u_numeric)
            + self.weights.get("w_table", 0.0) * (1.0 - uncertainty_vector.u_table)
            + self.weights.get("w_sufficiency", 0.0) * (1.0 - uncertainty_vector.u_sufficiency)
            + self.weights.get("w_quality", 0.0) * (1.0 - uncertainty_vector.u_quality)
            + self.weights.get("w_agreement", 0.0) * (1.0 - uncertainty_vector.u_agreement)
        )
        return max(0.0, min(1.0, conf))


class CalibratedCompositeModel:
    """C2 Proposed: Applies post-hoc calibration (e.g. temperature scaling or isotonic) to composite score."""

    def __init__(
        self,
        weights: Optional[Dict[str, float]] = None,
        temperature: float = 1.0,
        isotonic_calibrator: Optional[Any] = None,
    ):
        self.base_model = WeightedConfidenceModel(weights=weights)
        self.temperature = max(1e-4, float(temperature))
        self.isotonic_calibrator = isotonic_calibrator

    def compute(self, uncertainty_vector: UncertaintyVector) -> float:
        raw_comp = self.base_model.compute(uncertainty_vector)

        if self.isotonic_calibrator is not None:
            # Use isotonic calibrator if provided
            return self.isotonic_calibrator.predict([raw_comp])[0]

        # Apply temperature scaling to logit
        eps = 1e-6
        clamped = max(eps, min(1.0 - eps, raw_comp))
        logit = math.log(clamped / (1.0 - clamped))
        scaled_logit = logit / self.temperature
        calibrated = 1.0 / (1.0 + math.exp(-scaled_logit))
        return max(0.0, min(1.0, calibrated))
