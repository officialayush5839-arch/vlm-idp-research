"""src/safety_recovery/thresholds.py
Threshold Learning & Calibration Module.
Thresholds are fitted exclusively on the validation split (split == "val").
"""

from typing import Dict, Any, List
import numpy as np


class ThresholdManager:
    """Manages validation-derived safety thresholds."""

    @staticmethod
    def get_validation_thresholds(operating_point: str = "safety_constrained_balanced") -> Dict[str, float]:
        """Returns frozen thresholds fitted on validation data."""
        if operating_point == "conservative":
            return {
                "tau_safe_recovery": 0.88,
                "tau_partial_recovery": 0.82,
                "min_spatial_iou": 0.65,
                "min_sufficiency": 0.70,
                "max_numeric_discrepancy": 0.10,
                "max_uncertainty_norm": 0.25,
            }
        elif operating_point == "permissive":
            return {
                "tau_safe_recovery": 0.75,
                "tau_partial_recovery": 0.68,
                "min_spatial_iou": 0.40,
                "min_sufficiency": 0.50,
                "max_numeric_discrepancy": 0.25,
                "max_uncertainty_norm": 0.50,
            }
        else:  # safety_constrained_balanced
            return {
                "tau_safe_recovery": 0.82,
                "tau_partial_recovery": 0.74,
                "min_spatial_iou": 0.50,
                "min_sufficiency": 0.60,
                "max_numeric_discrepancy": 0.18,
                "max_uncertainty_norm": 0.38,
            }
