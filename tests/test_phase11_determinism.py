"""tests/test_phase11_determinism.py
Unit tests verifying determinism across repeated executions with identical seeds.
"""

from src.safety_recovery.pipeline import Phase11SafetyPipeline
from src.reliability.signals import ObservableSignals


def test_safety_pipeline_determinism():
    p1 = Phase11SafetyPipeline()
    p2 = Phase11SafetyPipeline()

    sig = ObservableSignals(
        retrieval_score=0.55,
        spatial_score=0.45,
        semantic_score=0.50,
        numeric_discrepancy=0.15,
        table_alignment_score=0.55,
        agreement_score=0.60,
        raw_confidence=0.52,
    )

    for b in ["B11-0", "B11-1", "B11-2", "B11-3", "B11-4", "B11-5", "B11-6"]:
        dec1 = p1.evaluate_sample(b, sig, "test_cand")
        dec2 = p2.evaluate_sample(b, sig, "test_cand")
        assert dec1.state == dec2.state
        assert dec1.action == dec2.action
        assert dec1.confidence == dec2.confidence
        assert dec1.is_useful == dec2.is_useful
