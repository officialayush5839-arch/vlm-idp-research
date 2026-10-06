"""tests/test_phase11_gate.py
Unit tests for deterministic safety gate G_safe(x).
"""

from src.safety_recovery.gate import SafetyConstrainedGate
from src.safety_recovery.schema import Phase11State, Phase11Action
from src.reliability.signals import ObservableSignals


def test_safety_gate_emit_complete():
    gate = SafetyConstrainedGate()
    sig = ObservableSignals(
        retrieval_score=0.90,
        spatial_score=0.80,
        semantic_score=0.85,
        numeric_discrepancy=0.05,
        table_alignment_score=0.90,
        agreement_score=0.92,
        raw_confidence=0.94,
    )
    dec = gate.evaluate(sig, "test_answer")
    assert dec.state == Phase11State.S11_0_SAFE_RECOVERED
    assert dec.action == Phase11Action.EMIT_COMPLETE
    assert dec.is_useful is True


def test_safety_gate_escalate_to_human():
    gate = SafetyConstrainedGate()
    sig = ObservableSignals(
        retrieval_score=0.50,
        spatial_score=0.35,  # fails spatial check
        semantic_score=0.50,
        numeric_discrepancy=0.25,
        table_alignment_score=0.50,
        agreement_score=0.60,
        raw_confidence=0.55,
        quality_score=0.45,
    )
    dec = gate.evaluate(sig, "test_answer")
    assert dec.state == Phase11State.S11_3_HUMAN_REVIEW_REQUIRED
    assert dec.action == Phase11Action.ESCALATE_TO_HUMAN
    assert dec.is_useful is False
    assert dec.review_package is not None
