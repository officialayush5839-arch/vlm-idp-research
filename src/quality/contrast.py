"""
Contrast and Dynamic Range Quality Feature Extractor.
Measures RMS contrast, dynamic range, and Michelson contrast.
"""

from __future__ import annotations

from typing import Any, Dict
import numpy as np

from src.quality.schema import FeatureResult, FeatureStatus


def measure_contrast(
    gray_image: np.ndarray,
    config: Dict[str, Any],
) -> FeatureResult:
    """
    Computes RMS contrast (standard deviation of normalized pixel intensities).
    Lower contrast indicates faded, washed-out, or low dynamic range documents.

    Args:
        gray_image: 2D uint8 numpy array
        config: Feature configuration parameters

    Returns:
        FeatureResult object
    """
    if gray_image is None or gray_image.size == 0:
        return FeatureResult(
            status=FeatureStatus.INVALID_INPUT,
            direction="lower_is_worse",
            message="Input grayscale image is empty or None.",
        )

    try:
        norm_img = gray_image.astype(np.float64) / 255.0
        rms_contrast = float(np.std(norm_img))

        # Effective dynamic range (99.5th percentile paper background - 0.5th percentile text ink)
        p_low, p_high = np.percentile(gray_image, [0.5, 99.5])
        dynamic_range = float(p_high - p_low)
        effective_dr_norm = min(1.0, max(0.0, dynamic_range / 255.0))

        # Severity mapping: S0 (>= 0.70) to S4 (< 0.15)
        # S0: >= 0.70; S1: 0.50 <= dr < 0.70; S2: 0.30 <= dr < 0.50; S3: 0.15 <= dr < 0.30; S4: < 0.15
        cutoffs = config.get("cutoffs", [0.70, 0.50, 0.30, 0.15])
        if effective_dr_norm >= cutoffs[0]:
            severity = 0
        elif effective_dr_norm >= cutoffs[1]:
            severity = 1
        elif effective_dr_norm >= cutoffs[2]:
            severity = 2
        elif effective_dr_norm >= cutoffs[3]:
            severity = 3
        else:
            severity = 4

        return FeatureResult(
            raw_value=round(effective_dr_norm, 4),
            normalized_value=round(effective_dr_norm, 4),
            severity=severity,
            status=FeatureStatus.MEASURED,
            direction="lower_is_worse",
            metadata={
                "metric": "effective_dynamic_range",
                "raw_dynamic_range": round(dynamic_range, 2),
                "p_low": round(float(p_low), 2),
                "p_high": round(float(p_high), 2),
            },
        )
    except Exception as e:
        return FeatureResult(
            status=FeatureStatus.FAILED,
            direction="lower_is_worse",
            message=f"Contrast extraction failed: {str(e)}",
        )
