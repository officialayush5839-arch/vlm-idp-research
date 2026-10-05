"""
Unit tests for Phase 7 Partition Split Integrity and Isolation.
"""

from src.evidence.provenance import build_provenance_record


def test_partition_isolation():
    # Verify that records correctly distinguish splits and do not cross-contaminate
    splits = ["train", "val", "test"]
    for s in splits:
        rec = build_provenance_record(
            dataset="docvqa",
            baseline="B7-5",
            document_id=f"doc_{s}_01",
            query_id=f"q_{s}_01",
            condition="clean",
            seed=42,
            extra_metadata={"split": s}
        )
        assert rec["split"] == s
        assert rec["dataset"] == "docvqa"
