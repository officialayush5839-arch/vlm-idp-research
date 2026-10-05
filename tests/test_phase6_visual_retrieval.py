"""
Unit tests for VisualRetriever and layout descriptors.
"""

import numpy as np
from src.retrieval.visual_index import VisualRetriever
from src.retrieval.schema import DocumentPageRecord, DocumentRegionRecord


def test_visual_retriever_layout_concepts():
    pages = [
        DocumentPageRecord(
            document_id="doc_vis_1",
            page_number=1,
            split="test",
            raw_text="Page with large tables and tabular statistics",
            regions=[
                DocumentRegionRecord(
                    region_id="r1",
                    page_number=1,
                    bbox=(100, 100, 900, 900),
                    region_type="table",
                    text_content="Table content"
                )
            ]
        ),
        DocumentPageRecord(
            document_id="doc_vis_1",
            page_number=2,
            split="test",
            raw_text="Standard plain text paragraph",
            regions=[
                DocumentRegionRecord(
                    region_id="r2",
                    page_number=2,
                    bbox=(50, 50, 950, 400),
                    region_type="text",
                    text_content="Text content"
                )
            ]
        )
    ]

    vr = VisualRetriever()
    vr.build(pages)

    results = vr.search_by_text_concept("Find table and grid data", top_k=2)
    assert len(results) == 2
    # Page 1 contains a table region, so should rank higher for table query
    assert results[0].page_number == 1
    assert results[0].visual_score > 0.0


def test_visual_retriever_vector_search():
    pages = [
        DocumentPageRecord(
            document_id="doc_vis_2",
            page_number=1,
            split="test",
            raw_text="Page 1",
        ),
        DocumentPageRecord(
            document_id="doc_vis_2",
            page_number=2,
            split="test",
            raw_text="Page 2",
        )
    ]
    vr = VisualRetriever()
    vr.build(pages)
    query_vec = np.ones(128, dtype=float)
    results = vr.search_by_vector(query_vec, top_k=2)
    assert len(results) == 2
