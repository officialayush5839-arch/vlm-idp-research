"""
Document and Page Object Models for VLM-IDP ingestion system.
Provides immutable, typed representations for documents, pages, and bounding boxes.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from pydantic import BaseModel, Field


class BoundingBox(BaseModel):
    """
    Standardized bounding box representation.
    normalized coordinates are in range [0, 1000].
    """
    x0: int = Field(ge=0, le=1000)
    y0: int = Field(ge=0, le=1000)
    x1: int = Field(ge=0, le=1000)
    y1: int = Field(ge=0, le=1000)
    label: Optional[str] = None
    confidence: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    text_content: Optional[str] = None

    @property
    def as_tuple(self) -> Tuple[int, int, int, int]:
        return (self.x0, self.y0, self.x1, self.y1)

    @property
    def area(self) -> int:
        return max(0, self.x1 - self.x0) * max(0, self.y1 - self.y0)


class Page(BaseModel):
    """
    Represents an extracted, rendered page of a document.
    """
    page_id: str
    document_id: str
    page_number: int = Field(ge=1)
    width: int = Field(gt=0, description="Pixel width of rendered image")
    height: int = Field(gt=0, description="Pixel height of rendered image")
    image_path: str
    source_dimensions: Tuple[float, float] = Field(description="Original PDF/image dimensions (pt or px)")
    normalized_dimensions: Tuple[int, int] = (1000, 1000)
    render_dpi: int = 150
    page_hash_sha256: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


class Document(BaseModel):
    """
    Top-level representation of an ingested document artifact.
    Identity is strictly derived from cryptographic SHA-256 of the source artifact.
    """
    document_id: str
    source_path: str
    source_hash_sha256: str
    page_count: int = Field(ge=1)
    pages: List[Page] = Field(default_factory=list)
    dataset_name: Optional[str] = None
    partition: Optional[str] = Field(default=None, description="train, val, or test")
    metadata: Dict[str, Any] = Field(default_factory=dict)


class IngestionManifest(BaseModel):
    """
    Provenance manifest recording complete ingestion details for an artifact.
    """
    document_id: str
    source_hash_sha256: str
    source_path: str
    page_count: int
    page_hashes: List[str]
    render_dimensions: List[Tuple[int, int]]
    ingestion_version: str = "0.1.0"
    git_commit: str
    timestamp_utc: str
