"""tests/test_phase10_5_recovery_eligibility.py
Unit tests for deterministic recovery eligibility gate.
"""

from src.recovery.eligibility import RecoveryEligibilityGate
from src.reliability.signals import ObservableSignals


def test_eligibility_severe_dual_destruction():
    gate = RecoveryEligibilityGate()
    sig = ObservableSignals(quality_score=0.10, retrieval_score=0.10)
    eligible, reason = gate.evaluate_eligibility(sig)
    assert not eligible
    assert "irrecoverable" in reason.lower()


def test_eligibility_low_retrieval_margin():
    gate = RecoveryEligibilityGate(min_retrieval_margin=0.25)
    sig = ObservableSignals(quality_score=0.70, retrieval_score=0.15)
    eligible, reason = gate.evaluate_eligibility(sig)
    assert not eligible
    assert "retrieval margin" in reason.lower()


def test_eligibility_valid_sample():
    gate = RecoveryEligibilityGate()
    sig = ObservableSignals(
        quality_score=0.45,
        retrieval_score=0.48,
        sufficiency_score=0.40,
        raw_confidence=0.48,
    )
    eligible, reason = gate.evaluate_eligibility(sig)
    assert eligible
    assert "eligible" in reason.lower()
