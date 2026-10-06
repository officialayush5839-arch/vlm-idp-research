"""Unit tests for Phase 10 metrics, statistical tests, and zero leakage."""

import pytest
from pathlib import Path
from src.robustness.robustness_metrics import RobustnessMetricsCalculator
from src.robustness.statistical_tests import RobustnessStatisticalTester
from src.robustness.audit import RobustnessZeroLeakageAuditor

SRC_ROBUSTNESS_DIR = Path("src/robustness")


def test_robustness_metrics_math():
    gap = RobustnessMetricsCalculator.compute_robustness_gap(0.90, 0.75)
    assert pytest.approx(gap, 0.001) == 0.15

    rel = RobustnessMetricsCalculator.compute_relative_degradation(0.90, 0.75)
    assert pytest.approx(rel, 0.001) == 0.1667

    gen_score = RobustnessMetricsCalculator.compute_cross_domain_generalization_score(0.90, [0.85, 0.80, 0.75])
    assert 0.0 <= gen_score <= 1.0


def test_paired_bootstrap_tester():
    scores_a = [0.95, 0.90, 0.85, 0.92, 0.88] * 10
    scores_b = [0.80, 0.75, 0.70, 0.72, 0.68] * 10

    res = RobustnessStatisticalTester.paired_bootstrap_test(scores_a, scores_b, replications=1000, random_seed=42)
    assert res["observed_diff"] > 0
    assert res["p_value"] < 0.05
    assert res["conclusion"] == "SUPPORTED"


def test_zero_leakage_ast_audit_clean():
    violations = RobustnessZeroLeakageAuditor.audit_robustness_package(SRC_ROBUSTNESS_DIR)
    assert len(violations) == 0, f"Found AST violations in src/robustness: {violations}"
