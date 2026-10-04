"""
Unit tests for cryptographic hashing, document identity derivation, and artifact manifests.
"""

from pathlib import Path
import pytest
from src.ingestion.metadata import (
    compute_sha256,
    create_ingestion_manifest,
    derive_document_id,
)


@pytest.mark.unit
class TestMetadata:

    def test_compute_sha256_bytes(self):
        """SHA-256 of empty bytes is known standard string."""
        empty_hash = compute_sha256(b"")
        assert empty_hash == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"

    def test_compute_sha256_file(self, tmp_path):
        """SHA-256 of a temporary file content."""
        sample_file = tmp_path / "sample.txt"
        sample_file.write_bytes(b"VLM-IDP Research Test String")

        file_hash = compute_sha256(sample_file)
        direct_hash = compute_sha256(b"VLM-IDP Research Test String")

        assert file_hash == direct_hash
        assert len(file_hash) == 64

    def test_derive_document_id(self):
        """Document ID is derived deterministically from first 16 chars of hash."""
        dummy_hash = "abcdef0123456789deadbeef12345678abcdef0123456789deadbeef12345678"
        doc_id = derive_document_id(dummy_hash)
        assert doc_id == "doc_abcdef0123456789"

    def test_create_ingestion_manifest(self, tmp_path):
        """Create valid IngestionManifest with timestamps and dimensions."""
        sample_file = tmp_path / "doc.pdf"
        sample_file.write_bytes(b"%PDF-1.4 mock")

        manifest = create_ingestion_manifest(
            document_id="doc_test123",
            source_hash_sha256="hash123",
            source_path=sample_file,
            page_count=2,
            page_hashes=["p1hash", "p2hash"],
            render_dimensions=[(1000, 1400), (1000, 1400)],
            git_commit="commit_abc123"
        )

        assert manifest.document_id == "doc_test123"
        assert manifest.page_count == 2
        assert len(manifest.page_hashes) == 2
        assert len(manifest.render_dimensions) == 2
        assert manifest.git_commit == "commit_abc123"
