"""
Unit tests for Phase 7 Paired Bootstrap Statistics ($B=10,000$).
"""

import numpy as np
from src.evidence.metrics import paired_bootstrap_test


def test_paired_bootstrap_significant_difference():
    # Model x is consistently higher than baseline y
    rng = np.random.default_rng(42)
    x = rng.normal(loc=0.85, scale=0.05, size=50)
    y = rng.normal(loc=0.60, scale=0.05, size=50)

    res = paired_bootstrap_test(x, y, num_replicates=5000, seed=42)
    assert res["statistically_significant"] is True
    assert res["p_value"] < 0.001
    assert res["ci_95"][0] > 0.0
    assert res["cohens_d"] > 1.5


def test_paired_bootstrap_identical_distribution():
    # Identical arrays
    x = np.ones(50) * 0.75
    y = np.ones(50) * 0.75

    res = paired_bootstrap_test(x, y, num_replicates=2000, seed=42)
    assert res["statistically_significant"] is False
    assert res["observed_mean_diff"] == 0.0
    assert res["p_value"] == 1.0


def test_paired_bootstrap_determinism():
    rng = np.random.default_rng(42)
    x = rng.uniform(0.7, 0.9, size=30)
    y = rng.uniform(0.5, 0.7, size=30)

    res1 = paired_bootstrap_test(x, y, num_replicates=2000, seed=12345)
    res2 = paired_bootstrap_test(x, y, num_replicates=2000, seed=12345)

    assert res1["observed_mean_diff"] == res2["observed_mean_diff"]
    assert res1["p_value"] == res2["p_value"]
    assert res1["ci_95"] == res2["ci_95"]
