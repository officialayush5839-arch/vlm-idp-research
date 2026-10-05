"""
Quality Feature Adapter for Phase 5 Adaptive Routing.
Extracts and normalizes inference-time visual quality metrics from PageQualityAssessment.
Strictly non-leaking: extracts only observable visual measurements.
"""

from __future__ import annotations

from typing import Dict, List, Optional
from src.quality.schema import PageQualityAssessment


FEATURE_KEYS: List[str] = [
    "blur",
    "noise",
    "skew",
    "glare",
    "contrast",
    "resolution",
    "compression",
    "illumination",
    "occlusion",
    "perspective",
]


class QualityFeatureAdapter:
    """
    Adapts PageQualityAssessment records into clean numerical vectors for routing policies.
    """

    def __init__(self, feature_keys: Optional[List[str]] = None):
        self.feature_keys = feature_keys or list(FEATURE_KEYS)

    def extract_features(self, assessment: PageQualityAssessment) -> Dict[str, float]:
        """
        Extract normalized quality feature dictionary in [0.0, 1.0].
        If a feature extractor failed or was absent, safely defaults to 0.0.
        """
        extracted: Dict[str, float] = {}
        for key in self.feature_keys:
            feat_res = assessment.features.get(key)
            if feat_res is not None and feat_res.normalized_value is not None:
                extracted[key] = float(max(0.0, min(1.0, feat_res.normalized_value)))
            else:
                extracted[key] = 0.0
        return extracted

    def extract_vector(self, assessment: PageQualityAssessment) -> List[float]:
        """
        Extract ordered list of floats corresponding to self.feature_keys.
        """
        feat_dict = self.extract_features(assessment)
        return [feat_dict[k] for k in self.feature_keys]
