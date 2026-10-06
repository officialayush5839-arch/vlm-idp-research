"""tests/test_phase10_5_metrics.py
Unit tests verifying Safe Useful Coverage (SUC) and Unsafe Recovery Rate (URR) metrics calculations.
"""

from src.recovery.schema import RecoveryDecision, RecoveryState, RecoveryAction
from src.recovery.metrics import RecoveryMetricsCalculator


def test_metrics_calculation_basic():
    decisions = [
        RecoveryDecision(
            state=RecoveryState.R0_SAFE_COMPLETE,
            action=RecoveryAction.EMIT_COMPLETE,
            confidence=0.9,
            uncertainty_norm=0.1,
            answer_text="a",
            is_useful=True,
            is_safe=True,
        ),
        RecoveryDecision(
            state=RecoveryState.R1_SAFE_PARTIAL,
            action=RecoveryAction.EMIT_PARTIAL,
            confidence=0.8,
            uncertainty_norm=0.2,
            answer_text="b",
            is_useful=True,
            is_safe=True,
        ),
        RecoveryDecision(
            state=RecoveryState.R4_UNSAFE_TO_ANSWER,
            action=RecoveryAction.ABSTAIN_UNSAFE,
            confidence=0.4,
            uncertainty_norm=0.6,
            answer_text=None,
            is_useful=False,
            is_safe=True,
        ),
        RecoveryDecision(
            state=RecoveryState.R2_RECOVERABLE_WITH_RESTORATION,
            action=RecoveryAction.RESTORE_AND_RETRY,
            confidence=0.7,
            uncertainty_norm=0.3,
            answer_text="wrong",
            is_useful=True,
            is_safe=False,
        ),
    ]

    preds = ["a", "b", "", "wrong"]
    gt = ["a", "b", "c", "right"]

    res = RecoveryMetricsCalculator.compute_metrics(decisions, gt, preds)
    assert res["total_samples"] == 4
    assert res["num_useful"] == 3
    assert res["num_safe_useful"] == 2
    assert res["num_unsafe"] == 1
    assert res["safe_useful_coverage"] == 0.50
    assert res["unsafe_recovery_rate"] == 0.25
    assert res["coverage"] == 0.75
