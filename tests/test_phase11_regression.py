"""tests/test_phase11_regression.py
Regression tests ensuring upstream Phases 0 through 10.5 remain unaffected.
"""

from src.recovery.pipeline import RecoveryPipeline
from src.robustness.pipeline import RobustnessEvaluationPipeline
from src.reliability.signals import ObservableSignals


def test_phase10_5_recovery_pipeline_unaffected():
    rec_pipeline = RecoveryPipeline()
    sig = ObservableSignals(quality_score=0.90, retrieval_score=0.90, raw_confidence=0.90)
    res = rec_pipeline.evaluate_sample("B10.5-5", sig)
    assert res is not None
    assert res.action.value in ["EMIT_COMPLETE", "EMIT_PARTIAL", "RESTORE_AND_RETRY", "ESCALATE_TO_HUMAN", "ABSTAIN_UNSAFE", "REJECT_IRRECOVERABLE"]


def test_phase10_robustness_pipeline_unaffected():
    rob_pipeline = RobustnessEvaluationPipeline()
    sig = ObservableSignals(quality_score=0.90, retrieval_score=0.90, raw_confidence=0.90)
    res = rob_pipeline.evaluate_sample("B10-4", sig)
    assert res is not None
    assert res.action.value in ["ACCEPT", "ACCEPT_WITH_WARNING", "ESCALATE", "ABSTAIN"]
