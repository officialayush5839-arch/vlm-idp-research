"""Audit test suite for metric recomputations and AURC calculations."""

import pytest
from src.reliability.risk import RiskCoverageCalculator
from src.reliability.metrics import ReliabilityMetricsCalculator
from src.reliability.schema import ReliabilityAction


def test_metric_recomputation_exact():
    confs = [0.95, 0.85, 0.75, 0.65]
    preds = ["A", "B", "C", "D"]
    gts = ["A", "B", "W", "X"]
    acts = [
        ReliabilityAction.ACCEPT,
        ReliabilityAction.ACCEPT,
        ReliabilityAction.ABSTAIN,
        ReliabilityAction.ABSTAIN,
    ]

    m = ReliabilityMetricsCalculator.compute(confs, preds, gts, acts)
    assert m["coverage"] == 0.5
    assert m["selective_accuracy"] == 1.0
    assert m["selective_unsupported_rate"] == 0.0
    assert 0.0 <= m["aurc"] <= 1.0


def test_aurc_trapezoid_integration():
    confs = [0.9, 0.8, 0.7, 0.6]
    corrs = [True, True, False, False]
    curve = RiskCoverageCalculator.compute_curve(confs, corrs)
    assert len(curve) == 4
    assert curve.aurc > 0.0
    assert curve.e_aurc >= 0.0
