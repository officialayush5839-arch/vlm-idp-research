import pytest
from src.uncertainty.schema import UncertaintyFeatures
from src.uncertainty.baselines import (
    BaselineRegistry,
    A0NoAbstentionBaseline,
    A1RandomAbstentionBaseline,
    A2UncalibratedBaseline,
    A3TemperatureScalingBaseline,
    A4IsotonicBaseline,
    A5EvidenceAwareBaseline
)


def test_baseline_registry_lookup():
    assert "A0_no_abstention" in BaselineRegistry.list_baselines()
    assert "A1_random_abstention" in BaselineRegistry.list_baselines()
    assert "A2_uncalibrated_heuristic" in BaselineRegistry.list_baselines()
    assert "A3_temperature_scaling" in BaselineRegistry.list_baselines()
    assert "A4_isotonic_regression" in BaselineRegistry.list_baselines()
    assert "A5_evidence_aware" in BaselineRegistry.list_baselines()


def test_a0_no_abstention():
    baseline = A0NoAbstentionBaseline()
    feat = UncertaintyFeatures(model_confidence=0.1)
    res = baseline.evaluate_single(confidence=0.1, features=feat, target_coverage=0.8)
    assert res.decision.decision == "ANSWER"
    assert res.decision.threshold == 0.0


def test_a1_random_abstention():
    baseline = A1RandomAbstentionBaseline(seed=42)
    feat = UncertaintyFeatures(model_confidence=0.9)
    # Target coverage 0.0 means always abstain
    res_abs = baseline.evaluate_single(confidence=0.9, features=feat, target_coverage=0.0)
    assert res_abs.decision.decision == "ABSTAIN"
