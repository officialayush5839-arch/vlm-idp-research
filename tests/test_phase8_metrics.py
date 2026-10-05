import pytest
from src.uncertainty.metrics import (
    compute_calibration_metrics,
    paired_bootstrap_test,
    compute_reliability_bins
)
from src.uncertainty.schema import CalibrationMetricsResult


def test_compute_calibration_metrics_perfect():
    # If confidences match labels perfectly
    confs = [0.05] * 10 + [0.95] * 10
    labels = [0] * 10 + [1] * 10

    metrics = compute_calibration_metrics(confs, labels, n_bins=10, method="test")
    assert isinstance(metrics, CalibrationMetricsResult)
    assert metrics.expected_calibration_error < 0.1
    assert metrics.brier_score < 0.05
    assert metrics.negative_log_likelihood < 0.2


def test_reliability_bins():
    confs = [0.1, 0.2, 0.5, 0.8, 0.9]
    labels = [0, 0, 1, 1, 1]
    bins = compute_reliability_bins(confs, labels, n_bins=5)
    assert len(bins) == 5
    assert "bin_accuracy" in bins[0]
    assert "bin_confidence" in bins[0]
    assert "bin_count" in bins[0]


def test_paired_bootstrap_test():
    # Model A: higher risk (worse), Model B: lower risk (better)
    risks_a = [0.4, 0.5, 0.3, 0.6, 0.4, 0.5, 0.3, 0.4, 0.5, 0.4] * 5
    risks_b = [0.2, 0.1, 0.2, 0.3, 0.1, 0.2, 0.2, 0.1, 0.2, 0.2] * 5

    res = paired_bootstrap_test(risks_a, risks_b, n_bootstraps=1000, seed=42)
    assert "mean_diff" in res
    assert "ci_lower" in res
    assert "ci_upper" in res
    assert "p_value" in res
    assert res["mean_diff"] > 0.0
    assert res["p_value"] < 0.05
