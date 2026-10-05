"""
Evaluation Metrics, Calibration Diagnostics, and Statistical Testing for Phase 8.
Computes ECE, MCE, Brier score, NLL, reliability diagrams, and paired bootstrap tests.
"""

from typing import Dict, Any, List, Tuple, Optional
import math
import numpy as np
from src.uncertainty.schema import CalibrationMetricsResult


def compute_reliability_bins(
    confidences: List[float],
    labels: List[int],
    n_bins: int = 10
) -> List[Dict[str, float]]:
    """
    Partition predictions into uniform confidence bins and compute empirical accuracy and confidence.
    """
    if len(confidences) == 0 or len(labels) == 0:
        return []

    confs = np.asarray(confidences, dtype=float)
    y = np.asarray(labels, dtype=float)
    bin_edges = np.linspace(0.0, 1.0, n_bins + 1)

    bins: List[Dict[str, float]] = []

    for i in range(n_bins):
        low = bin_edges[i]
        high = bin_edges[i + 1]

        if i == 0:
            mask = (confs >= low) & (confs <= high)
        else:
            mask = (confs > low) & (confs <= high)

        count = int(np.sum(mask))
        if count > 0:
            bin_acc = float(np.mean(y[mask]))
            bin_conf = float(np.mean(confs[mask]))
        else:
            bin_acc = 0.0
            bin_conf = float((low + high) / 2.0)

        bins.append({
            "bin_index": i,
            "bin_lower": round(float(low), 4),
            "bin_upper": round(float(high), 4),
            "bin_accuracy": round(float(bin_acc), 4),
            "bin_confidence": round(float(bin_conf), 4),
            "bin_count": count
        })

    return bins


def compute_calibration_metrics(
    confidences: List[float],
    labels: List[int],
    n_bins: int = 10,
    method: str = "uncalibrated"
) -> CalibrationMetricsResult:
    """
    Compute formal calibration metrics: ECE, MCE, Brier Score, NLL, slope, and intercept.
    """
    n = len(confidences)
    if n == 0 or len(labels) == 0:
        return CalibrationMetricsResult(
            method=method,
            sample_count=0,
            expected_calibration_error=0.0,
            maximum_calibration_error=0.0,
            brier_score=0.0,
            negative_log_likelihood=0.0,
            calibration_slope=1.0,
            calibration_intercept=0.0
        )

    confs = np.asarray(confidences, dtype=float)
    y = np.asarray(labels, dtype=float)

    # Brier score
    brier = float(np.mean((confs - y) ** 2))

    # NLL with numerical stability clipping
    eps = 1e-12
    clipped_confs = np.clip(confs, eps, 1.0 - eps)
    nll = -float(np.mean(y * np.log(clipped_confs) + (1.0 - y) * np.log(1.0 - clipped_confs)))

    # Reliability bins & ECE / MCE
    bins = compute_reliability_bins(confidences, labels, n_bins=n_bins)
    ece = 0.0
    mce = 0.0

    for b in bins:
        count = b["bin_count"]
        if count > 0:
            err = abs(b["bin_accuracy"] - b["bin_confidence"])
            ece += (count / n) * err
            if err > mce:
                mce = err

    # Linear calibration slope and intercept
    if np.var(confs) > 1e-7:
        try:
            poly = np.polyfit(confs, y, deg=1)
            slope = float(poly[0])
            intercept = float(poly[1])
        except Exception:
            slope = 1.0
            intercept = 0.0
    else:
        slope = 1.0
        intercept = 0.0

    return CalibrationMetricsResult(
        method=method,
        sample_count=n,
        expected_calibration_error=round(float(ece), 6),
        maximum_calibration_error=round(float(mce), 6),
        brier_score=round(float(brier), 6),
        negative_log_likelihood=round(float(nll), 6),
        calibration_slope=round(float(slope), 4),
        calibration_intercept=round(float(intercept), 4)
    )


def paired_bootstrap_test(
    metric_a: List[float],
    metric_b: List[float],
    n_bootstraps: int = 10000,
    seed: int = 42
) -> Dict[str, Any]:
    """
    Conduct paired bootstrap hypothesis test comparing system A and system B.
    Computes mean difference (A - B), 95% confidence interval, p-value, and Cohen's dz.
    """
    if len(metric_a) != len(metric_b) or len(metric_a) == 0:
        raise ValueError("Metric lists must have identical non-zero length for paired bootstrap")

    diffs = np.asarray(metric_a, dtype=float) - np.asarray(metric_b, dtype=float)
    n = len(diffs)
    observed_mean_diff = float(np.mean(diffs))

    rng = np.random.default_rng(seed)
    boot_indices = rng.integers(0, n, size=(n_bootstraps, n))
    boot_means = np.mean(diffs[boot_indices], axis=1)

    ci_lower = float(np.percentile(boot_means, 2.5))
    ci_upper = float(np.percentile(boot_means, 97.5))

    # Two-sided p-value against null hypothesis (mean diff == 0)
    if observed_mean_diff >= 0:
        p_val = 2.0 * float(np.mean(boot_means <= 0.0))
    else:
        p_val = 2.0 * float(np.mean(boot_means >= 0.0))
    p_val = min(1.0, max(0.0, p_val))

    # Effect size (Cohen's dz)
    diff_std = float(np.std(diffs, ddof=1)) if n > 1 else 0.0
    effect_size = (observed_mean_diff / diff_std) if diff_std > 1e-9 else 0.0

    return {
        "mean_diff": round(observed_mean_diff, 6),
        "ci_lower": round(ci_lower, 6),
        "ci_upper": round(ci_upper, 6),
        "p_value": round(p_val, 6),
        "effect_size_cohen_d": round(effect_size, 4),
        "n_bootstraps": n_bootstraps,
        "sample_size": n
    }
