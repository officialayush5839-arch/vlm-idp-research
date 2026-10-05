"""
Evidence Package Builder and Serialization Module.
Packages coarse page candidates, fine-grained spatial region evidence,
provenance metadata, and page reduction ratios into standardized JSON structures.
"""

import json
import os
from typing import List, Dict, Any, Optional
from src.retrieval.schema import (
    PageRetrievalResult,
    RegionRetrievalResult,
    EvidencePackage,
    RetrievalQuery
)


class EvidencePackageBuilder:
    """
    Constructs and persists immutable EvidencePackage instances.
    """
    def __init__(self, output_dir: str = "experiments/phase6/evidence"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def build_package(
        self,
        document_id: str,
        query: RetrievalQuery,
        retrieval_method: str,
        total_document_pages: int,
        selected_pages: List[PageRetrievalResult],
        selected_regions: List[RegionRetrievalResult],
        provenance: Dict[str, Any],
        top_k: int = 3,
        top_m: int = 3
    ) -> EvidencePackage:
        """
        Assemble and validate an EvidencePackage.
        """
        n_sel = len(selected_pages)
        reduction_ratio = max(0.0, min(1.0, 1.0 - (float(n_sel) / float(total_document_pages))))

        package_id = f"pkg_{provenance.get('run_id', 'p6')}"

        pkg = EvidencePackage(
            package_id=package_id,
            document_id=document_id,
            query_id=query.query_id,
            retrieval_method=retrieval_method,
            top_k_pages_requested=top_k,
            top_m_regions_requested=top_m,
            total_document_pages=total_document_pages,
            selected_pages=selected_pages,
            selected_regions=selected_regions,
            vlm_page_reduction_ratio=round(reduction_ratio, 6),
            provenance=provenance
        )
        return pkg

    def save_package(self, package: EvidencePackage, filename: Optional[str] = None) -> str:
        """
        Serialize EvidencePackage to JSON file.
        """
        if filename is None:
            filename = f"{package.package_id}.json"
        target_path = os.path.join(self.output_dir, filename)

        with open(target_path, "w", encoding="utf-8") as f:
            f.write(package.model_dump_json(indent=2))

        return target_path
