"""
Unit tests for Dataset Split and Zero-Leakage Invariant Validation.
Verifies that no document or variant leaks across train/val/test partitions.
"""

import pytest
from src.evaluation.reproducibility import SplitLeakageError, validate_dataset_splits


@pytest.mark.splits
class TestSplitValidation:

    def test_clean_split_passes(self):
        """Standard valid split across train, val, and test."""
        records = [
            {"source_document_id": "doc_001", "source_hash": "hash_a", "partition": "train"},
            {"source_document_id": "doc_002", "source_hash": "hash_b", "partition": "val"},
            {"source_document_id": "doc_003", "source_hash": "hash_c", "partition": "test"},
        ]
        valid, summary = validate_dataset_splits(records)
        assert valid is True
        assert summary["total_records"] == 3
        assert summary["partition_counts"]["train"] == 1
        assert summary["partition_counts"]["val"] == 1
        assert summary["partition_counts"]["test"] == 1

    def test_variant_inherits_source_partition(self):
        """Test 2: Corrupted variants must strictly inherit source partition."""
        records = [
            {"source_document_id": "doc_001", "source_hash": "hash_a", "partition": "train"},
            {"source_document_id": "doc_001", "source_hash": "hash_a_blur", "partition": "train"},
            {"source_document_id": "doc_001", "source_hash": "hash_a_noise", "partition": "train"},
            {"source_document_id": "doc_002", "source_hash": "hash_b", "partition": "test"},
            {"source_document_id": "doc_002", "source_hash": "hash_b_jpeg", "partition": "test"},
        ]
        valid, summary = validate_dataset_splits(records)
        assert valid is True
        assert summary["unique_source_documents"] == 2

    def test_leakage_same_source_across_train_test(self):
        """Test 1: Same source document cannot occur across train and test."""
        records = [
            {"source_document_id": "doc_001", "source_hash": "hash_a", "partition": "train"},
            {"source_document_id": "doc_001", "source_hash": "hash_a_blur", "partition": "test"},
        ]
        with pytest.raises(SplitLeakageError, match="DATA LEAKAGE DETECTED"):
            validate_dataset_splits(records)

    def test_identical_hash_crossing_partitions(self):
        """Test 3: Identical source hashes cannot cross partitions."""
        records = [
            {"source_document_id": "doc_alpha", "source_hash": "shared_hash_99", "partition": "train"},
            {"source_document_id": "doc_beta", "source_hash": "shared_hash_99", "partition": "test"},
        ]
        with pytest.raises(SplitLeakageError, match="Source hash .* appears in both"):
            validate_dataset_splits(records)

    def test_missing_partition_fails(self):
        """Test 4: Missing or invalid partition assignment fails validation."""
        records = [
            {"source_document_id": "doc_001", "source_hash": "hash_a", "partition": "invalid_split"}
        ]
        with pytest.raises(SplitLeakageError, match="invalid partition"):
            validate_dataset_splits(records)

    def test_missing_source_identity_fails(self):
        """Test 5: Missing source identity fails validation."""
        records = [
            {"source_hash": "hash_a", "partition": "train"}
        ]
        with pytest.raises(SplitLeakageError, match="missing required source identity"):
            validate_dataset_splits(records)
