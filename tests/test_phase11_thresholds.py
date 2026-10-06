"""tests/test_phase11_thresholds.py
Unit tests verifying threshold provenance from validation partition.
"""

from src.safety_recovery.thresholds import ThresholdManager


def test_threshold_manager():
    thresh = ThresholdManager.get_validation_thresholds("safety_constrained_balanced")
    assert thresh["tau_safe_recovery"] == 0.82
    assert thresh["min_spatial_iou"] == 0.50
    assert thresh["max_numeric_discrepancy"] == 0.18

    cons = ThresholdManager.get_validation_thresholds("conservative")
    assert cons["tau_safe_recovery"] == 0.88
