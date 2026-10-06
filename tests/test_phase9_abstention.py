"""Tests for Phase 9 calibration, abstention policies, risk curves, metrics, and failure modes."""

import pytest
from src.reliability.schema import ReliabilityAction, FailureMode, UncertaintyVector
from src.reliability.abstention import AbstentionPolicy
from src.reliability.selective_prediction import SelectivePredictor
from src.reliability.failure_modes import FailureModeClassifier
from src.reliability.risk import RiskCoverageCalculator
from src.reliability.metrics import ReliabilityMetricsCalculator


def test_abstention_policy_decisions():
    policy = AbstentionPolicy(
        tau_accept=0.85,
        tau_warning=0.65,
        tau_escalate=0.45,
        u_max_accept=0.25,
        u_max_warning=0.50,
        u_max_escalate=0.70,
    )

    # High conf, low uncertainty -> ACCEPT
    d1 = policy.evaluate(confidence=0.90, uncertainty_norm=0.15)
    assert d1.action == ReliabilityAction.ACCEPT

    # Moderate conf -> ACCEPT_WITH_WARNING
    d2 = policy.evaluate(confidence=0.75, uncertainty_norm=0.40)
    assert d2.action == ReliabilityAction.ACCEPT_WITH_WARNING

    # Lower conf -> ESCALATE
    d3 = policy.evaluate(confidence=0.50, uncertainty_norm=0.60)
    assert d3.action == ReliabilityAction.ESCALATE

    # Very low conf -> ABSTAIN
    d4 = policy.evaluate(confidence=0.30, uncertainty_norm=0.85)
    assert d4.action == ReliabilityAction.ABSTAIN


def test_failure_mode_classifier():
    classifier = FailureModeClassifier()
    # High visual degradation uncertainty
    vec = UncertaintyVector(0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.85, 0.1)
    res = classifier.diagnose(uncertainty_vector=vec, confidence=0.40)
    assert res.primary_failure == FailureMode.F02_VISUAL_DEGRADATION

    # High numeric discrepancy
    vec_num = UncertaintyVector(0.1, 0.1, 0.1, 0.90, 0.1, 0.1, 0.1, 0.1)
    res_num = classifier.diagnose(uncertainty_vector=vec_num, confidence=0.40)
    assert res_num.primary_failure == FailureMode.F04_NUMERIC_CONFLICT


def test_risk_coverage_calculator():
    confidences = [0.95, 0.90, 0.85, 0.70, 0.40, 0.30]
    is_correct = [True, True, True, False, False, False]
    
    curve = RiskCoverageCalculator.compute_curve(confidences, is_correct)
    assert len(curve) > 0
    assert 0.0 <= curve.aurc <= 1.0


def test_reliability_metrics():
    confidences = [0.9, 0.8, 0.7, 0.4, 0.3]
    predictions = ["A", "B", "C", "D", "E"]
    ground_truth = ["A", "B", "X", "D", "Y"]
    actions = [
        ReliabilityAction.ACCEPT,
        ReliabilityAction.ACCEPT,
        ReliabilityAction.ACCEPT,
        ReliabilityAction.ABSTAIN,
        ReliabilityAction.ABSTAIN,
    ]

    metrics = ReliabilityMetricsCalculator.compute(
        confidences=confidences,
        predictions=predictions,
        ground_truth=ground_truth,
        actions=actions,
    )

    assert "coverage" in metrics
    assert "selective_accuracy" in metrics
    assert metrics["coverage"] == 0.6  # 3 of 5 accepted
    assert pytest.approx(metrics["selective_accuracy"], 0.01) == 0.667  # 2 of 3 correct
