"""tests/test_phase11_evidence.py
Unit tests verifying layered evidence existence and spatial verification.
"""

from src.safety_recovery.verification import VerificationStack
from src.reliability.signals import ObservableSignals


def test_evidence_verification_layers():
    stack = VerificationStack(min_spatial_iou=0.50, min_retrieval_margin=0.25)
    sig_pass = ObservableSignals(
        retrieval_score=0.40,
        spatial_score=0.60,
        semantic_score=0.70,
        numeric_discrepancy=0.10,
        table_alignment_score=0.70,
        agreement_score=0.80,
        raw_confidence=0.85,
    )
    all_passed, passed, failed = stack.verify_all_layers(sig_pass, "cand")
    assert all_passed is True
    assert len(failed) == 0

    sig_fail = ObservableSignals(
        retrieval_score=0.10,  # Fails layer 1
        spatial_score=0.30,   # Fails layer 2
        semantic_score=0.70,
        numeric_discrepancy=0.10,
        table_alignment_score=0.70,
        agreement_score=0.80,
        raw_confidence=0.85,
    )
    all_passed, passed, failed = stack.verify_all_layers(sig_fail, "cand")
    assert all_passed is False
    assert "layer1_evidence_existence" in failed
    assert "layer2_spatial_grounding" in failed
