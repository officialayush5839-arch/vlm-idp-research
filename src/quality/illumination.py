"""
Illumination and Brightness Quality Feature Extractor.
Measures photometric attenuation and spatial grid illumination variance.
"""

from __future__ import annotations

from typing import Any, Dict
import numpy as np

from src.quality.schema import FeatureResult, FeatureStatus


def measure_illumination(
    gray_image: np.ndarray,
    config: Dict[str, Any],
) -> FeatureResult:
    """
    Measures document illumination attenuation (mean intensity)
    and spatial illumination non-uniformity across a 4x4 spatial grid.

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

    try:
        mean_intensity = float(np.mean(gray_image))

        # Spatial grid partition (e.g. 4x4 grid) to detect localized shadows/gradients
        rows = int(config.get("grid_rows", 4))
        cols = int(config.get("grid_cols", 4))
        r_step, c_step = H // rows, W // cols

        block_means = []
        if r_step > 0 and c_step > 0:
            for r in range(rows):
                for c in range(cols):
                    block = gray_image[r * r_step : (r + 1) * r_step, c * c_step : (c + 1) * c_step]
                    block_means.append(float(np.mean(block)))
            spatial_variance = float(np.var(block_means))
            min_block_mean = float(np.min(block_means))
            max_block_mean = float(np.max(block_means))
        else:
            spatial_variance = 0.0
            min_block_mean = mean_intensity
            max_block_mean = mean_intensity

        # Clean document typically has white background: mean intensity ~ 200-240
        # Normalization: map [0, 240] to [0, 1]
        norm_val = min(1.0, max(0.0, mean_intensity / 240.0))

        # Severity mapping based on attenuation cutoffs:
        # S0: mean >= 195.0; S1: 145 <= mean < 195; S2: 95 <= mean < 145; S3: 50 <= mean < 95; S4: mean < 50
        cutoffs = config.get("cutoffs", [195.0, 145.0, 95.0, 50.0])
        if mean_intensity >= cutoffs[0]:
            severity = 0
        elif mean_intensity >= cutoffs[1]:
            severity = 1
        elif mean_intensity >= cutoffs[2]:
            severity = 2
        elif mean_intensity >= cutoffs[3]:
            severity = 3
        else:
            severity = 4

        return FeatureResult(
            raw_value=round(mean_intensity, 3),
            normalized_value=round(norm_val, 4),
            severity=severity,
            status=FeatureStatus.MEASURED,
            direction="lower_is_worse",
            metadata={
                "metric": "mean_intensity",
                "spatial_grid_variance": round(spatial_variance, 3),
                "min_block_intensity": round(min_block_mean, 2),
                "max_block_intensity": round(max_block_mean, 2),
            },
        )
    except Exception as e:
        return FeatureResult(
            status=FeatureStatus.FAILED,
            direction="lower_is_worse",
            message=f"Illumination extraction failed: {str(e)}",
        )
