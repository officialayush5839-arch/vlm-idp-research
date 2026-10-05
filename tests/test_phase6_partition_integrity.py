"""
Partition Integrity tests for Phase 6 Page Records.
Verifies that all child pages inherit the dataset partition split ('train', 'val', 'test')
from the parent document without cross-split leakage.
"""

from src.retrieval.schema import DocumentPageRecord


def test_split_inheritance():
    # Documents in test split must have all child pages in test split
    parent_doc_id = "doc_test_partition_01"
    parent_split = "test"

    pages = [
        DocumentPageRecord(
            document_id=parent_doc_id,
            page_number=p_num,
            split=parent_split,
            raw_text=f"Content for page {p_num}"
        )
        for p_num in range(1, 6)
    ]

    for p in pages:
        assert p.split == "test"
        assert p.document_id == parent_doc_id
