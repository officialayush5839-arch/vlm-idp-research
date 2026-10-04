"""
Glare and Specular Reflection Quality Feature Extractor.
Measures overexposure hotspots and saturated pixel clustering.
"""

from __future__ import annotations

from typing import Any, Dict
import cv2
import numpy as np

from src.quality.schema import FeatureResult, FeatureStatus


def measure_glare(
    gray_image: np.ndarray,
    config: Dict[str, Any],
) -> FeatureResult:
    """
    Measures specular reflection / overexposure glare fraction.
    Distinguishes legitimate white paper from concentrated glare hotspots.

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
    total_pixels = H * W

    try:
        # Luminance threshold for highlight clipping
        thresh_val = int(config.get("luminance_threshold", 250))
        _, sat_mask = cv2.threshold(gray_image, thresh_val, 255, cv2.THRESH_BINARY)

        # Morphological opening to filter isolated single-pixel noise
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        clean_mask = cv2.morphologyEx(sat_mask, cv2.MORPH_OPEN, kernel)

        # Connected component analysis for concentrated hotspots
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(clean_mask, connectivity=8)
        
        min_cluster_area = int(config.get("min_region_area", 50))
        glare_pixel_count = 0
        largest_cluster = 0

        for i in range(1, num_labels):
            area = stats[i, cv2.CC_STAT_AREA]
            if area >= min_cluster_area:
                glare_pixel_count += area
                if area > largest_cluster:
                    largest_cluster = area

        glare_ratio = float(glare_pixel_count / total_pixels)

        # Normalization: map [0, severe_thresh (0.25)] to [0, 1]
        severe_th = float(config.get("severe_threshold", 0.25))
        norm_val = min(1.0, max(0.0, glare_ratio / severe_th))

        # Severity mapping: S0 (0 <= 0.02) to S4 (> 0.22)
        cutoffs = config.get("cutoffs", [0.02, 0.06, 0.12, 0.22])
        if glare_ratio <= cutoffs[0]:
            severity = 0
        elif glare_ratio <= cutoffs[1]:
            severity = 1
        elif glare_ratio <= cutoffs[2]:
            severity = 2
        elif glare_ratio <= cutoffs[3]:
            severity = 3
        else:
            severity = 4

        return FeatureResult(
            raw_value=round(glare_ratio, 4),
            normalized_value=round(norm_val, 4),
            severity=severity,
            status=FeatureStatus.MEASURED,
            direction="higher_is_worse",
            metadata={
                "metric": "glare_fraction",
                "largest_hotspot_pixels": int(largest_cluster),
                "total_saturated_pixels": int(glare_pixel_count),
            },
        )
    except Exception as e:
        return FeatureResult(
            status=FeatureStatus.FAILED,
            direction="higher_is_worse",
            message=f"Glare extraction failed: {str(e)}",
        )
