"""tests/test_phase10_5_statistics.py
Unit tests verifying statistical test infrastructure (paired bootstrap) for H10.5.
"""

import numpy as np


def paired_bootstrap_test(ref_scores, proposed_scores, b_samples=2000, seed=42):
    rng = np.random.RandomState(seed)
    diff = np.array(proposed_scores) - np.array(ref_scores)
    observed_mean_diff = float(np.mean(diff))
    n = len(diff)
    resamples = rng.choice(diff, size=(b_samples, n), replace=True)
    resampled_means = np.mean(resamples, axis=1)
    p_value = float(np.mean(resampled_means <= 0.0))
    return observed_mean_diff, p_value


def test_paired_bootstrap_positive_effect():
    ref = [0.0] * 50
    prop = [1.0] * 35 + [0.0] * 15
    delta, p = paired_bootstrap_test(ref, prop, b_samples=1000)
    assert delta == 0.70
    assert p == 0.0


def test_paired_bootstrap_no_effect():
    ref = [1.0] * 25 + [0.0] * 25
    prop = [1.0] * 25 + [0.0] * 25
    delta, p = paired_bootstrap_test(ref, prop, b_samples=1000)
    assert delta == 0.0
    assert p >= 0.40
