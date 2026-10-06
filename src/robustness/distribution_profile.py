"""src/robustness/distribution_profile.py
Extraction of purely observable structural, layout, and visual characteristics.
"""

from typing import List, Dict, Any
import numpy as np
from src.robustness.schema import DomainID, ObservableDistributionProfile


class DistributionProfiler:
    """Profiles document sets based purely on observable characteristics."""

    @staticmethod
    def profile_documents(
        domain_id: DomainID,
        doc_indices: List[Dict[str, Any]],
    ) -> ObservableDistributionProfile:
        if not doc_indices:
            return ObservableDistributionProfile(
                domain_id=domain_id,
                mean_page_count=0.0,
                mean_token_count=0.0,
                mean_text_density=0.0,
                mean_region_density=0.0,
                mean_table_count=0.0,
                mean_whitespace_ratio=0.0,
                mean_visual_quality=1.0,
            )

        page_counts = []
        token_counts = []
        region_counts = []
        qual_scores = []

        for doc in doc_indices:
            pages = doc.get("pages", [])
            page_counts.append(len(pages))
            doc_tokens = sum(len(p.get("raw_text", "").split()) for p in pages)
            token_counts.append(doc_tokens)
            doc_regions = sum(len(p.get("regions", [])) for p in pages)
            region_counts.append(doc_regions)
            doc_quals = [p.get("quality_score", 1.0) for p in pages if "quality_score" in p]
            if doc_quals:
                qual_scores.append(float(np.mean(doc_quals)))
            else:
                qual_scores.append(1.0)

        mean_pages = float(np.mean(page_counts))
        mean_tokens = float(np.mean(token_counts))
        mean_regions = float(np.mean(region_counts))
        mean_qual = float(np.mean(qual_scores))

        # Derived observable density metrics
        text_density = mean_tokens / (mean_pages * 500.0 + 1e-6)
        region_density = mean_regions / (mean_pages + 1e-6)
        whitespace_ratio = max(0.0, min(1.0, 1.0 - text_density * 0.5))

        return ObservableDistributionProfile(
            domain_id=domain_id,
            mean_page_count=round(mean_pages, 2),
            mean_token_count=round(mean_tokens, 2),
            mean_text_density=round(text_density, 4),
            mean_region_density=round(region_density, 4),
            mean_table_count=round(mean_regions * 0.15, 2),
            mean_whitespace_ratio=round(whitespace_ratio, 4),
            mean_visual_quality=round(mean_qual, 4),
        )
