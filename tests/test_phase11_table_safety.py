"""tests/test_phase11_table_safety.py
Unit tests verifying Layer 5 tabular structural alignment gating.
"""

from src.safety_recovery.verification import VerificationStack
from src.reliability.signals import ObservableSignals


def test_table_alignment_rejection():
    stack = VerificationStack(min_structural_alignment=0.60)
    sig = ObservableSignals(
        retrieval_score=0.90,
        spatial_score=0.80,
        semantic_score=0.80,
        numeric_discrepancy=0.05,
        table_alignment_score=0.40,  # Row/column misalignment
        agreement_score=0.80,
        raw_confidence=0.85,
    )
    all_passed, passed, failed = stack.verify_all_layers(sig, "cand")
    assert all_passed is False
    assert "layer5_structural_consistency" in failed
