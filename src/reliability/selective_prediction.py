"""src/reliability/selective_prediction.py
Selective prediction module for risk-coverage trade-off optimization.
"""

from typing import List, Dict, Any, Tuple
import numpy as np
from src.reliability.risk import RiskCoverageCalculator, RiskCoverageCurve


class SelectivePredictor:
    """Calculates coverage-constrained thresholds and operating points."""

    def __init__(self, target_coverages: Optional[List[float]] = None):
        self.target_coverages = target_coverages or [1.0, 0.95, 0.90, 0.85, 0.80, 0.70, 0.60, 0.50]

    def find_threshold_for_coverage(
        self,
        confidences: List[float],
        target_coverage: float,
    ) -> float:
        """Finds the confidence threshold that yields approximately the target coverage."""
        if not confidences:
            return 0.5
        sorted_conf = sorted(confidences, reverse=True)
        idx = int(np.clip(round(target_coverage * len(sorted_conf)) - 1, 0, len(sorted_conf) - 1))
        return sorted_conf[idx]

    def evaluate_operating_points(
        self,
        confidences: List[float],
        is_correct: List[bool],
    ) -> Dict[float, Dict[str, float]]:
        """Evaluates empirical risk and threshold at each target coverage."""
        results = {}
        curve = RiskCoverageCalculator.compute_curve(confidences, is_correct)
        
        for cov_target in self.target_coverages:
            # Find nearest point in curve
            best_pt = min(curve.points, key=lambda p: abs(p.coverage - cov_target))
            results[cov_target] = {
                "achieved_coverage": round(best_pt.coverage, 4),
                "risk": round(best_pt.risk, 4),
                "threshold": round(best_pt.threshold, 4),
            }
        return results
