"""
Unit tests for DenseTextRetriever.
"""

from src.retrieval.dense_retrieval import DenseTextRetriever
from src.retrieval.schema import DocumentPageRecord


def test_dense_retriever_ranking():
    pages = [
        DocumentPageRecord(
            document_id="doc_d1",
            page_number=1,
            split="test",
            raw_text="Machine learning neural networks deep learning vision models",
        ),
        DocumentPageRecord(
            document_id="doc_d1",
            page_number=2,
            split="test",
            raw_text="Financial accounting revenue tax expense deductions balance sheet",
        ),
        DocumentPageRecord(
            document_id="doc_d1",
            page_number=3,
            split="test",
            raw_text="Medical clinical pathology patient symptoms diagnosis prescription",
        )
    ]

    retriever = DenseTextRetriever(embedding_dim=16)
    retriever.build(pages)

    results = retriever.search("tax deductions and financial expenses", top_k=2)
    assert len(results) == 2
    assert results[0].page_number == 2
    assert results[0].score > 0.0


def test_dense_retriever_unseen_query():
    pages = [
        DocumentPageRecord(
            document_id="doc_d1",
            page_number=1,
            split="test",
            raw_text="simple hello world",
        )
    ]
    retriever = DenseTextRetriever(embedding_dim=16)
    retriever.build(pages)
    results = retriever.search("completely unknown vocabulary terms xyz123", top_k=1)
    assert len(results) == 1
    assert results[0].score == 0.0
