"""tests/test_phase10_5_safety_gate.py
Unit tests for evidence safety verification gate.
"""

from src.recovery.safety_gate import EvidenceSafetyGate
from src.reliability.signals import ObservableSignals


def test_safety_gate_rejection_low_sufficiency():
    gate = EvidenceSafetyGate(min_sufficiency=0.50)
    sig = ObservableSignals(sufficiency_score=0.30, spatial_score=0.60)
    safe, reason = gate.verify_safety(sig)
    assert not safe
    assert "sufficiency" in reason.lower()


def test_safety_gate_rejection_high_numeric_discrepancy():
    gate = EvidenceSafetyGate(max_discrepancy=0.30)
    sig = ObservableSignals(sufficiency_score=0.80, spatial_score=0.70, numeric_discrepancy=0.45)
    safe, reason = gate.verify_safety(sig)
    assert not safe
    assert "numeric discrepancy" in reason.lower()


def test_safety_gate_pass():
    gate = EvidenceSafetyGate()
    sig = ObservableSignals(sufficiency_score=0.75, spatial_score=0.65, numeric_discrepancy=0.05)
    safe, reason = gate.verify_safety(sig)
    assert safe
