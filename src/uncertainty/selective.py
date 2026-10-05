"""
Selective Prediction Metrics, Risk-Coverage Curve, and AURC for Phase 8.
Evaluates the trade-off between coverage and accuracy under uncertainty-based abstention.
"""

from typing import Dict, Any, List, Tuple, Optional
import math
import numpy as np
from sklearn.metrics import roc_auc_score
from src.uncertainty.schema import SelectivePredictionMetricsResult


def compute_selective_prediction_curve(
    predictions: List[Dict[str, Any]],
    target_coverages: Optional[List[float]] = None,
    method: str = "calibrated"
) -> List[SelectivePredictionMetricsResult]:
    """
    Compute selective prediction metrics across multiple target coverage levels.
    predictions: list of dicts with 'confidence' (float) and 'is_correct' (int: 1 or 0).
    """
    if not predictions:
        return []

    if target_coverages is None:
        target_coverages = [1.0, 0.95, 0.90, 0.80, 0.70, 0.60, 0.50]

    # Sort descending by confidence
    sorted_preds = sorted(predictions, key=lambda p: float(p["confidence"]), reverse=True)
    n_total = len(sorted_preds)

    # Compute overall correctness AUROC
    all_confs = [float(p["confidence"]) for p in sorted_preds]
    all_labels = [int(p.get("is_correct", 0)) for p in sorted_preds]
    if len(set(all_labels)) > 1:
        try:
            auroc_val = float(roc_auc_score(all_labels, all_confs))
        except Exception:
            auroc_val = 0.5
    else:
        auroc_val = 0.5

    # First pass: calculate risks and coverages across points to compute curve-level AURC
    curve_points = []
    for cov in target_coverages:
        if cov >= 1.0:
            k = n_total
            th = 0.0
        elif cov <= 0.0:
            k = 0
            th = 1.0
        else:
            k = min(n_total, max(1, math.ceil(cov * n_total)))
            th = float(sorted_preds[k - 1]["confidence"])

        answered = sorted_preds[:k]
        n_ans = len(answered)
        emp_cov = n_ans / n_total if n_total > 0 else 0.0

        if n_ans > 0:
            correct_count = sum(int(p.get("is_correct", 0)) for p in answered)
            sel_acc = correct_count / n_ans
            sel_risk = 1.0 - sel_acc
        else:
            sel_acc = 0.0
            sel_risk = 0.0

        curve_points.append({
            "target_cov": float(cov),
            "emp_cov": float(emp_cov),
            "sel_acc": float(sel_acc),
            "sel_risk": float(sel_risk),
            "th": float(th),
            "n_ans": n_ans,
            "n_abs": n_total - n_ans
        })

    # Overall risk (at coverage 1.0)
    overall_risk = curve_points[0]["sel_risk"] if curve_points else 0.0
    coverages_for_aurc = [p["emp_cov"] for p in curve_points]
    risks_for_aurc = [p["sel_risk"] for p in curve_points]
    aurc_val, excess_aurc_val = compute_aurc(coverages_for_aurc, risks_for_aurc, overall_risk=overall_risk)

    results: List[SelectivePredictionMetricsResult] = []
    for pt in curve_points:
        results.append(SelectivePredictionMetricsResult(
            method=method,
            target_coverage=round(pt["target_cov"], 4),
            empirical_coverage=round(pt["emp_cov"], 4),
            selective_risk=round(pt["sel_risk"], 4),
            selective_accuracy=round(pt["sel_acc"], 4),
            error_rate_answered=round(pt["sel_risk"], 4),
            abstention_rate=round(1.0 - pt["emp_cov"], 4),
            aurc=aurc_val,
            excess_aurc=excess_aurc_val,
            auroc_correctness=round(auroc_val, 4)
        ))

    return results


def compute_aurc(
    coverages: List[float],
    risks: List[float],
    overall_risk: Optional[float] = None
) -> Tuple[float, float]:
    """
    Compute Area Under Risk-Coverage curve (AURC) using the trapezoidal rule,
    and excess AURC relative to the optimal (oracle) risk-coverage curve.
    coverages: list of empirical coverages
    risks: corresponding selective risks
    """
    if len(coverages) < 2:
        return 0.0, 0.0

    covs = np.asarray(coverages, dtype=float)
    r = np.asarray(risks, dtype=float)

    # Sort by coverage ascending
    idx = np.argsort(covs)
    covs_sorted = covs[idx]
    r_sorted = r[idx]

    eval_covs = list(covs_sorted)
    eval_risks = list(r_sorted)

    if eval_covs[0] > 0.0:
        eval_covs.insert(0, 0.0)
        eval_risks.insert(0, eval_risks[0])
    if eval_covs[-1] < 1.0:
        eval_covs.append(1.0)
        eval_risks.append(eval_risks[-1])

    aurc = float(np.trapezoid(eval_risks, eval_covs))

    if overall_risk is not None and overall_risk > 0.0:
        E = float(overall_risk)
        if E < 1.0:
            optimal_aurc = E + (1.0 - E) * math.log(1.0 - E)
        else:
            optimal_aurc = 1.0
        excess_aurc = max(0.0, aurc - optimal_aurc)
    else:
        excess_aurc = aurc

    return round(float(aurc), 6), round(float(excess_aurc), 6)
