"""
Multi-Page Evidence Aggregation Module for Phase 7 Evidence Grounding.
Fuses evidence units distributed across multiple pages into a coherent,
provenance-tracked evidence representation.
"""

from typing import List, Dict, Any, Set
from collections import defaultdict
import math
from src.evidence.schema import EvidenceUnit


class MultiPageAggregator:
    """
    Aggregates and organizes evidence units across distinct document pages.
    """

    def aggregate_evidence(
        self,
        evidence_units: List[EvidenceUnit]
    ) -> Dict[str, Any]:
        """
        Aggregate evidence units, group by page, and calculate multi-page dispersion metrics.
        """
        if not evidence_units:
            return {
                "page_count": 0,
                "distinct_pages": [],
                "units_by_page": {},
                "combined_text": "",
                "cross_page_score": 0.0,
                "primary_page": None
            }

        units_by_page: Dict[int, List[EvidenceUnit]] = defaultdict(list)
        for u in evidence_units:
            units_by_page[u.page_id].append(u)

        distinct_pages = sorted(units_by_page.keys())
        total_units = len(evidence_units)

        # Primary page is page with highest retrieval score / most units
        page_weights = {
            p: sum(u.retrieval_score for u in units) for p, units in units_by_page.items()
        }
        primary_page = max(page_weights.keys(), key=lambda p: page_weights[p])

        # Concatenate text respecting page order
        page_snippets = []
        for p in distinct_pages:
            page_text = " ".join(u.text.strip() for u in units_by_page[p] if u.text.strip())
            if page_text:
                page_snippets.append(f"[Page {p}] {page_text}")
        combined_text = "\n".join(page_snippets)

        # Cross-page dispersion metric (normalized Shannon entropy)
        if len(distinct_pages) > 1:
            entropy = -sum(
                (len(u_list) / total_units) * math.log2(len(u_list) / total_units)
                for u_list in units_by_page.values()
            )
            max_entropy = math.log2(len(distinct_pages))
            cross_page_score = round(entropy / max_entropy, 6) if max_entropy > 0 else 0.0
        else:
            cross_page_score = 0.0

        return {
            "page_count": len(distinct_pages),
            "distinct_pages": distinct_pages,
            "units_by_page": {p: [u.evidence_id for u in u_list] for p, u_list in units_by_page.items()},
            "combined_text": combined_text,
            "cross_page_score": cross_page_score,
            "primary_page": primary_page
        }
