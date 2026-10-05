"""
Pydantic Domain Models and Schemas for Phase 8 Uncertainty Calibration & Abstention.
Defines strict schemas for UncertaintyFeatures, CalibrationArtifact,
AbstentionDecision, UncertaintyPackage, and Evaluation Metrics.
"""

from typing import List, Dict, Any, Optional, Tuple, Literal
from pydantic import BaseModel, Field, field_validator, model_validator


class UncertaintyFeatures(BaseModel):
    """
    Inference-time observable multi-signal uncertainty feature vector.
    Zero ground-truth or benchmark degradation label leakage.
    """
    model_confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    retrieval_margin: float = Field(default=1.0, ge=0.0, le=1.0)
    retrieval_entropy: float = Field(default=0.0, ge=0.0, le=1.0)
    semantic_support_score: float = Field(default=1.0, ge=0.0, le=1.0)
    entity_coverage: float = Field(default=1.0, ge=0.0, le=1.0)
    spatial_valid: float = Field(default=1.0, ge=0.0, le=1.0)
    sufficiency_status: Literal["SUFFICIENT", "PARTIALLY_SUFFICIENT", "INSUFFICIENT"] = Field(default="SUFFICIENT")
    grounding_status: Literal["GROUNDED", "PARTIALLY_GROUNDED", "UNSUPPORTED"] = Field(default="GROUNDED")
    citation_count: int = Field(default=1, ge=0)
    visual_quality_score: float = Field(default=1.0, ge=0.0, le=1.0)
    quality_blur: float = Field(default=0.0, ge=0.0, le=1.0)
    quality_noise: float = Field(default=0.0, ge=0.0, le=1.0)
    quality_skew: float = Field(default=0.0, ge=0.0, le=1.0)
    quality_contrast: float = Field(default=1.0, ge=0.0, le=1.0)
    quality_resolution: float = Field(default=1.0, ge=0.0, le=1.0)
    page_count: int = Field(default=1, ge=1)
    composite_raw_confidence: float = Field(default=1.0, ge=0.0, le=1.0)

    def to_feature_vector(self) -> List[float]:
        """
        Convert numeric features to a dense 1D vector for calibration or regression.
        """
        suff_map = {"SUFFICIENT": 1.0, "PARTIALLY_SUFFICIENT": 0.5, "INSUFFICIENT": 0.0}
        gnd_map = {"GROUNDED": 1.0, "PARTIALLY_GROUNDED": 0.5, "UNSUPPORTED": 0.0}

        return [
            self.model_confidence,
            self.retrieval_margin,
            1.0 - self.retrieval_entropy,
            self.semantic_support_score,
            self.entity_coverage,
            self.spatial_valid,
            suff_map[self.sufficiency_status],
            gnd_map[self.grounding_status],
            min(1.0, self.citation_count / 5.0),
            self.visual_quality_score,
            1.0 - self.quality_blur,
            1.0 - self.quality_noise,
            1.0 - self.quality_skew,
            self.quality_contrast,
            self.quality_resolution,
            min(1.0, 1.0 / self.page_count),
        ]


class CalibrationArtifact(BaseModel):
    """
    Serialized parameters for a fitted post-hoc calibration model.
    """
    method: Literal["uncalibrated", "temperature_scaling", "isotonic_regression"]
    training_partition: str = Field(default="val")
    temperature: Optional[float] = Field(default=None)
    isotonic_x: Optional[List[float]] = Field(default=None)
    isotonic_y: Optional[List[float]] = Field(default=None)
    config_hash: str = Field(...)
    artifact_hash: str = Field(...)
    created_at_utc: str = Field(...)


class AbstentionDecision(BaseModel):
    """
    Selective prediction decision for an answered query.
    """
    decision: Literal["ANSWER", "ABSTAIN"]
    calibrated_confidence: float = Field(..., ge=0.0, le=1.0)
    threshold: float = Field(..., ge=0.0, le=1.0)
    target_coverage: float = Field(..., ge=0.0, le=1.0)
    margin: float = Field(...)
    abstention_reason: str = Field(default="")


class UncertaintyPackage(BaseModel):
    """
    Complete, self-contained uncertainty assessment bundle.
    """
    package_id: str
    document_id: str
    query_id: str
    raw_confidence: float = Field(..., ge=0.0, le=1.0)
    calibrated_confidence: float = Field(..., ge=0.0, le=1.0)
    features: UncertaintyFeatures
    decision: AbstentionDecision
    calibration_method: str
    provenance: Dict[str, Any] = Field(default_factory=dict)
    package_hash: str


class CalibrationMetricsResult(BaseModel):
    """
    Quantitative evaluation metrics for calibration accuracy.
    """
    method: str
    sample_count: int = Field(..., ge=0)
    expected_calibration_error: float = Field(..., ge=0.0, le=1.0)
    maximum_calibration_error: float = Field(..., ge=0.0, le=1.0)
    brier_score: float = Field(..., ge=0.0, le=1.0)
    negative_log_likelihood: float = Field(..., ge=0.0)
    calibration_slope: float = Field(...)
    calibration_intercept: float = Field(...)


class SelectivePredictionMetricsResult(BaseModel):
    """
    Risk-coverage and selective prediction metrics across target coverage thresholds.
    """
    method: str
    target_coverage: float = Field(..., ge=0.0, le=1.0)
    empirical_coverage: float = Field(..., ge=0.0, le=1.0)
    selective_risk: float = Field(..., ge=0.0, le=1.0)
    selective_accuracy: float = Field(..., ge=0.0, le=1.0)
    error_rate_answered: float = Field(..., ge=0.0, le=1.0)
    abstention_rate: float = Field(..., ge=0.0, le=1.0)
    aurc: float = Field(..., ge=0.0, le=1.0)
    excess_aurc: float = Field(default=0.0)
    auroc_correctness: float = Field(default=0.5, ge=0.0, le=1.0)
