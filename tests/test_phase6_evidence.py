"""
Unit tests for EvidencePackageBuilder and RegionRetriever.
"""

import os
import json
from src.retrieval.schema import (
    DocumentPageRecord,
    DocumentRegionRecord,
    RetrievalQuery,
    PageRetrievalResult
)
from src.retrieval.region import RegionRetriever
from src.retrieval.evidence import EvidencePackageBuilder


def test_region_retriever():
    page = DocumentPageRecord(
        document_id="doc_reg_1",
        page_number=1,
        split="test",
        raw_text="Full page text with summary table",
        regions=[
            DocumentRegionRecord(
                region_id="reg_1",
                page_number=1,
                bbox=(50, 50, 950, 300),
                region_type="table",
                text_content="Table 1: Operating Profit and Revenue by Division",
                confidence=0.98
            ),
            DocumentRegionRecord(
                region_id="reg_2",
                page_number=1,
                bbox=(50, 400, 950, 800),
                region_type="text",
                text_content="General narrative remarks by corporate officers",
                confidence=0.90
            )
        ]
    )

    query = RetrievalQuery(
        query_id="q_tbl",
        document_id="doc_reg_1",
        query_text="What was the operating profit table in 2024?",
        ground_truth_pages=[1]
    )

    rr = RegionRetriever()
    regions = rr.retrieve_regions([page], query, top_m=1)
    assert len(regions) == 1
    assert regions[0].region_id == "reg_1"
    assert regions[0].region_type == "table"


def test_evidence_package_builder(tmp_path):
    builder = EvidencePackageBuilder(output_dir=str(tmp_path))
    query = RetrievalQuery(
        query_id="q100",
        document_id="d100",
        query_text="Sample query",
        ground_truth_pages=[2]
    )
    pages = [
        PageRetrievalResult(page_number=2, score=0.95, rank=1)
    ]
    pkg = builder.build_package(
        document_id="d100",
        query=query,
        retrieval_method="B6-5",
        total_document_pages=10,
        selected_pages=pages,
        selected_regions=[],
        provenance={"run_id": "test_run", "git_commit": "3dfa2a2"}
    )

    assert pkg.vlm_page_reduction_ratio == 0.90  # 1 - 1/10
    saved_path = builder.save_package(pkg)
    assert os.path.exists(saved_path)

    with open(saved_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert data["package_id"] == "pkg_test_run"
    assert data["vlm_page_reduction_ratio"] == 0.90
