"""tests/test_phase10_5_determinism.py
Unit tests verifying determinism across repeated runs given fixed seeds and inputs.
"""

from src.recovery.pipeline import RecoveryPipeline
from src.reliability.signals import ObservableSignals


def test_pipeline_determinism():
    pipeline1 = RecoveryPipeline()
    pipeline2 = RecoveryPipeline()

    sig = ObservableSignals(
        retrieval_score=0.45,
        semantic_score=0.50,
        spatial_score=0.40,
        numeric_discrepancy=0.10,
        table_alignment_score=0.50,
        sufficiency_score=0.45,
        quality_score=0.35,
        agreement_score=0.70,
        raw_confidence=0.45,
    )

    for baseline_id in ["B10.5-0", "B10.5-1", "B10.5-2", "B10.5-3", "B10.5-4", "B10.5-5"]:
        dec1 = pipeline1.evaluate_sample(baseline_id, sig, "test_candidate")
        dec2 = pipeline2.evaluate_sample(baseline_id, sig, "test_candidate")
        assert dec1.state == dec2.state
        assert dec1.action == dec2.action
        assert dec1.confidence == dec2.confidence
        assert dec1.answer_text == dec2.answer_text
        assert dec1.is_useful == dec2.is_useful
