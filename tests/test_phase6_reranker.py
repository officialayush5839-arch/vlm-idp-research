"""
Unit tests for CrossModalReranker.
"""

from src.retrieval.reranker import CrossModalReranker
from src.retrieval.schema import PageRetrievalResult, DocumentPageRecord, DocumentRegionRecord, RetrievalQuery


def test_cross_modal_reranker_bonus():
    candidates = [
        PageRetrievalResult(page_number=1, score=0.60, rank=1),
        PageRetrievalResult(page_number=2, score=0.58, rank=2)
    ]

    # Page 2 has a table matching the query
    pages_map = {
        1: DocumentPageRecord(
            document_id="d1", page_number=1, split="test", raw_text="Overview", regions=[]
        ),
        2: DocumentPageRecord(
            document_id="d1", page_number=2, split="test", raw_text="Table data",
            regions=[
                DocumentRegionRecord(
                    region_id="reg_tbl", page_number=2, bbox=(100, 100, 800, 800),
                    region_type="table", text_content="Revenue Table"
                )
            ]
        )
    }

    query = RetrievalQuery(
        query_id="q1",
        document_id="d1",
        query_text="Find the financial table of profits",
        ground_truth_pages=[2]
    )

    reranker = CrossModalReranker(alignment_weight=0.5, region_density_bonus=0.3)
    reranked = reranker.rerank(candidates, pages_map, query, top_m=2)

    assert len(reranked) == 2
    # Page 2 receives alignment bonus and jumps to rank 1
    assert reranked[0].page_number == 2
    assert reranked[0].rank == 1
