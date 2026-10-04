"""
Cryptographic hashing and artifact manifest generation for document ingestion.
Ensures deterministic document identities and complete provenance tracking.
"""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Tuple
from src.ingestion.schema import IngestionManifest


def compute_sha256(file_path_or_bytes: str | Path | bytes) -> str:
    """
    Calculate the cryptographic SHA-256 hash of a file or byte buffer.
    Ensures document identity does not depend on local paths, timestamps, or filenames.
    """
    hasher = hashlib.sha256()

    if isinstance(file_path_or_bytes, bytes):
        hasher.update(file_path_or_bytes)
    else:
        path = Path(file_path_or_bytes)
        if not path.is_file():
            raise FileNotFoundError(f"Source file not found for hashing: {path.resolve()}")
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                hasher.update(chunk)

    return hasher.hexdigest()


def derive_document_id(source_hash_sha256: str, prefix: str = "doc") -> str:
    """
    Derive a deterministic, reproducible document ID from its SHA-256 hash.
    Format: doc_<16_char_hash_prefix>
    """
    return f"{prefix}_{source_hash_sha256[:16]}"


def create_ingestion_manifest(
    document_id: str,
    source_hash_sha256: str,
    source_path: str | Path,
    page_count: int,
    page_hashes: List[str],
    render_dimensions: List[Tuple[int, int]],
    git_commit: str,
    ingestion_version: str = "0.1.0",
) -> IngestionManifest:
    """
    Create an immutable provenance manifest for an ingested document.
    """
    timestamp = datetime.now(timezone.utc).isoformat()
    return IngestionManifest(
        document_id=document_id,
        source_hash_sha256=source_hash_sha256,
        source_path=str(Path(source_path).resolve()),
        page_count=page_count,
        page_hashes=page_hashes,
        render_dimensions=render_dimensions,
        ingestion_version=ingestion_version,
        git_commit=git_commit,
        timestamp_utc=timestamp,
    )
