"""
Statistical Analysis Framework for Phase 4 Controlled Degradation Benchmark.
Implements Paired Bootstrap Resampling (B=10,000), Cliff's Delta, Cohen's d, and Hypothesis H1 testing.
Strictly compliant with protocol/statistical_protocol.md.
"""

from __future__ import annotations

import math
from typing import Any, Dict, List, Optional, Tuple, Union
import numpy as np


def paired_bootstrap_test(
    scores_treatment: np.ndarray,
    scores_control: np.ndarray,
    n_bootstraps: int = 10000,
    confidence_level: float = 0.95,
    seed: int = 42,
) -> Tuple[float, Tuple[float, float], float]:
    """
    Non-parametric Paired Bootstrap Resampling per Section 3 of statistical_protocol.md.

    Args:
        scores_treatment: Array of treatment condition scores
        scores_control: Array of paired control condition scores
        n_bootstraps: Number of bootstrap iterations (default 10,000)
        confidence_level: Desired confidence level (default 0.95)
        seed: Random seed for deterministic reproducibility

    Returns:
        (delta_observed, (ci_lower, ci_upper), p_value)
    """
    treatment = np.asarray(scores_treatment, dtype=np.float64)
    control = np.asarray(scores_control, dtype=np.float64)

    if len(treatment) != len(control):
        raise ValueError("Treatment and control scores must have identical lengths for paired testing")

    n = len(treatment)
    if n == 0:
        return 0.0, (0.0, 0.0), 1.0

    delta_observed = float(np.mean(treatment - control))
    paired_deltas = treatment - control

    rng = np.random.default_rng(seed)
    bootstrap_deltas = np.empty(n_bootstraps, dtype=np.float64)

    for b in range(n_bootstraps):
        idx = rng.integers(0, n, size=n)
        bootstrap_deltas[b] = np.mean(paired_deltas[idx])

    alpha = 1.0 - confidence_level
    ci_lower = float(np.percentile(bootstrap_deltas, 100.0 * (alpha / 2.0)))
    ci_upper = float(np.percentile(bootstrap_deltas, 100.0 * (1.0 - alpha / 2.0)))

    # Two-tailed empirical p-value relative to 0
    if delta_observed > 0:
        p_val = float(np.mean(bootstrap_deltas <= 0)) * 2.0
    elif delta_observed < 0:
        p_val = float(np.mean(bootstrap_deltas >= 0)) * 2.0
    else:
        p_val = 1.0

    p_val = float(np.clip(p_val, 0.0, 1.0))
    return delta_observed, (ci_lower, ci_upper), p_val


def compute_cliffs_delta(
    group1: np.ndarray,
    group2: np.ndarray,
) -> Tuple[float, str]:
    """
    Computes Cliff's delta effect size and categorical interpretation.
    delta = #(g1 > g2) - #(g1 < g2) / (N1 * N2)
    """
    g1 = np.asarray(group1, dtype=np.float64)
    g2 = np.asarray(group2, dtype=np.float64)

    n1, n2 = len(g1), len(g2)
    if n1 == 0 or n2 == 0:
        return 0.0, "negligible"

    greater = 0
    less = 0
    for x in g1:
        greater += int(np.sum(x > g2))
        less += int(np.sum(x < g2))

    delta = float((greater - less) / (n1 * n2))
    abs_d = abs(delta)

    if abs_d < 0.147:
        interp = "negligible"
    elif abs_d < 0.330:
        interp = "small"
    elif abs_d < 0.474:
        interp = "medium"
    else:
        interp = "large"

    return delta, interp


def compute_cohens_d(
    group1: np.ndarray,
    group2: np.ndarray,
) -> float:
    """Computes Cohen's d effect size for parametric comparison."""
    g1 = np.asarray(group1, dtype=np.float64)
    g2 = np.asarray(group2, dtype=np.float64)

    n1, n2 = len(g1), len(g2)
    if n1 < 2 or n2 < 2:
        return 0.0

    m1, m2 = np.mean(g1), np.mean(g2)
    v1, v2 = np.var(g1, ddof=1), np.var(g2, ddof=1)
    pooled_sd = math.sqrt(((n1 - 1) * v1 + (n2 - 1) * v2) / (n1 + n2 - 2))

    if pooled_sd <= 1e-9:
        return 0.0

    return float((m1 - m2) / pooled_sd)


def evaluate_hypothesis_h1_trend(
    severity_levels: List[int],
    mean_scores: List[float],
) -> Dict[str, Any]:
    """
    Tests Hypothesis H1:
    H1: Increasing visual degradation significantly reduces VLM/OCR performance.
    Computes linear regression slope beta_rob and checks downward trend.
    """
    x = np.asarray(severity_levels, dtype=np.float64)
    y = np.asarray(mean_scores, dtype=np.float64)

    if len(x) < 2:
        return {"slope": 0.0, "r2": 0.0, "supported": False}

    # Fit linear slope: y = beta * x + alpha
    coeffs = np.polyfit(x, y, 1)
    slope = float(coeffs[0])
    intercept = float(coeffs[1])

    # Compute R^2
    y_pred = slope * x + intercept
    ss_res = np.sum((y - y_pred) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    r2 = float(1.0 - (ss_res / max(1e-9, ss_tot)))

    # H1 is supported if slope is strictly negative and accounts for significant variance
    supported = (slope < -0.05) and (r2 > 0.70)

    return {
        "slope": slope,
        "intercept": intercept,
        "r2": r2,
        "supported": supported,
        "verdict": "SUPPORTED" if supported else "NOT_SUPPORTED",
    }


test_hypothesis_h1_trend = evaluate_hypothesis_h1_trend
