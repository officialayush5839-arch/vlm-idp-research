"""
Document Quality and Degradation Assessment Subsystem (Phase 3).
Provides reproducible, independent visual quality feature extraction and degradation detection.
"""

from src.quality.config import QualityConfig, load_phase3_quality_config
from src.quality.pipeline import DocumentQualityPipeline
from src.quality.schema import (
    DegradationDetection,
    DocumentQualityAssessment,
    FeatureResult,
    FeatureStatus,
    PageQualityAssessment,
    RuntimeBreakdown,
    SeverityLevel,
)

__all__ = [
    "QualityConfig",
    "load_phase3_quality_config",
    "DocumentQualityPipeline",
    "FeatureStatus",
    "SeverityLevel",
    "FeatureResult",
    "DegradationDetection",
    "RuntimeBreakdown",
    "PageQualityAssessment",
    "DocumentQualityAssessment",
]
