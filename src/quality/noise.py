"""
Noise Feature Extractor.
Implements Immerkaer's fast noise variance estimation algorithm.
"""

from __future__ import annotations

import math
from typing import Any, Dict
import cv2
import numpy as np

from src.quality.schema import FeatureResult, FeatureStatus


def measure_noise(
    gray_image: np.ndarray,
    config: Dict[str, Any],
) -> FeatureResult:
    """
    Estimates additive Gaussian noise standard deviation (sigma)
    using Immerkaer's Laplacian-based fast operator.

    Args:
        gray_image: 2D uint8 numpy array
        config: Feature configuration parameters

    Returns:
        FeatureResult object
    """
    if gray_image is None or gray_image.size == 0:
        return FeatureResult(
            status=FeatureStatus.INVALID_INPUT,
            direction="higher_is_worse",
            message="Input grayscale image is empty or None.",
        )

    H, W = gray_image.shape
    if H < 5 or W < 5:
        return FeatureResult(
            status=FeatureStatus.NOT_APPLICABLE,
            direction="higher_is_worse",
            message=f"Image dimensions ({W}x{H}) too small for Immerkaer noise operator.",
        )

    try:
        # Immerkaer kernel
        # [ 1, -2,  1]
        # [-2,  4, -2]
        # [ 1, -2,  1]
        kernel = np.array([[1, -2, 1], [-2, 4, -2], [1, -2, 1]], dtype=np.float64)
        
        # Convolve using cv2.filter2D with float64
        filtered = cv2.filter2D(gray_image.astype(np.float64), -1, kernel, borderType=cv2.BORDER_CONSTANT)
        
        # Discard 1-pixel border to eliminate boundary artifacts
        inner = filtered[1:-1, 1:-1]
        abs_sum = np.sum(np.abs(inner))
        
        # Scaling factor: sqrt(pi/2) / (6 * (W - 2) * (H - 2))
        factor = math.sqrt(math.pi / 2.0) / (6.0 * (W - 2) * (H - 2))
        noise_sigma = float(abs_sum * factor)

        # Normalization: map [0, severe_thresh] to [0, 1]
        severe_th = float(config.get("severe_threshold", 50.0))
        norm_val = min(1.0, max(0.0, noise_sigma / severe_th))

        # Severity mapping: S0 (Clean) to S4 (Extreme noise)
        cutoffs = config.get("cutoffs", [3.0, 10.0, 22.0, 40.0])
        if noise_sigma <= cutoffs[0]:
            severity = 0
        elif noise_sigma <= cutoffs[1]:
            severity = 1
        elif noise_sigma <= cutoffs[2]:
            severity = 2
        elif noise_sigma <= cutoffs[3]:
            severity = 3
        else:
            severity = 4

        return FeatureResult(
            raw_value=round(noise_sigma, 4),
            normalized_value=round(norm_val, 4),
            severity=severity,
            status=FeatureStatus.MEASURED,
            direction="higher_is_worse",
            metadata={
                "metric": "immerkaer_noise_sigma",
                "image_dims": [W, H],
            },
        )
    except Exception as e:
        return FeatureResult(
            status=FeatureStatus.FAILED,
            direction="higher_is_worse",
            message=f"Noise extraction failed: {str(e)}",
        )
