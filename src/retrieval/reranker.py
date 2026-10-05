"""
Cross-Modal Reranker Module.
Filters and refines top-K candidate pages down to top-M target pages using
lexical-layout alignment, region evidence density, and structural signals.
"""

from typing import List, Dict, Any, Optional
from src.retrieval.schema import PageRetrievalResult, DocumentPageRecord, RetrievalQuery


class CrossModalReranker:
    """
    Reranks page candidates using structural evidence signals and query-layout alignment.
    """
    def __init__(
        self,
        alignment_weight: float = 0.35,
        region_density_bonus: float = 0.15,
        diversity_penalty: float = 0.05
    ):
        self.alignment_weight = alignment_weight
        self.region_density_bonus = region_density_bonus
        self.diversity_penalty = diversity_penalty

    def rerank(
        self,
        candidates: List[PageRetrievalResult],
        pages_map: Dict[int, DocumentPageRecord],
        query: RetrievalQuery,
        top_m: int = 3
    ) -> List[PageRetrievalResult]:
        """
        Rerank candidate list down to top_m selected pages.
        """
        if not candidates:
            return []

        scored_candidates = []
        q_lower = query.query_text.lower()
        needs_table = "table" in q_lower or "grid" in q_lower or "total" in q_lower
        needs_figure = "figure" in q_lower or "chart" in q_lower or "graph" in q_lower

        selected_pages_so_far: List[int] = []

        for cand in candidates:
            p_rec = pages_map.get(cand.page_number)
            bonus = 0.0

            if p_rec:
                # Region density bonus
                if p_rec.regions:
                    bonus += min(0.10, len(p_rec.regions) * 0.02)

                # Query-layout alignment
                for reg in p_rec.regions:
                    if needs_table and reg.region_type == "table":
                        bonus += self.region_density_bonus
                        break
                    if needs_figure and reg.region_type == "figure":
                        bonus += self.region_density_bonus
                        break

            # Diversity check: slight penalty if immediately adjacent to already top-selected page
            penalty = 0.0
            if selected_pages_so_far and any(abs(cand.page_number - sp) == 1 for sp in selected_pages_so_far):
                penalty += self.diversity_penalty

            rerank_score = cand.score + (self.alignment_weight * bonus) - penalty
            scored_candidates.append((cand, max(0.0, rerank_score)))

        # Sort descending by rerank_score
        scored_candidates.sort(key=lambda x: x[1], reverse=True)

        results: List[PageRetrievalResult] = []
        for rank, (cand, final_s) in enumerate(scored_candidates[:top_m], start=1):
            results.append(
                PageRetrievalResult(
                    page_number=cand.page_number,
                    score=float(round(final_s, 6)),
                    text_score=cand.text_score,
                    visual_score=cand.visual_score,
                    rank=rank,
                    metadata={
                        **cand.metadata,
                        "initial_rank": cand.rank,
                        "reranked": True
                    }
                )
            )
            selected_pages_so_far.append(cand.page_number)

        return results
