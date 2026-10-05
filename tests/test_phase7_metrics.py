"""
Unit tests for Phase 7 Grounding and Verification Metrics.
"""

import pytest
import numpy as np
from src.evidence.metrics import (
    compute_region_recall_at_iou,
    compute_evidence_precision,
    compute_evidence_f1,
    compute_mean_iou,
    categorize_grounding_failure
)


def test_metrics_perfect_overlap():
    gt_boxes = [(100, 100, 300, 300), (400, 400, 600, 600)]
    ret_boxes = [(100, 100, 300, 300), (400, 400, 600, 600)]

    rec50 = compute_region_recall_at_iou(ret_boxes, gt_boxes, 0.50)
    rec75 = compute_region_recall_at_iou(ret_boxes, gt_boxes, 0.75)
    prec = compute_evidence_precision(ret_boxes, gt_boxes, 0.50)
    f1 = compute_evidence_f1(prec, rec50)
    mean_iou = compute_mean_iou(ret_boxes, gt_boxes)

    assert rec50 == 1.0
    assert rec75 == 1.0
    assert prec == 1.0
    assert f1 == 1.0
    assert mean_iou == 1.0


def test_metrics_partial_overlap():
    gt_boxes = [(100, 100, 300, 300)]
    # ret box overlaps with IoU ~ 0.60
    ret_boxes = [(100, 100, 300, 230)]

    rec50 = compute_region_recall_at_iou(ret_boxes, gt_boxes, 0.50)
    rec75 = compute_region_recall_at_iou(ret_boxes, gt_boxes, 0.75)
    assert rec50 == 1.0
    assert rec75 == 0.0


def test_categorize_grounding_failure():
    # Success
    assert categorize_grounding_failure(True, True, True, True, True) == "SUCCESS_GROUNDED"
    # Retrieval miss
    assert categorize_grounding_failure(False, False, False, False, False) == "RETRIEVAL_MISS"
    # Sufficiency failure
    assert categorize_grounding_failure(True, True, True, True, False) == "INSUFFICIENT_EVIDENCE"
    # Numeric failure
    assert categorize_grounding_failure(True, True, True, False, True) == "NUMERIC_MISMATCH"
    # Semantic failure
    assert categorize_grounding_failure(True, True, False, True, True) == "SEMANTIC_SUPPORT_FAILURE"
    # Spatial boundary miss
    assert categorize_grounding_failure(True, False, True, True, True) == "SPATIAL_BOUNDARY_MISS"
