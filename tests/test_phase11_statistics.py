"""tests/test_phase11_statistics.py
Unit tests verifying paired bootstrap testing for Hypothesis H11.
"""

import numpy as np


def paired_bootstrap_h11(ref_suc, prop_suc, b_samples=1000, seed=42):
    rng = np.random.RandomState(seed)
    diff = np.array(prop_suc) - np.array(ref_suc)
    obs_diff = float(np.mean(diff))
    n = len(diff)
    res = rng.choice(diff, size=(b_samples, n), replace=True)
    means = np.mean(res, axis=1)
    p_val = float(np.mean(means <= 0.0))
    return obs_diff, p_val


def test_h11_paired_bootstrap():
    ref = [0.0] * 50
    prop = [1.0] * 40 + [0.0] * 10
    delta, p = paired_bootstrap_h11(ref, prop, b_samples=1000)
    assert delta == 0.80
    assert p == 0.0
