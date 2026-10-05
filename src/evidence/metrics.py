"""
Evidence Grounding and Verification Evaluation Metrics for Phase 7.
Implements Evidence Precision, Recall, F1, Region Recall@0.50/0.75,
Mean IoU, Semantic Support Accuracy, Answer Support Accuracy,
Sufficiency Rate, Grounded Answer Rate, and Paired Bootstrap Hypothesis Testing.
"""

import math
import numpy as np
from typing import List, Dict, Any, Tuple, Optional
from src.evidence.region_validator import compute_iou


def compute_region_recall_at_iou(
    retrieved_bboxes: List[Tuple[int, int, int, int]],
    ground_truth_bboxes: List[Tuple[int, int, int, int]],
    iou_threshold: float = 0.50
) -> float:
    """
    Fraction of ground-truth target regions matched with IoU >= iou_threshold.
    """
    if not ground_truth_bboxes:
        return 1.0
    if not retrieved_bboxes:
        return 0.0

    hits = 0
    for gt in ground_truth_bboxes:
        max_iou = max((compute_iou(cand, gt) for cand in retrieved_bboxes), default=0.0)
        if max_iou >= iou_threshold:
            hits += 1

    return round(float(hits) / float(len(ground_truth_bboxes)), 6)


def compute_evidence_precision(
    retrieved_bboxes: List[Tuple[int, int, int, int]],
    ground_truth_bboxes: List[Tuple[int, int, int, int]],
    iou_threshold: float = 0.50
) -> float:
    """
    Fraction of candidate retrieved boxes that overlap any GT box with IoU >= iou_threshold.
    """
    if not retrieved_bboxes:
        return 0.0
    if not ground_truth_bboxes:
        return 0.0

    valid_cands = 0
    for cand in retrieved_bboxes:
        max_iou = max((compute_iou(cand, gt) for gt in ground_truth_bboxes), default=0.0)
        if max_iou >= iou_threshold:
            valid_cands += 1

    return round(float(valid_cands) / float(len(retrieved_bboxes)), 6)


def compute_evidence_f1(precision: float, recall: float) -> float:
    """
    Compute harmonic mean of precision and recall.
    """
    if precision + recall <= 0:
        return 0.0
    return round(2.0 * (precision * recall) / (precision + recall), 6)


def compute_mean_iou(
    retrieved_bboxes: List[Tuple[int, int, int, int]],
    ground_truth_bboxes: List[Tuple[int, int, int, int]]
) -> float:
    """
    Compute mean of maximum IoU for each ground-truth bounding box.
    """
    if not ground_truth_bboxes:
        return 1.0
    if not retrieved_bboxes:
        return 0.0

    ious = []
    for gt in ground_truth_bboxes:
        max_iou = max((compute_iou(cand, gt) for cand in retrieved_bboxes), default=0.0)
        ious.append(max_iou)

    return round(float(np.mean(ious)), 6)


def categorize_grounding_failure(
    retrieved_any: bool,
    spatial_relaxed_pass: bool,
    semantic_pass: bool,
    numeric_pass: bool,
    sufficiency_pass: bool
) -> str:
    """
    Map verification outcomes to standard failure taxonomy.
    """
    if not retrieved_any:
        return "RETRIEVAL_MISS"
    if not sufficiency_pass:
        return "INSUFFICIENT_EVIDENCE"
    if not numeric_pass:
        return "NUMERIC_MISMATCH"
    if not semantic_pass:
        return "SEMANTIC_SUPPORT_FAILURE"
    if not spatial_relaxed_pass:
        return "SPATIAL_BOUNDARY_MISS"
    return "SUCCESS_GROUNDED"


def paired_bootstrap_test(
    x: np.ndarray,
    y: np.ndarray,
    num_replicates: int = 10000,
    seed: int = 42
) -> Dict[str, Any]:
    """
    Perform two-sided paired bootstrap hypothesis test comparing model x vs baseline y.
    """
    rng = np.random.default_rng(seed)
    diffs = np.asarray(x, dtype=float) - np.asarray(y, dtype=float)
    observed_mean = float(np.mean(diffs))
    n = len(diffs)

    boot_means = np.empty(num_replicates, dtype=float)
    for i in range(num_replicates):
        resample = rng.choice(diffs, size=n, replace=True)
        boot_means[i] = np.mean(resample)

    ci_lower = float(np.percentile(boot_means, 2.5))
    ci_upper = float(np.percentile(boot_means, 97.5))

    # Centered for p-value under null hypothesis H0: diff == 0
    centered = boot_means - observed_mean
    p_value = float(np.mean(np.abs(centered) >= np.abs(observed_mean)))

    # Cohen's d
    s_diff = float(np.std(diffs, ddof=1)) if n > 1 else 1.0
    cohens_d = float(observed_mean / s_diff) if s_diff > 1e-8 else 0.0

    return {
        "observed_mean_diff": round(observed_mean, 6),
        "ci_95": [round(ci_lower, 6), round(ci_upper, 6)],
        "p_value": round(p_value, 6),
        "cohens_d": round(cohens_d, 4),
        "statistically_significant": bool(p_value < 0.05 and (ci_lower > 0 or ci_upper < 0))
    }
