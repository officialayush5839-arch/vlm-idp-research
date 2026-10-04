"""
Pydantic data schemas for Document Quality Assessment and Degradation Detection (Phase 3).
Enforces strict typing, provenance tracking, and explicit failure status isolation.
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class FeatureStatus(str, Enum):
    """Execution status for an individual quality feature extractor."""
    MEASURED = "MEASURED"
    NOT_AVAILABLE = "NOT_AVAILABLE"
    INVALID_INPUT = "INVALID_INPUT"
    FAILED = "FAILED"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class SeverityLevel(int, Enum):
    """Discrete degradation severity scale (S0 to S4 per Phase 0 Protocol)."""
    S0_CLEAN = 0
    S1_MILD = 1
    S2_MODERATE = 2
    S3_SEVERE = 3
    S4_EXTREME = 4

    @property
    def label(self) -> str:
        return self.name


class FeatureResult(BaseModel):
    """Detailed result of an individual visual feature extraction."""
    raw_value: Optional[float] = Field(default=None, description="Direct unnormalized measurement")
    normalized_value: Optional[float] = Field(default=None, description="Normalized score in [0.0, 1.0]")
    severity: Optional[int] = Field(default=None, ge=0, le=4, description="Mapped severity level 0-4")
    status: FeatureStatus = Field(default=FeatureStatus.MEASURED)
    direction: str = Field(default="higher_is_worse", description="Polarity of raw feature value")
    message: Optional[str] = Field(default=None, description="Diagnostics or failure reason if applicable")
    metadata: Dict[str, Any] = Field(default_factory=dict)


class DegradationDetection(BaseModel):
    """Detection record identifying a specific degradation family present on the page."""
    family: str = Field(description="Name of degradation family, e.g. gaussian_blur")
    severity: int = Field(ge=0, le=4, description="Assigned severity level (0=clean, 1-4 degraded)")
    severity_label: str = Field(description="S0_CLEAN, S1_MILD, S2_MODERATE, S3_SEVERE, S4_EXTREME")
    evidence_feature: str = Field(description="Primary feature metric supporting this classification")
    measured_value: float = Field(description="Numerical value of supporting feature")
    threshold_exceeded: float = Field(description="Cutoff threshold that was crossed")


class RuntimeBreakdown(BaseModel):
    """Benchmarked execution latency and memory usage for quality assessment."""
    preprocessing_ms: float = Field(ge=0.0)
    feature_extraction_ms: float = Field(ge=0.0)
    detection_ms: float = Field(ge=0.0)
    aggregation_ms: float = Field(default=0.0, ge=0.0)
    total_latency_ms: float = Field(ge=0.0)
    memory_mb: Optional[float] = Field(default=None, description="Memory used in MB or None if NOT_AVAILABLE")


class PageQualityAssessment(BaseModel):
    """Complete visual quality assessment for a single document page."""
    document_id: str
    page_id: str
    page_number: int = Field(ge=1)
    width: int = Field(gt=0)
    height: int = Field(gt=0)

    # Dictionary of all extracted visual features (blur, noise, skew, etc.)
    features: Dict[str, FeatureResult]

    # Explicit list of detected degradations with severity > 0
    detected_degradations: List[DegradationDetection] = Field(default_factory=list)

    # Note: Phase 0 protocol does NOT formalize an authoritative overall quality aggregation formula.
    # Therefore, overall_quality_score is marked None (NOT_DEFINED) to prevent scientific fabrication.
    overall_quality_score: Optional[float] = Field(
        default=None,
        description="Overall aggregate quality score (None / NOT_DEFINED per Phase 0 Protocol Section 13)"
    )
    overall_quality_status: str = Field(
        default="NOT_DEFINED",
        description="NOT_DEFINED until protocol explicitly authorizes aggregation formula"
    )

    runtime: RuntimeBreakdown
    algorithm_version: str = "1.0.0"
    config_hash: str
    timestamp_utc: str
    status: str = "SUCCESS"  # SUCCESS, PARTIAL_SUCCESS, FAILED


class DocumentQualityAssessment(BaseModel):
    """Aggregated document-level visual quality report preserving page-level fidelity."""
    document_id: str
    page_count: int = Field(ge=1)
    pages: List[PageQualityAssessment]

    # Descriptive summary statistics across pages (mean, median, min, max, std)
    summary_statistics: Dict[str, Any] = Field(default_factory=dict)
    worst_page_id: Optional[str] = None
    worst_page_number: Optional[int] = None
    highest_severity_detected: int = Field(default=0, ge=0, le=4)
    highest_severity_family: Optional[str] = None

    algorithm_version: str = "1.0.0"
    config_hash: str
    timestamp_utc: str
    status: str = "SUCCESS"
