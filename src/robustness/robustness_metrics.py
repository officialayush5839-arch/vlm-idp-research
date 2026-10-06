"""src/robustness/robustness_metrics.py
Calculation of robustness gaps, relative degradations, and cross-domain variance.
"""

from typing import Dict, Any, List
import numpy as np


class RobustnessMetricsCalculator:
    """Computes robustness gap G_m(d) and relative degradation R_m(d)."""

    @staticmethod
    def compute_robustness_gap(in_domain_score: float, shifted_score: float) -> float:
        """G_m(d) = M_m(D_0) - M_m(D_d) (Positive gap indicates performance drop)."""
        return float(in_domain_score - shifted_score)

    @staticmethod
    def compute_relative_degradation(
        in_domain_score: float,
        shifted_score: float,
        epsilon: float = 1e-6,
    ) -> float:
        """R_m(d) = (M_m(D_0) - M_m(D_d)) / max(|M_m(D_0)|, eps)."""
        gap = in_domain_score - shifted_score
        denom = max(abs(in_domain_score), epsilon)
        return float(gap / denom)

    @staticmethod
    def compute_cross_domain_generalization_score(
        in_domain_score: float,
        domain_scores: List[float],
        epsilon: float = 1e-6,
    ) -> float:
        """G = (1 / |D|) * sum(M(D_d) / (M(D_0) + eps))."""
        if not domain_scores:
            return 1.0
        ratios = [s / (in_domain_score + epsilon) for s in domain_scores]
        return float(np.mean(ratios))
