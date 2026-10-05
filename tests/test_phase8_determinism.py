import pytest
from src.uncertainty.baselines import A1RandomAbstentionBaseline
from src.uncertainty.schema import UncertaintyFeatures
from src.uncertainty.metrics import paired_bootstrap_test


def test_determinism_across_identical_seeds():
    feat = UncertaintyFeatures(model_confidence=0.7)

    # 1. Random baseline determinism
    a1_seed42_run1 = A1RandomAbstentionBaseline(seed=42)
    a1_seed42_run2 = A1RandomAbstentionBaseline(seed=42)

    decisions1 = [a1_seed42_run1.evaluate_single(0.7, feat, target_coverage=0.75).decision.decision for _ in range(20)]
    decisions2 = [a1_seed42_run2.evaluate_single(0.7, feat, target_coverage=0.75).decision.decision for _ in range(20)]

    assert decisions1 == decisions2

    # 2. Bootstrap test determinism
    m_a = [0.4, 0.5, 0.6, 0.3, 0.5] * 5
    m_b = [0.2, 0.3, 0.2, 0.1, 0.3] * 5

    res1 = paired_bootstrap_test(m_a, m_b, n_bootstraps=500, seed=123)
    res2 = paired_bootstrap_test(m_a, m_b, n_bootstraps=500, seed=123)

    assert res1["mean_diff"] == res2["mean_diff"]
    assert res1["ci_lower"] == res2["ci_lower"]
    assert res1["ci_upper"] == res2["ci_upper"]
    assert res1["p_value"] == res2["p_value"]
