"""
Unit tests for Phase 6 Retrieval Schemas and Data Models.
"""

import pytest
from pydantic import ValidationError
from src.retrieval.schema import (
    DocumentRegionRecord,
    DocumentPageRecord,
    RetrievalQuery,
    PageRetrievalResult,
    RegionRetrievalResult,
    EvidencePackage,
    RetrievalMetricsResult,
)


def test_document_region_record_valid():
    region = DocumentRegionRecord(
        region_id="reg_001",
        page_number=1,
        bbox=(100, 150, 500, 300),
        region_type="table",
        text_content="Quarterly Revenue Table",
        confidence=0.95
    )
    assert region.region_id == "reg_001"
    assert region.page_number == 1
    assert region.bbox == (100, 150, 500, 300)
    assert region.region_type == "table"


def test_document_region_record_invalid_bbox():
    # Out of [0, 1000] bounds
    with pytest.raises(ValidationError):
        DocumentRegionRecord(
            region_id="reg_bad",
            page_number=1,
            bbox=(0, 0, 1200, 500)
        )

    # Inverted coordinates: xmin > xmax
    with pytest.raises(ValidationError):
        DocumentRegionRecord(
            region_id="reg_bad",
            page_number=1,
            bbox=(600, 100, 400, 500)
        )


def test_document_page_record():
    page = DocumentPageRecord(
        document_id="doc_101",
        page_number=2,
        split="test",
        raw_text="Line 1\nLine 2   multiple spaces",
        quality_score=0.88
    )
    assert page.document_id == "doc_101"
    assert page.clean_text == "Line 1 Line 2 multiple spaces"
    assert page.quality_score == 0.88


def test_retrieval_query_validation():
    query = RetrievalQuery(
        query_id="q_01",
        document_id="doc_101",
        query_text="What was the total operating cost?",
        ground_truth_pages=[3, 1, 3]  # duplicates and unsorted
    )
    assert query.ground_truth_pages == [1, 3]

    with pytest.raises(ValidationError):
        RetrievalQuery(
            query_id="q_empty",
            document_id="doc_101",
            query_text="Where is total?",
            ground_truth_pages=[]
        )


def test_evidence_package_and_page_reduction():
    selected_pages = [
        PageRetrievalResult(page_number=2, score=0.92, text_score=0.90, visual_score=0.85, rank=1),
        PageRetrievalResult(page_number=5, score=0.81, text_score=0.80, visual_score=0.75, rank=2)
    ]
    pkg = EvidencePackage(
        package_id="pkg_test_01",
        document_id="doc_long_01",
        query_id="q_01",
        retrieval_method="B6-5",
        top_k_pages_requested=3,
        top_m_regions_requested=2,
        total_document_pages=10,
        selected_pages=selected_pages,
        vlm_page_reduction_ratio=0.80,  # 1 - 2/10 = 0.80
        provenance={"hash": "abc1234"}
    )
    assert pkg.vlm_page_reduction_ratio == 0.80
    assert len(pkg.selected_pages) == 2


def test_retrieval_metrics_result():
    res = RetrievalMetricsResult(
        method="B6-5",
        dataset="synthetic_multipage",
        degradation_level="clean",
        sample_count=50,
        recall_at_1=0.72,
        recall_at_3=0.88,
        recall_at_5=0.94,
        mrr=0.81,
        ndcg_at_10=0.85,
        page_recall=0.88,
        evidence_region_recall=0.82,
        vlm_page_reduction_ratio=0.70,
        avg_latency_ms=12.4
    )
    assert res.recall_at_3 == 0.88
    assert res.vlm_page_reduction_ratio == 0.70
