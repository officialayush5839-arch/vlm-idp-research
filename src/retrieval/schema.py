"""
Pydantic Schemas for Phase 6 Long-Document Multimodal Retrieval.
Provides standardized validation, serialization, and provenance for documents,
pages, regions, queries, retrieval results, and evidence packages.
"""

from typing import List, Dict, Any, Optional, Tuple, Literal
from pydantic import BaseModel, Field, field_validator, model_validator


class DocumentRegionRecord(BaseModel):
    """
    Sub-page spatial region record with normalized bounding box coordinates [0, 1000].
    """
    region_id: str = Field(..., description="Unique region identifier within the document/page")
    page_number: int = Field(..., ge=1, description="1-indexed document page number")
    bbox: Tuple[int, int, int, int] = Field(
        ...,
        description="Normalized coordinates (x_min, y_min, x_max, y_max) in integer range [0, 1000]"
    )
    region_type: Literal["text", "table", "figure", "form", "header", "footer", "mixed"] = Field(
        default="text",
        description="Semantic region classification"
    )
    text_content: str = Field(default="", description="Extracted OCR or layout text for this region")
    confidence: float = Field(default=1.0, ge=0.0, le=1.0, description="Extraction or detection confidence")

    @field_validator("bbox")
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


class DocumentPageRecord(BaseModel):
    """
    Page-level representation containing extracted text, spatial layout regions, and quality indicators.
    """
    document_id: str = Field(..., description="Parent document identifier")
    page_number: int = Field(..., ge=1, description="1-indexed page number")
    split: Literal["train", "val", "test"] = Field(..., description="Inherited partition split")
    raw_text: str = Field(default="", description="Raw OCR or text extracted from page")
    clean_text: str = Field(default="", description="Normalized cleaned text token stream")
    image_path: Optional[str] = Field(default=None, description="Optional path to page rendered image")
    regions: List[DocumentRegionRecord] = Field(default_factory=list, description="Extracted sub-page regions")
    quality_score: float = Field(default=1.0, ge=0.0, le=1.0, description="Phase 3 quality score")
    degradation_level: str = Field(default="clean", description="Observed or injected degradation condition")

    @model_validator(mode="after")
    def compute_clean_text(self):
        if not self.clean_text and self.raw_text:
            self.clean_text = " ".join(self.raw_text.split())
        elif self.clean_text:
            self.clean_text = " ".join(self.clean_text.split())
        return self


class RetrievalQuery(BaseModel):
    """
    Evaluation or runtime retrieval query with ground-truth evidence targets.
    """
    query_id: str = Field(..., description="Unique query identifier")
    document_id: str = Field(..., description="Target document ID")
    query_text: str = Field(..., min_length=1, description="Natural language query or question")
    query_type: Literal["factoid", "spatial", "table", "visual", "multi_hop"] = Field(
        default="factoid",
        description="Query complexity category"
    )
    ground_truth_pages: List[int] = Field(..., description="List of 1-indexed pages containing answer evidence")
    ground_truth_regions: List[str] = Field(default_factory=list, description="Optional list of ground-truth region IDs")

    @field_validator("ground_truth_pages")
    @classmethod
    def validate_gt_pages(cls, v: List[int]) -> List[int]:
        if not v:
            raise ValueError("ground_truth_pages cannot be empty")
        for p in v:
            if p < 1:
                raise ValueError(f"Page numbers must be >= 1. Got: {p}")
        return sorted(list(set(v)))


class PageRetrievalResult(BaseModel):
    """
    Single candidate page retrieval output.
    """
    page_number: int = Field(..., ge=1)
    score: float = Field(..., description="Overall retrieval score")
    text_score: float = Field(default=0.0, description="Lexical or dense text similarity score")
    visual_score: float = Field(default=0.0, description="Visual descriptor similarity score")
    rank: int = Field(..., ge=1, description="1-indexed rank among candidates")
    metadata: Dict[str, Any] = Field(default_factory=dict)


class RegionRetrievalResult(BaseModel):
    """
    Single candidate sub-page region retrieval output.
    """
    region_id: str
    page_number: int = Field(..., ge=1)
    bbox: Tuple[int, int, int, int]
    region_type: str
    score: float
    rank: int = Field(..., ge=1)
    snippet: str = Field(default="")


class EvidencePackage(BaseModel):
    """
    Standardized, self-contained EvidencePackage passed to downstream VLM reasoning.
    Preserves complete provenance, selected pages, and fine-grained spatial evidence.
    """
    package_id: str = Field(..., description="Unique evidence package identifier")
    document_id: str = Field(..., description="Parent document identifier")
    query_id: str = Field(..., description="Query identifier")
    retrieval_method: str = Field(..., description="Retrieval method (e.g. B6-0, B6-1, ..., B6-5)")
    top_k_pages_requested: int = Field(..., ge=1)
    top_m_regions_requested: int = Field(..., ge=1)
    total_document_pages: int = Field(..., ge=1)
    selected_pages: List[PageRetrievalResult] = Field(default_factory=list)
    selected_regions: List[RegionRetrievalResult] = Field(default_factory=list)
    vlm_page_reduction_ratio: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Proportion of document pages pruned before VLM inference: 1 - len(selected_pages) / total_pages"
    )
    provenance: Dict[str, Any] = Field(
        default_factory=dict,
        description="Cryptographic hashes, git commit, seed, and timestamps"
    )

    @model_validator(mode="after")
    def validate_page_reduction(self):
        n_sel = len(self.selected_pages)
        n_tot = self.total_document_pages
        expected_ratio = max(0.0, min(1.0, 1.0 - (float(n_sel) / float(n_tot))))
        # Allow small floating point tolerance
        if abs(self.vlm_page_reduction_ratio - expected_ratio) > 1e-4:
            self.vlm_page_reduction_ratio = round(expected_ratio, 6)
        return self


class RetrievalMetricsResult(BaseModel):
    """
    Aggregated evaluation metrics for a retrieval configuration.
    """
    method: str
    dataset: str
    degradation_level: str
    sample_count: int = Field(..., ge=0)
    recall_at_1: float = Field(default=0.0, ge=0.0, le=1.0)
    recall_at_3: float = Field(default=0.0, ge=0.0, le=1.0)
    recall_at_5: float = Field(default=0.0, ge=0.0, le=1.0)
    recall_at_10: float = Field(default=0.0, ge=0.0, le=1.0)
    recall_at_20: float = Field(default=0.0, ge=0.0, le=1.0)
    mrr: float = Field(default=0.0, ge=0.0, le=1.0)
    ndcg_at_10: float = Field(default=0.0, ge=0.0, le=1.0)
    page_recall: float = Field(default=0.0, ge=0.0, le=1.0)
    evidence_region_recall: float = Field(default=0.0, ge=0.0, le=1.0)
    vlm_page_reduction_ratio: float = Field(default=0.0, ge=0.0, le=1.0)
    avg_latency_ms: float = Field(default=0.0, ge=0.0)
