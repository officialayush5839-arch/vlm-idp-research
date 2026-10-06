"""tests/test_phase11_numeric_safety.py
Unit tests verifying Layer 4 numeric consistency gating.
"""

from src.safety_recovery.verification import VerificationStack
from src.reliability.signals import ObservableSignals


def test_numeric_discrepancy_rejection():
    stack = VerificationStack(max_numeric_discrepancy=0.18)
    sig = ObservableSignals(
        retrieval_score=0.90,
        spatial_score=0.80,
        semantic_score=0.80,
        numeric_discrepancy=0.35,  # Numeric mismatch
        table_alignment_score=0.80,
        agreement_score=0.80,
        raw_confidence=0.85,
    )
    all_passed, passed, failed = stack.verify_all_layers(sig, "$125.00")
    assert all_passed is False
    assert "layer4_numeric_consistency" in failed
