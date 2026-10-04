"""Standardized Data Models and Schemas for Unlimited-OCR (B0-U)."""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class UnlimitedOCRElement(BaseModel):
    """A single layout or text entity with spatial coordinates extracted by Unlimited-OCR."""
    element_id: str
    element_type: str = Field(description="Detected layout type: title, text, table, figure, header, etc.")
    text: str
    normalized_bbox: List[int] = Field(description="Bounding box [x1, y1, x2, y2] in normalized [0, 1000] space")
    raw_bbox: Optional[List[int]] = Field(default=None, description="Bounding box [x1, y1, x2, y2] in pixel space")
    confidence: Optional[float] = None


class UnlimitedOCRParsedOutput(BaseModel):
    """Structured layout and textual decomposition of an Unlimited-OCR document parse."""
    elements: List[UnlimitedOCRElement] = Field(default_factory=list)
    full_transcription: str = ""
    detected_element_counts: Dict[str, int] = Field(default_factory=dict)
    has_spatial_grounding: bool = False


class UnlimitedOCRResult(BaseModel):
    """Standardized Run Artifact Format for B0-U matching Section 23."""
    baseline_id: str = "B0-U"
    engine: str = "Unlimited-OCR"
    model_revision: str
    document_id: str
    page_id: str
    raw_output: str = Field(description="Immutable raw model generation output")
    normalized_text: str = Field(description="Clean normalized plain text or Markdown")
    structured_elements: List[Dict[str, Any]] = Field(default_factory=list)
    bounding_boxes: List[List[int]] = Field(default_factory=list, description="All normalized [0, 1000] bounding boxes")
    confidence: Optional[float] = None
    spatial_evidence_status: str = Field(
        description="'SUPPORTED', 'PARTIALLY_SUPPORTED', 'NOT_SUPPORTED', or 'NOT_AVAILABLE'"
    )
    latency_ms: Optional[float] = None
    gpu_peak_memory_mb: Optional[float] = None
    status: str = "SUCCESS"
    error_type: Optional[str] = None
    error_message: Optional[str] = None
