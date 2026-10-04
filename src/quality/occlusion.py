"""
Occlusion and Cutout Masking Quality Feature Extractor.
Measures physical obstruction and artificial cutout mask coverage.
"""

from __future__ import annotations

from typing import Any, Dict
import cv2
import numpy as np

from src.quality.schema import FeatureResult, FeatureStatus


def measure_occlusion(
    gray_image: np.ndarray,
    config: Dict[str, Any],
) -> FeatureResult:
    """
    Measures document occlusion ratio (fraction of document area covered by dark/gray cutout patches).

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
        # Detect pixels matching synthetic cutout / occlusion masks (typically intensity <= 40 or low variance blocks)
        intensity_max = int(config.get("intensity_max", 40))
        _, dark_mask = cv2.threshold(gray_image, intensity_max, 255, cv2.THRESH_BINARY_INV)

        # Filter out thin text characters: text strokes are thin (1-4px wide),
        # whereas occlusion masks are large connected blocks (e.g. at least 15x15 px).
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (11, 11))
        block_mask = cv2.morphologyEx(dark_mask, cv2.MORPH_OPEN, kernel)

        # Count connected components
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(block_mask, connectivity=8)
        
        min_patch_area = int(config.get("min_patch_area", max(200, total_pixels // 500)))
        occluded_pixels = 0
        patch_count = 0

        for i in range(1, num_labels):
            area = stats[i, cv2.CC_STAT_AREA]
            if area >= min_patch_area:
                occluded_pixels += area
                patch_count += 1

        occlusion_ratio = float(occluded_pixels / total_pixels)

        # Normalization: map [0, severe_thresh (0.35)] to [0, 1]
        severe_th = float(config.get("severe_threshold", 0.35))
        norm_val = min(1.0, max(0.0, occlusion_ratio / severe_th))

        # Severity mapping: S0 (<= 0.02) to S4 (> 0.25)
        cutoffs = config.get("cutoffs", [0.02, 0.075, 0.15, 0.25])
        if occlusion_ratio <= cutoffs[0]:
            severity = 0
        elif occlusion_ratio <= cutoffs[1]:
            severity = 1
        elif occlusion_ratio <= cutoffs[2]:
            severity = 2
        elif occlusion_ratio <= cutoffs[3]:
            severity = 3
        else:
            severity = 4

        return FeatureResult(
            raw_value=round(occlusion_ratio, 4),
            normalized_value=round(norm_val, 4),
            severity=severity,
            status=FeatureStatus.MEASURED,
            direction="higher_is_worse",
            metadata={
                "metric": "occluded_area_ratio",
                "detected_patches": patch_count,
                "total_occluded_pixels": int(occluded_pixels),
            },
        )
    except Exception as e:
        return FeatureResult(
            status=FeatureStatus.FAILED,
            direction="higher_is_worse",
            message=f"Occlusion extraction failed: {str(e)}",
        )
