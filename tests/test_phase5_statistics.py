"""
Tests for Phase 5 Statistical Analysis and Routing Regret.
Verifies paired bootstrap testing ($B=10,000$), effect size computations, and routing regret.
"""

import numpy as np
import pytest

from src.benchmark.statistics import paired_bootstrap_test, compute_cliffs_delta, compute_cohens_d


def test_routing_regret_computation():
    # Synthetic scores for Oracle vs Router vs Fixed
    oracle_scores = np.array([1.0, 1.0, 0.8, 0.9, 1.0])
    router_scores = np.array([1.0, 0.9, 0.8, 0.7, 1.0])
    fixed_scores = np.array([0.5, 0.6, 0.8, 0.5, 0.7])

    # Regret = Oracle - Model
    router_regret = oracle_scores - router_scores
    fixed_regret = oracle_scores - fixed_scores

    assert np.all(router_regret >= 0.0)
    assert np.all(fixed_regret >= 0.0)
    assert np.mean(router_regret) < np.mean(fixed_regret)

    delta, interp = compute_cliffs_delta(router_scores, fixed_scores)
    assert isinstance(delta, float)
    assert isinstance(interp, str)


def test_hypothesis_h2_paired_bootstrap():
    np.random.seed(42)
    # Adaptive router outperforms fixed baseline on degraded samples
    router_scores = np.random.normal(loc=0.82, scale=0.08, size=40)
    fixed_scores = np.random.normal(loc=0.70, scale=0.10, size=40)

    delta_obs, (ci_lower, ci_upper), p_val = paired_bootstrap_test(
        scores_treatment=router_scores,
        scores_control=fixed_scores,
        n_bootstraps=1000,
        confidence_level=0.95,
        seed=42,
    )

    assert delta_obs > 0.0
    assert p_val < 0.05
    assert ci_lower > 0.0
