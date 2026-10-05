"""
Unit tests for MultimodalFusion and score normalization.
"""

from src.retrieval.fusion import MultimodalFusion, normalize_scores
from src.retrieval.schema import PageRetrievalResult


def test_normalize_scores():
    scores = {1: 10.0, 2: 20.0, 3: 0.0}
    norm = normalize_scores(scores, method="min_max")
    assert norm[3] == 0.0
    assert norm[2] == 1.0
    assert norm[1] == 0.5


def test_normalize_scores_uniform():
    scores = {1: 5.0, 2: 5.0}
    norm = normalize_scores(scores, method="min_max")
    assert norm[1] == 1.0
    assert norm[2] == 1.0


def test_multimodal_fusion():
    text_results = [
        PageRetrievalResult(page_number=1, score=10.0, rank=1),
        PageRetrievalResult(page_number=2, score=5.0, rank=2)
    ]
    visual_results = [
        PageRetrievalResult(page_number=2, score=20.0, rank=1),
        PageRetrievalResult(page_number=3, score=15.0, rank=2)
    ]

    fusion = MultimodalFusion(alpha_text=0.60)
    fused = fusion.fuse(text_results, visual_results, top_k=3)

    assert len(fused) == 3
    # All 3 pages (1, 2, 3) must be present in ranked candidates
    fused_page_nums = [r.page_number for r in fused]
    assert set(fused_page_nums) == {1, 2, 3}
    assert fused[0].rank == 1
    assert fused[1].rank == 2
    assert fused[2].rank == 3
