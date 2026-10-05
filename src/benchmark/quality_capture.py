"""
Quality Feature Capture Hook for Observational Benchmark Analysis.
Executes Phase 3 DocumentQualityPipeline independently alongside baseline evaluations.
Strictly observational per Section 31 and 68 of the Phase 4 specification.
"""

from __future__ import annotations

from typing import Any, Dict, Optional
from PIL import Image

from src.quality.config import load_phase3_quality_config
from src.quality.pipeline import DocumentQualityPipeline


class QualityCaptureHook:
    """Non-intrusive quality feature extractor capturing Phase 3 metrics."""

    def __init__(
        self,
        quality_config_path: str = "configs/phase3/quality_config.yaml",
        feature_config_path: str = "configs/phase3/feature_config.yaml",
        severity_config_path: str = "configs/phase3/severity_config.yaml",
    ):
        try:
            cfg = load_phase3_quality_config(
                quality_config_path=quality_config_path,
                feature_config_path=feature_config_path,
                severity_config_path=severity_config_path,
            )
            self.pipeline = DocumentQualityPipeline(config=cfg)
        except Exception:
            self.pipeline = DocumentQualityPipeline()

    def capture(self, image: Image.Image, doc_id: str, page_idx: int = 0) -> Dict[str, Any]:
        """
        Runs quality assessment independently.
        Returns serialized dictionary of features and degradation predictions.
        """
        try:
            page_id = f"{doc_id}_p{page_idx}"
            assessment = self.pipeline.assess_page(
                image_input=image,
                document_id=doc_id,
                page_id=page_id,
                page_number=page_idx + 1,
            )
            return {
                "algorithm_version": assessment.algorithm_version,
                "config_hash": assessment.config_hash,
                "overall_quality_status": assessment.overall_quality_status,
                "overall_quality_score": assessment.overall_quality_score,
                "features": {
                    name: {
                        "raw_value": feat.raw_value,
                        "normalized_value": feat.normalized_value,
                        "severity": feat.severity,
                        "status": feat.status.value,
                    }
                    for name, feat in assessment.features.items()
                },
                "detected_degradations": [
                    {
                        "family": deg.family,
                        "severity": deg.severity,
                        "severity_label": deg.severity_label,
                        "evidence_feature": deg.evidence_feature,
                        "measured_value": deg.measured_value,
                    }
                    for deg in assessment.detected_degradations
                ],
                "runtime_ms": assessment.runtime.total_latency_ms,
            }
        except Exception as e:
            return {
                "status": "ERROR",
                "error_message": str(e),
                "features": {},
                "detected_degradations": [],
            }
