"""
Unit Tests for Phase 4 Statistical Framework.
Strictly verifies Sections 43, 44, 45, 46, and 48 of the Phase 4 specification.
"""

import numpy as np
from src.benchmark.statistics import (
    compute_cliffs_delta,
    compute_cohens_d,
    evaluate_hypothesis_h1_trend,
    paired_bootstrap_test,
)


def test_paired_bootstrap_test():
    treatment = np.array([0.4, 0.45, 0.5, 0.35, 0.42])
    control = np.array([0.9, 0.95, 0.88, 0.92, 0.91])

    delta_obs, (ci_l, ci_u), p_val = paired_bootstrap_test(
        treatment, control, n_bootstraps=2000, seed=42
    )

    assert delta_obs < -0.40
    assert ci_l < 0.0
    assert ci_u < 0.0
    assert p_val < 0.01  # Significant degradation


def test_cliffs_delta_effect_sizes():
    g1 = np.array([0.2, 0.3, 0.25, 0.35])
    g2 = np.array([0.8, 0.9, 0.85, 0.95])

    d_neg, interp_neg = compute_cliffs_delta(g1, g2)
    assert d_neg == -1.0
    assert interp_neg == "large"

    # Identical distributions -> delta = 0
    d_zero, interp_zero = compute_cliffs_delta(g1, g1)
    assert d_zero == 0.0
    assert interp_zero == "negligible"


def test_cohens_d():
    g1 = np.array([10.0, 11.0, 12.0])
    g2 = np.array([5.0, 6.0, 7.0])
    d = compute_cohens_d(g1, g2)
    assert d > 3.0  # Very large positive shift


def test_eval_hypothesis_h1_trend():
    severities = [0, 1, 2, 3, 4]
    degrading_scores = [0.95, 0.82, 0.65, 0.40, 0.18]

    res = evaluate_hypothesis_h1_trend(severities, degrading_scores)
    assert res["supported"] is True
    assert res["verdict"] == "SUPPORTED"
    assert res["slope"] < -0.15
    assert res["r2"] > 0.95

    # Invariant scores should NOT support H1
    flat_scores = [0.90, 0.89, 0.91, 0.90, 0.89]
    res_flat = evaluate_hypothesis_h1_trend(severities, flat_scores)
    assert res_flat["supported"] is False
    assert res_flat["verdict"] == "NOT_SUPPORTED"
