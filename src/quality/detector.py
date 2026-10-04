"""
Degradation Detector Module for Phase 3.
Classifies specific degradation families and assigns discrete severity levels (S0 to S4)
based on measured visual feature metrics without label leakage.
"""

from __future__ import annotations

import time
from typing import Dict, List, Tuple

from src.quality.config import QualityConfig
from src.quality.schema import DegradationDetection, FeatureResult, FeatureStatus, SeverityLevel

FEATURE_TO_FAMILY = {
    "blur": "gaussian_blur",
    "noise": "gaussian_noise",
    "skew": "skew_rotation",
    "compression": "jpeg_compression",
    "illumination": "illumination",
    "occlusion": "occlusion",
    "resolution": "resolution_reduction",
    "perspective": "perspective_distortion",
    "glare": "glare",
    "contrast": "contrast",
}


def detect_degradations(
    features: Dict[str, FeatureResult],
    config: QualityConfig,
) -> Tuple[List[DegradationDetection], float]:
    """
    Evaluates extracted features and identifies detected degradation families.
    Only features with severity >= 1 (S1_MILD or worse) are flagged as active degradations.

    Args:
        features: Dictionary of FeatureResult objects
        config: Loaded QualityConfig

    Returns:
        (detected_degradations_list, detection_time_ms)
    """
    t0 = time.perf_counter()
    detections: List[DegradationDetection] = []
    severities_count = 0

    for feat_name, result in features.items():
        if result.status != FeatureStatus.MEASURED or result.severity is None:
            continue

        family_name = FEATURE_TO_FAMILY.get(feat_name, feat_name)
        sev = result.severity

        if sev > 0:
            severities_count += 1
            sev_label = SeverityLevel(sev).name
            thresh_cutoffs = config.severity_thresholds.get(family_name, {}).get("cutoffs", [0, 0, 0, 0])
            idx = min(sev - 1, len(thresh_cutoffs) - 1)
            cutoff = float(thresh_cutoffs[idx]) if thresh_cutoffs else 0.0

            detections.append(
                DegradationDetection(
                    family=family_name,
                    severity=sev,
                    severity_label=sev_label,
                    evidence_feature=feat_name,
                    measured_value=result.raw_value if result.raw_value is not None else 0.0,
                    threshold_exceeded=cutoff,
                )
            )

    # Check for composite mixed degradation (>= 3 independent degradations present)
    if severities_count >= 3:
        avg_sev = int(round(sum(d.severity for d in detections) / len(detections)))
        avg_sev = max(1, min(4, avg_sev))
        detections.append(
            DegradationDetection(
                family="mixed_degradation",
                severity=avg_sev,
                severity_label=SeverityLevel(avg_sev).name,
                evidence_feature="composite_multi_family",
                measured_value=float(severities_count),
                threshold_exceeded=3.0,
            )
        )

    elapsed_ms = (time.perf_counter() - t0) * 1000.0
    return detections, elapsed_ms
