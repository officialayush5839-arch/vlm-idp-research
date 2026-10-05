"""
Fine-Grained Region Retrieval Module.
Identifies relevant sub-page spatial bounding box regions on selected candidate pages.
Coordinates are strictly normalized within [0, 1000].
"""

from typing import List, Dict, Tuple, Optional
from src.retrieval.bm25 import simple_tokenize
from src.retrieval.schema import DocumentPageRecord, DocumentRegionRecord, RegionRetrievalResult, RetrievalQuery


class RegionRetriever:
    """
    Sub-page region retriever executing fine-grained spatial evidence localization.
    """
    def __init__(self):
        pass

    def retrieve_regions(
        self,
        pages: List[DocumentPageRecord],
        query: RetrievalQuery,
        top_m: int = 3
    ) -> List[RegionRetrievalResult]:
        """
        Rank all regions across selected candidate pages by relevance to the query.
        """
        q_tokens = set(simple_tokenize(query.query_text))
        q_lower = query.query_text.lower()
        wants_table = "table" in q_lower or "grid" in q_lower or "total" in q_lower or "row" in q_lower
        wants_figure = "figure" in q_lower or "chart" in q_lower or "graph" in q_lower or "plot" in q_lower

        all_candidate_regions: List[Tuple[DocumentRegionRecord, float]] = []

        for p in pages:
            for reg in p.regions:
                reg_tokens = simple_tokenize(reg.text_content)
                overlap = sum(1 for t in reg_tokens if t in q_tokens)
                lexical_score = overlap / (len(q_tokens) + 1e-6)

                type_bonus = 0.0
                if wants_table and reg.region_type == "table":
                    type_bonus = 0.35
                elif wants_figure and reg.region_type == "figure":
                    type_bonus = 0.35

                # Spatial area normalization
                xmin, ymin, xmax, ymax = reg.bbox
                area_ratio = ((xmax - xmin) * (ymax - ymin)) / 1_000_000.0
                area_bonus = min(0.10, area_ratio * 0.2)

                total_region_score = (0.55 * lexical_score) + type_bonus + area_bonus + (0.10 * reg.confidence)
                all_candidate_regions.append((reg, total_region_score))

        all_candidate_regions.sort(key=lambda x: x[1], reverse=True)

        results: List[RegionRetrievalResult] = []
        for rank, (reg, score) in enumerate(all_candidate_regions[:top_m], start=1):
            results.append(
                RegionRetrievalResult(
                    region_id=reg.region_id,
                    page_number=reg.page_number,
                    bbox=reg.bbox,
                    region_type=reg.region_type,
                    score=float(round(score, 6)),
                    rank=rank,
                    snippet=reg.text_content[:150]
                )
            )

        return results
