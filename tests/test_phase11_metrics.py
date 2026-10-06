"""tests/test_phase11_metrics.py
Unit tests verifying Phase 11 URR, SUC, and escalation rate calculations.
"""

from src.safety_recovery.schema import SafetyRecoveryDecision, Phase11State, Phase11Action
from src.safety_recovery.metrics import Phase11MetricsCalculator


def test_phase11_metrics_calculation():
    decisions = [
        SafetyRecoveryDecision(
            state=Phase11State.S11_0_SAFE_RECOVERED,
            action=Phase11Action.EMIT_COMPLETE,
            confidence=0.9,
            uncertainty_norm=0.1,
            answer_text="a",
            is_useful=True,
            is_safe=True,
        ),
        SafetyRecoveryDecision(
            state=Phase11State.S11_1_SAFE_PARTIAL,
            action=Phase11Action.EMIT_PARTIAL,
            confidence=0.8,
            uncertainty_norm=0.2,
            answer_text="b",
            is_useful=True,
            is_safe=True,
        ),
        SafetyRecoveryDecision(
            state=Phase11State.S11_3_HUMAN_REVIEW_REQUIRED,
            action=Phase11Action.ESCALATE_TO_HUMAN,
            confidence=0.5,
            uncertainty_norm=0.5,
            answer_text=None,
            is_useful=False,
            is_safe=True,
        ),
        SafetyRecoveryDecision(
            state=Phase11State.S11_0_SAFE_RECOVERED,
            action=Phase11Action.EMIT_COMPLETE,
            confidence=0.85,
            uncertainty_norm=0.15,
            answer_text="wrong",
            is_useful=True,
            is_safe=False,
        ),
    ]

    preds = ["a", "b", "", "wrong"]
    targets = ["a", "b", "c", "right"]

    m = Phase11MetricsCalculator.compute_metrics(decisions, targets, preds)
    assert m["total_samples"] == 4
    assert m["num_emitted"] == 3
    assert m["num_safe_useful"] == 2
    assert m["num_unsafe"] == 1
    assert m["num_escalated"] == 1
    assert m["safe_useful_coverage"] == 0.50
    assert m["unsafe_recovery_rate"] == 0.25
    assert m["human_escalation_rate"] == 0.25
