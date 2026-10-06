"""tests/test_phase11_no_leakage.py
Zero-leakage static AST audit and runtime adversarial leakage test suite.
"""

from src.safety_recovery.audit import ZeroLeakageAuditor
from src.safety_recovery.gate import SafetyConstrainedGate
from src.reliability.signals import ObservableSignals


def test_zero_leakage_static_ast():
    violations = ZeroLeakageAuditor.audit_directory("src/safety_recovery")
    assert violations == [], f"Zero-leakage violations detected in src/safety_recovery: {violations}"


def test_zero_leakage_runtime_adversarial():
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
    # Changing candidate answer to adversarial text must NOT change the decision state or action
    dec1 = gate.evaluate(sig, "ground_truth_sentinel_A")
    dec2 = gate.evaluate(sig, "arbitrary_perturbed_sentinel_B")
    assert dec1.state == dec2.state
    assert dec1.action == dec2.action
    assert dec1.confidence == dec2.confidence
