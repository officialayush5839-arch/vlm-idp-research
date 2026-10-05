"""
Pydantic Domain Models and Schemas for Phase 7 Evidence Grounding.
Defines strict schemas for EvidenceUnit, EvidenceSupportResult, GroundingResult,
CitationRecord, and Phase7EvidencePackage.
"""

from typing import List, Dict, Any, Optional, Tuple, Literal
from pydantic import BaseModel, Field, field_validator, model_validator


class EvidenceUnit(BaseModel):
    """
    Fine-grained atomic unit of evidence extracted from a retrieved page/region.
    """
    evidence_id: str = Field(..., description="Unique evidence unit identifier")
    document_id: str = Field(..., description="Parent document identifier")
    page_id: int = Field(..., ge=1, description="1-indexed page number")
    region_id: str = Field(..., description="Region identifier from which evidence originated")
    bbox_1000: Tuple[int, int, int, int] = Field(
        ...,
        description="Bounding box in normalized integer coordinate range [0, 1000]"
    )
    bbox_pixel: Optional[Tuple[int, int, int, int]] = Field(
        default=None,
        description="Optional absolute pixel bounding box"
    )
    text: str = Field(default="", description="Textual content of the evidence snippet")
    entity_type: str = Field(default="text", description="Entity type: text, table, figure, numeric, key_value")
    source_type: Literal["text", "table", "figure", "form", "layout", "multimodal"] = Field(
        default="multimodal",
        description="Source channel from retrieval"
    )
    retrieval_score: float = Field(default=0.0, ge=0.0, description="Upstream retrieval score")
    retrieval_rank: int = Field(default=1, ge=1, description="Rank among candidate evidence units")
    page_rank: int = Field(default=1, ge=1, description="Page rank in retrieval output")
    region_rank: int = Field(default=1, ge=1, description="Region rank within page")
    provenance_hash: str = Field(..., description="Cryptographic SHA-256 fingerprint")

    @field_validator("bbox_1000")
    @classmethod
    def validate_bbox(cls, v: Tuple[int, int, int, int]) -> Tuple[int, int, int, int]:
        xmin, ymin, xmax, ymax = v
        if not (0 <= xmin <= 1000 and 0 <= ymin <= 1000 and 0 <= xmax <= 1000 and 0 <= ymax <= 1000):
            raise ValueError(f"Bbox coordinates must be within [0, 1000]. Got: {v}")
        if xmin > xmax:
            raise ValueError(f"xmin ({xmin}) cannot be greater than xmax ({xmax})")
        if ymin > ymax:
            raise ValueError(f"ymin ({ymin}) cannot be greater than ymax ({ymax})")
        return v


class EvidenceSupportResult(BaseModel):
    """
    Semantic and answer-support evaluation outcome.
    """
    support_status: Literal["SUPPORTED", "PARTIALLY_SUPPORTED", "NOT_SUPPORTED", "INSUFFICIENT_EVIDENCE"] = Field(...)
    semantic_score: float = Field(default=0.0, ge=0.0, le=1.0, description="Heuristic semantic support score")
    spatial_score: float = Field(default=0.0, ge=0.0, le=1.0, description="Spatial IoU overlap score")
    coverage_score: float = Field(default=0.0, ge=0.0, le=1.0, description="Query entity coverage score")
    sufficiency_score: float = Field(default=0.0, ge=0.0, le=1.0, description="Evidence sufficiency score")
    reason: str = Field(default="", description="Detailed qualitative rationale")
    evidence_ids: List[str] = Field(default_factory=list, description="IDs of evidence units contributing to support")


class GroundingResult(BaseModel):
    """
    Composite decision state representing spatial, semantic, and sufficiency grounding.
    """
    grounding_status: Literal["GROUNDED", "PARTIALLY_GROUNDED", "UNSUPPORTED"] = Field(...)
    answer_support_status: Literal["SUPPORTED", "PARTIALLY_SUPPORTED", "NOT_SUPPORTED", "INSUFFICIENT_EVIDENCE"] = Field(...)
    spatial_grounding_status: Literal["PASS", "PARTIAL", "FAIL"] = Field(...)
    evidence_sufficiency_status: Literal["SUFFICIENT", "PARTIALLY_SUFFICIENT", "INSUFFICIENT"] = Field(...)
    grounding_score: float = Field(default=0.0, ge=0.0, le=1.0, description="Composite grounding score")
    evidence_ids: List[str] = Field(default_factory=list)


class CitationRecord(BaseModel):
    """
    Deterministic evidence reference citation for an answered query.
    """
    citation_id: str = Field(..., description="Unique citation identifier")
    document_id: str = Field(...)
    page_number: int = Field(..., ge=1)
    region_id: str = Field(...)
    bbox: Tuple[int, int, int, int]
    evidence_id: str = Field(...)
    provenance_hash: str = Field(...)
    text_snippet: str = Field(default="")


class Phase7EvidencePackage(BaseModel):
    """
    Enriched, self-contained EvidencePackage extending Phase 6 retrieval output
    with complete evidence units, support evaluations, grounding statuses, and citations.
    """
    package_id: str = Field(..., description="Package identifier")
    document_id: str = Field(...)
    query_id: str = Field(...)
    query_text: str = Field(...)
    retrieval_method: str = Field(..., description="Upstream retrieval baseline (e.g. B6-5)")
    selected_pages: List[int] = Field(default_factory=list)
    selected_regions: List[str] = Field(default_factory=list)
    evidence_units: List[EvidenceUnit] = Field(default_factory=list)
    support_result: EvidenceSupportResult = Field(...)
    grounding_result: GroundingResult = Field(...)
    citations: List[CitationRecord] = Field(default_factory=list)
    provenance: Dict[str, Any] = Field(default_factory=dict)
    package_hash: str = Field(..., description="SHA-256 integrity hash")


class GroundingMetricsResult(BaseModel):
    """
    Aggregated grounding evaluation metrics across an experimental partition.
    """
    baseline_id: str
    sample_count: int = Field(..., ge=0)
    evidence_precision: float = Field(default=0.0, ge=0.0, le=1.0)
    evidence_recall: float = Field(default=0.0, ge=0.0, le=1.0)
    evidence_f1: float = Field(default=0.0, ge=0.0, le=1.0)
    region_recall_at_050: float = Field(default=0.0, ge=0.0, le=1.0)
    region_recall_at_075: float = Field(default=0.0, ge=0.0, le=1.0)
    mean_iou: float = Field(default=0.0, ge=0.0, le=1.0)
    semantic_support_accuracy: float = Field(default=0.0, ge=0.0, le=1.0)
    answer_support_accuracy: float = Field(default=0.0, ge=0.0, le=1.0)
    evidence_sufficiency_rate: float = Field(default=0.0, ge=0.0, le=1.0)
    grounded_answer_rate: float = Field(default=0.0, ge=0.0, le=1.0)
    partially_grounded_rate: float = Field(default=0.0, ge=0.0, le=1.0)
    unsupported_answer_rate: float = Field(default=0.0, ge=0.0, le=1.0)
    provenance_integrity_rate: float = Field(default=1.0, ge=0.0, le=1.0)
    trace_completeness: float = Field(default=1.0, ge=0.0, le=1.0)
    citation_validity: float = Field(default=1.0, ge=0.0, le=1.0)
    avg_latency_ms: float = Field(default=0.0, ge=0.0)
