"""
Blur and Defocus Quality Feature Extractor.
Measures sharpness via Variance of Laplacian and Tenengrad Gradient Energy.
"""

from __future__ import annotations

from typing import Any, Dict
import cv2
import numpy as np

from src.quality.schema import FeatureResult, FeatureStatus


def measure_blur(
    gray_image: np.ndarray,
    config: Dict[str, Any],
) -> FeatureResult:
    """
    Computes blur score using Variance of Laplacian.
    Lower variance indicates higher blur (loss of sharp edges).

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
        # Variance of Laplacian
        laplacian = cv2.Laplacian(gray_image, cv2.CV_64F, ksize=config.get("kernel_size", 3))
        lap_var = float(laplacian.var())

        # Tenengrad Gradient Energy
        gx = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize=3)
        gy = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=3)
        tenengrad = float(np.mean(gx**2 + gy**2))

        # Normalization: map [0, clean_thresh] to [0, 1]
        clean_th = float(config.get("clean_threshold", 300.0))
        norm_val = min(1.0, max(0.0, lap_var / clean_th))

        # Severity mapping: S0 (Clean) to S4 (Extreme blur)
        # S0: var >= 250; S1: 100 <= var < 250; S2: 45 <= var < 100; S3: 20 <= var < 45; S4: var < 20
        cutoffs = config.get("cutoffs", [250.0, 100.0, 45.0, 20.0])
        if lap_var >= cutoffs[0]:
            severity = 0
        elif lap_var >= cutoffs[1]:
            severity = 1
        elif lap_var >= cutoffs[2]:
            severity = 2
        elif lap_var >= cutoffs[3]:
            severity = 3
        else:
            severity = 4

        return FeatureResult(
            raw_value=round(lap_var, 4),
            normalized_value=round(norm_val, 4),
            severity=severity,
            status=FeatureStatus.MEASURED,
            direction="lower_is_worse",
            metadata={
                "metric": "laplacian_variance",
                "tenengrad_energy": round(tenengrad, 2),
            },
        )
    except Exception as e:
        return FeatureResult(
            status=FeatureStatus.FAILED,
            direction="lower_is_worse",
            message=f"Blur extraction failed: {str(e)}",
        )
