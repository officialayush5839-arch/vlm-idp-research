"""Standardized OCR Schemas for VLM-IDP Phase 2."""

from datetime import datetime, timezone
from typing import List, Optional
from pydantic import BaseModel, Field


class OCRWord(BaseModel):
    """Word-level OCR token representation."""
    word_id: str
    text: str
    confidence: float = Field(ge=0.0, le=1.0)
    raw_bbox: List[int] = Field(description="[x1, y1, x2, y2] in original image pixel coordinates")
    normalized_bbox: List[int] = Field(description="[x1, y1, x2, y2] in normalized [0, 1000] coordinates")


class OCRLine(BaseModel):
    """Line-level OCR structure."""
    line_id: str
    text: str
    confidence: float = Field(ge=0.0, le=1.0)
    raw_bbox: List[int]
    normalized_bbox: List[int]
    words: List[OCRWord] = Field(default_factory=list)


class OCRResult(BaseModel):
    """Standardized OCR Extraction result for a single document page."""
    document_id: str
    page_idx: int
    full_text: str
    confidence: float = Field(ge=0.0, le=1.0)
    lines: List[OCRLine] = Field(default_factory=list)
    engine: str
    engine_version: str
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    latency_ms: Optional[float] = None
