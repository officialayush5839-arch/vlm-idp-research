"""
Unit tests for Information Retrieval metrics in Phase 6.
"""

import pytest
from src.retrieval.metrics import (
    compute_recall_at_k,
    compute_hit_at_k,
    compute_mrr,
    compute_ndcg_at_k,
    compute_evidence_region_recall,
    compute_vlm_page_reduction_ratio,
)


def test_recall_at_k():
    retrieved = [1, 2, 3, 4, 5]
    gt = [2, 5]

    # At k=1, retrieved=[1], hits=0
    assert compute_recall_at_k(retrieved, gt, k=1) == 0.0
    # At k=2, retrieved=[1, 2], hits=1 out of 2 -> 0.5
    assert compute_recall_at_k(retrieved, gt, k=2) == 0.5
    # At k=5, retrieved=[1, 2, 3, 4, 5], hits=2 out of 2 -> 1.0
    assert compute_recall_at_k(retrieved, gt, k=5) == 1.0


def test_hit_at_k():
    retrieved = [1, 4, 2]
    gt = [2]
    assert compute_hit_at_k(retrieved, gt, k=1) == 0.0
    assert compute_hit_at_k(retrieved, gt, k=3) == 1.0


def test_mrr():
    retrieved = [10, 20, 30, 40]
    gt = [30]
    # First hit is at rank 3 -> 1/3
    assert pytest.approx(compute_mrr(retrieved, gt), 1e-4) == 1.0 / 3.0

    # No hit within cutoff
    assert compute_mrr(retrieved, [99]) == 0.0


def test_ndcg_at_k():
    retrieved = [1, 2, 3, 4]
    gt = [1]
    # First hit at rank 1 -> perfect ranking
    assert pytest.approx(compute_ndcg_at_k(retrieved, gt, k=4), 1e-4) == 1.0

    retrieved2 = [2, 1, 3, 4]
    # Hit at rank 2
    assert compute_ndcg_at_k(retrieved2, gt, k=4) < 1.0
    assert compute_ndcg_at_k(retrieved2, gt, k=4) > 0.0


def test_evidence_region_recall():
    retrieved_regions = ["reg_1", "reg_2", "reg_5"]
    gt_regions = ["reg_1", "reg_3"]
    # 1 of 2 -> 0.5
    assert compute_evidence_region_recall(retrieved_regions, gt_regions) == 0.5
    assert compute_evidence_region_recall(retrieved_regions, []) == 1.0


def test_vlm_page_reduction_ratio():
    # 3 selected out of 10 -> reduction 1 - 3/10 = 0.70
    assert compute_vlm_page_reduction_ratio(3, 10) == 0.70
    # 5 selected out of 5 -> reduction 0.0
    assert compute_vlm_page_reduction_ratio(5, 5) == 0.0
    # 0 total pages -> 0.0
    assert compute_vlm_page_reduction_ratio(0, 0) == 0.0
