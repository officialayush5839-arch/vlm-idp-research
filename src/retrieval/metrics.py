"""
Information Retrieval Evaluation Metrics for Phase 6.
Implements Recall@K (K=1, 3, 5, 10, 20), Mean Reciprocal Rank (MRR), nDCG@K,
Evidence Region Recall, and VLM Page Reduction Ratio.
"""

import math
from typing import List, Set, Dict


def compute_recall_at_k(retrieved_pages: List[int], ground_truth_pages: List[int], k: int) -> float:
    """
    Calculate fraction of ground-truth evidence pages retrieved in top-k candidates.
    Recall@K = |Retrieved[:k] ∩ GT| / |GT|
    """
    if not ground_truth_pages:
        return 0.0
    gt_set = set(ground_truth_pages)
    top_k_set = set(retrieved_pages[:k])
    hits = len(top_k_set & gt_set)
    return float(hits) / float(len(gt_set))


def compute_hit_at_k(retrieved_pages: List[int], ground_truth_pages: List[int], k: int) -> float:
    """
    Binary hit indicator: 1.0 if at least one ground-truth page is within top-k.
    """
    if not ground_truth_pages:
        return 0.0
    gt_set = set(ground_truth_pages)
    for p in retrieved_pages[:k]:
        if p in gt_set:
            return 1.0
    return 0.0


def compute_mrr(retrieved_pages: List[int], ground_truth_pages: List[int], cutoff: int = 20) -> float:
    """
    Calculate Reciprocal Rank (1 / rank) of the first ground-truth page found within cutoff.
    """
    if not ground_truth_pages or not retrieved_pages:
        return 0.0
    gt_set = set(ground_truth_pages)
    for rank, p in enumerate(retrieved_pages[:cutoff], start=1):
        if p in gt_set:
            return 1.0 / float(rank)
    return 0.0


def compute_ndcg_at_k(retrieved_pages: List[int], ground_truth_pages: List[int], k: int = 10) -> float:
    """
    Calculate Normalized Discounted Cumulative Gain at cutoff k with binary relevance.
    """
    if not ground_truth_pages or not retrieved_pages:
        return 0.0
    gt_set = set(ground_truth_pages)

    dcg = 0.0
    for i, p in enumerate(retrieved_pages[:k], start=1):
        rel = 1.0 if p in gt_set else 0.0
        dcg += rel / math.log2(i + 1)

    # Ideal DCG
    idcg = 0.0
    ideal_hits = min(k, len(gt_set))
    for i in range(1, ideal_hits + 1):
        idcg += 1.0 / math.log2(i + 1)

    if idcg == 0.0:
        return 0.0
    return float(dcg / idcg)


def compute_evidence_region_recall(retrieved_regions: List[str], ground_truth_regions: List[str]) -> float:
    """
    Calculate recall of target sub-page evidence regions.
    """
    if not ground_truth_regions:
        return 1.0
    gt_set = set(ground_truth_regions)
    hits = len(set(retrieved_regions) & gt_set)
    return float(hits) / float(len(gt_set))


def compute_vlm_page_reduction_ratio(selected_pages_count: int, total_pages_count: int) -> float:
    """
    Calculate VLM Page Reduction Ratio:
    1 - (N_VLM / N_total)
    """
    if total_pages_count <= 0:
        return 0.0
    ratio = 1.0 - (float(selected_pages_count) / float(total_pages_count))
    return float(max(0.0, min(1.0, round(ratio, 6))))
