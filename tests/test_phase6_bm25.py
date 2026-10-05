"""
Unit tests for deterministic BM25Okapi and TextIndex.
"""

from src.retrieval.bm25 import BM25Okapi, simple_tokenize
from src.retrieval.text_index import TextIndex
from src.retrieval.schema import DocumentPageRecord


def test_simple_tokenize():
    text = "Total Revenue: $4,500,000 for fiscal year 2024!"
    tokens = simple_tokenize(text)
    assert "total" in tokens
    assert "revenue" in tokens
    assert "2024" in tokens
    assert "4" in tokens


def test_bm25_ranking():
    corpus = [
        ["the", "quick", "brown", "fox"],
        ["net", "profit", "was", "five", "million", "dollars"],
        ["annual", "financial", "report", "with", "balance", "sheet"],
        ["profit", "margin", "and", "net", "revenue", "breakdown"]
    ]
    bm25 = BM25Okapi(corpus)
    query = ["net", "profit"]
    scores = bm25.get_scores(query)

    assert len(scores) == 4
    # Documents 1 and 3 contain net and profit, should rank higher than doc 0
    assert scores[1] > scores[0]
    assert scores[3] > scores[0]

    top_k = bm25.get_top_k(query, k=2)
    top_indices = [idx for idx, s in top_k]
    assert 1 in top_indices or 3 in top_indices


def test_bm25_empty_query():
    corpus = [["page", "one"], ["page", "two"]]
    bm25 = BM25Okapi(corpus)
    scores = bm25.get_scores([])
    assert scores == [0.0, 0.0]


def test_text_index_search():
    pages = [
        DocumentPageRecord(
            document_id="doc_audit_1",
            page_number=1,
            split="test",
            raw_text="Table of Contents and Corporate Directory",
            quality_score=0.9
        ),
        DocumentPageRecord(
            document_id="doc_audit_1",
            page_number=2,
            split="test",
            raw_text="Statement of Cash Flows and Operating Expenses",
            quality_score=0.85
        ),
        DocumentPageRecord(
            document_id="doc_audit_1",
            page_number=3,
            split="test",
            raw_text="Executive Summary and CEO Letter to Shareholders",
            quality_score=0.92
        )
    ]

    index = TextIndex()
    index.build(pages)

    results = index.search("Cash Flows Operating Expenses", top_k=2)
    assert len(results) == 2
    assert results[0].page_number == 2
    assert results[0].score > 0.0
    assert results[0].rank == 1
