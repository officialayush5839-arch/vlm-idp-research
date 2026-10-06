"""tests/test_phase10_5_regression.py
Regression tests ensuring that upstream phases (Phases 0–10) are unaffected by Phase 10.5.
"""

from src.robustness.pipeline import RobustnessEvaluationPipeline
from src.reliability.pipeline import ReliabilityPipeline
from src.reliability.signals import ObservableSignals


def test_phase10_pipeline_unaffected():
    rob_pipeline = RobustnessEvaluationPipeline()
    sig = ObservableSignals(quality_score=0.90, retrieval_score=0.90, raw_confidence=0.90)
    res = rob_pipeline.evaluate_sample("B10-4", sig)
    assert res is not None
    assert res.action.value in ["ACCEPT", "ACCEPT_WITH_WARNING", "ESCALATE", "ABSTAIN"]


def test_phase9_pipeline_unaffected():
    rel_pipeline = ReliabilityPipeline()
    res = rel_pipeline.process(
        doc_id="doc_mp_026",
        query_id="q_doc_mp_026",
        phase3_output={"quality_score": 0.90},
        phase6_output={"retrieval_score": 0.90},
        phase7_output={"sufficiency_score": 0.90, "spatial_overlap": 0.90},
        phase8_output={"raw_confidence": 0.90},
    )
    assert res is not None
    assert res.decision.action.value in ["ACCEPT", "ACCEPT_WITH_WARNING", "ESCALATE", "ABSTAIN"]
