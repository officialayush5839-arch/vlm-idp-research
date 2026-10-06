"""src/robustness/__init__.py
Phase 10 Robustness, Cross-Domain Generalization & Distribution-Shift Module.
"""

from src.robustness.schema import (
    DomainID,
    ObservableDistributionProfile,
    DistributionShiftMetrics,
    RobustnessEvaluationResult,
)

__all__ = [
    "DomainID",
    "ObservableDistributionProfile",
    "DistributionShiftMetrics",
    "RobustnessEvaluationResult",
]
