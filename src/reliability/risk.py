"""src/reliability/risk.py
Risk-Coverage curve calculation and selective prediction metrics.
"""

from dataclasses import dataclass
from typing import List, Tuple
import numpy as np


@dataclass
class RiskCoveragePoint:
    coverage: float
    risk: float
    threshold: float


@dataclass
class RiskCoverageCurve:
    points: List[RiskCoveragePoint]
    aurc: float
    e_aurc: float

    def __len__(self):
        return len(self.points)


class RiskCoverageCalculator:
    """Computes empirical risk-coverage curves and Area Under Risk-Coverage (AURC)."""

    @staticmethod
    def compute_curve(
        confidences: List[float],
        is_correct: List[bool],
    ) -> RiskCoverageCurve:
        if not confidences or len(confidences) != len(is_correct):
            return RiskCoverageCurve([], 0.0, 0.0)

        n = len(confidences)
        # Sort by confidence descending
        indices = np.argsort(confidences)[::-1]
        sorted_conf = np.array(confidences)[indices]
        sorted_corr = np.array(is_correct)[indices]

        points = []
        coverages = []
        risks = []

        cumulative_errors = 0
        for i in range(n):
            if not sorted_corr[i]:
                cumulative_errors += 1
            cov = (i + 1) / n
            risk = cumulative_errors / (i + 1)
            thresh = float(sorted_conf[i])
            points.append(RiskCoveragePoint(coverage=cov, risk=risk, threshold=thresh))
            coverages.append(cov)
            risks.append(risk)

        # AURC via trapezoidal rule over coverage
        def _integrate_trapezoid(y, x):
            if hasattr(np, "trapezoid"):
                return float(np.trapezoid(y, x))
            # Manual fallback
            total = 0.0
            for i in range(len(x) - 1):
                dx = x[i + 1] - x[i]
                avg_y = (y[i + 1] + y[i]) / 2.0
                total += dx * avg_y
            return float(total)

        aurc = _integrate_trapezoid(risks, coverages) if len(coverages) > 1 else 0.0

        # Optimal risk (oracle ordering): all correct first, then incorrect
        total_errors = sum(1 for c in is_correct if not c)
        optimal_risks = []
        for i in range(n):
            errors = max(0, (i + 1) - (n - total_errors))
            optimal_risks.append(errors / (i + 1))
        optimal_aurc = _integrate_trapezoid(optimal_risks, coverages) if len(coverages) > 1 else 0.0

        e_aurc = max(0.0, aurc - optimal_aurc)

        return RiskCoverageCurve(points=points, aurc=aurc, e_aurc=e_aurc)
