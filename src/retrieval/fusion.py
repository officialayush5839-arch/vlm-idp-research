"""
Multimodal Score Normalization and Fusion Module.
Combines text and visual similarity scores via normalized weighted linear interpolation.
"""

from typing import List, Dict, Optional, Tuple
import numpy as np
from src.retrieval.schema import PageRetrievalResult


def normalize_scores(scores: Dict[int, float], method: str = "min_max") -> Dict[int, float]:
    """
    Normalize raw score dictionary mapping page_number -> score.
    Safely handles edge cases (empty dict, single item, uniform scores).
    """
    if not scores:
        return {}

    pages = list(scores.keys())
    vals = np.array([scores[p] for p in pages], dtype=float)

    if method == "min_max":
        min_v = float(np.min(vals))
        max_v = float(np.max(vals))
        diff = max_v - min_v
        if diff < 1e-8:
            # All values equal
            norm_val = 1.0 if max_v > 0.0 else 0.0
            return {p: norm_val for p in pages}
        norm_vals = (vals - min_v) / diff
        return {p: float(norm_vals[i]) for i, p in enumerate(pages)}

    elif method == "z_score":
        mean_v = float(np.mean(vals))
        std_v = float(np.std(vals))
        if std_v < 1e-8:
            return {p: 0.5 for p in pages}
        # Clip z-scores to [-3, 3] and map to [0, 1]
        z_vals = (vals - mean_v) / std_v
        z_clipped = np.clip(z_vals, -3.0, 3.0)
        norm_vals = (z_clipped + 3.0) / 6.0
        return {p: float(norm_vals[i]) for i, p in enumerate(pages)}

    # Fallback: pass-through with clipping [0, 1]
    return {p: float(np.clip(scores[p], 0.0, 1.0)) for p in pages}


class MultimodalFusion:
    """
    Weighted Multimodal Fusion combining lexical/dense text and visual layout scores.
    """
    def __init__(self, alpha_text: float = 0.60, normalization: str = "min_max"):
        self.alpha_text = float(alpha_text)
        self.alpha_visual = 1.0 - self.alpha_text
        self.normalization = normalization

    def fuse(
        self,
        text_results: List[PageRetrievalResult],
        visual_results: List[PageRetrievalResult],
        top_k: int = 5
    ) -> List[PageRetrievalResult]:
        """
        Merge candidate page results from text and visual retrieval channels.
        """
        raw_text_scores: Dict[int, float] = {}
        raw_visual_scores: Dict[int, float] = {}
        metadata_map: Dict[int, Dict] = {}

        for r in text_results:
            raw_text_scores[r.page_number] = r.score
            metadata_map[r.page_number] = r.metadata

        for r in visual_results:
            raw_visual_scores[r.page_number] = r.score
            if r.page_number not in metadata_map:
                metadata_map[r.page_number] = r.metadata

        all_pages = sorted(list(set(raw_text_scores.keys()) | set(raw_visual_scores.keys())))
        if not all_pages:
            return []

        # Ensure all pages exist in score dicts
        for p in all_pages:
            if p not in raw_text_scores:
                raw_text_scores[p] = 0.0
            if p not in raw_visual_scores:
                raw_visual_scores[p] = 0.0

        norm_text = normalize_scores(raw_text_scores, method=self.normalization)
        norm_vis = normalize_scores(raw_visual_scores, method=self.normalization)

        fused_candidates: List[Tuple[int, float, float, float]] = []
        for p in all_pages:
            s_t = norm_text[p]
            s_v = norm_vis[p]
            s_hybrid = self.alpha_text * s_t + self.alpha_visual * s_v
            fused_candidates.append((p, s_hybrid, s_t, s_v))

        # Sort descending by hybrid score, tie-breaking by text score then page number
        fused_candidates.sort(key=lambda x: (x[1], x[2], -x[0]), reverse=True)

        results: List[PageRetrievalResult] = []
        for rank, (p, s_hyb, s_t, s_v) in enumerate(fused_candidates[:top_k], start=1):
            results.append(
                PageRetrievalResult(
                    page_number=p,
                    score=float(round(s_hyb, 6)),
                    text_score=float(round(s_t, 6)),
                    visual_score=float(round(s_v, 6)),
                    rank=rank,
                    metadata={
                        **metadata_map.get(p, {}),
                        "alpha_text": self.alpha_text,
                        "fusion_method": "weighted_linear"
                    }
                )
            )

        return results
