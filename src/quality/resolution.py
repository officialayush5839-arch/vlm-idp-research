"""
Resolution and Effective Scale Quality Feature Extractor.
Measures high-frequency edge density and pixel dimension metrics.
"""

from __future__ import annotations

from typing import Any, Dict
import cv2
import numpy as np

from src.quality.schema import FeatureResult, FeatureStatus


def measure_resolution(
    gray_image: np.ndarray,
    config: Dict[str, Any],
) -> FeatureResult:
    """
    Measures high-frequency edge density and document resolution adequacy.
    Downsampled or low-resolution documents experience sharp drops in edge density.

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

    H, W = gray_image.shape
    total_pixels = H * W

    try:
        # Compute gradient magnitude using Sobel operators
        gx = cv2.Sobel(gray_image, cv2.CV_32F, 1, 0, ksize=3)
        gy = cv2.Sobel(gray_image, cv2.CV_32F, 0, 1, ksize=3)
        magnitude = cv2.magnitude(gx, gy)

        # High-frequency edge sharpness ratio (fine edge stroke preservation)
        sharp_edges = int(np.sum(magnitude > 150.0))
        soft_edges = int(np.sum(magnitude > 30.0))
        sharpness_ratio = float(sharp_edges / max(1, soft_edges))

        # Normalization: map [0, 1.0]
        norm_val = min(1.0, max(0.0, sharpness_ratio))

        # Severity mapping: S0 (>= 0.80) to S4 (< 0.05)
        # S0: >= 0.80; S1: 0.65 <= r < 0.80; S2: 0.35 <= r < 0.65; S3: 0.05 <= r < 0.35; S4: < 0.05
        cutoffs = config.get("cutoffs", [0.80, 0.65, 0.35, 0.05])
        if sharpness_ratio >= cutoffs[0]:
            severity = 0
        elif sharpness_ratio >= cutoffs[1]:
            severity = 1
        elif sharpness_ratio >= cutoffs[2]:
            severity = 2
        elif sharpness_ratio >= cutoffs[3]:
            severity = 3
        else:
            severity = 4

        return FeatureResult(
            raw_value=round(sharpness_ratio, 4),
            normalized_value=round(norm_val, 4),
            severity=severity,
            status=FeatureStatus.MEASURED,
            direction="lower_is_worse",
            metadata={
                "metric": "high_freq_sharpness_ratio",
                "sharp_edges": sharp_edges,
                "soft_edges": soft_edges,
                "width": W,
                "height": H,
            },
        )
    except Exception as e:
        return FeatureResult(
            status=FeatureStatus.FAILED,
            direction="lower_is_worse",
            message=f"Resolution extraction failed: {str(e)}",
        )
