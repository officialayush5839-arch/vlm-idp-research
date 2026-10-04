"""
Perspective Distortion Quality Feature Extractor.
Measures projective trapezoidal convergence angle from document line segments.
"""

from __future__ import annotations

import math
from typing import Any, Dict
import cv2
import numpy as np

from src.quality.schema import FeatureResult, FeatureStatus


def measure_perspective(
    gray_image: np.ndarray,
    config: Dict[str, Any],
) -> FeatureResult:
    """
    Measures perspective distortion by analyzing the trapezoidal convergence
    between opposing vertical/horizontal line segments.

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
    if H < 30 or W < 30:
        return FeatureResult(
            raw_value=0.0,
            normalized_value=0.0,
            severity=0,
            status=FeatureStatus.NOT_APPLICABLE,
            direction="higher_is_worse",
            message="Image dimensions too small for perspective analysis.",
        )

    try:
        # Edge detection
        edges = cv2.Canny(gray_image, 50, 150)
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=40, minLineLength=W // 8, maxLineGap=15)

        left_tilts = []
        right_tilts = []

        if lines is not None:
            mid_x = W / 2.0
            for raw_line in lines:
                line = np.asarray(raw_line).flatten()
                if len(line) < 4:
                    continue
                x1, y1, x2, y2 = line[0], line[1], line[2], line[3]
                dx = x2 - x1
                dy = y2 - y1
                if dx == 0:
                    continue
                ang = math.degrees(math.atan2(dy, dx))
                # Vertical or near-vertical lines (|ang| > 45 deg)
                if abs(ang) > 45.0:
                    tilt = 90.0 - abs(ang)
                    if (x1 + x2) / 2.0 < mid_x:
                        left_tilts.append(tilt)
                    else:
                        right_tilts.append(tilt)

        if left_tilts and right_tilts:
            med_left = float(np.median(left_tilts))
            med_right = float(np.median(right_tilts))
            # Trapezoidal convergence angle between left and right margins
            convergence_deg = abs(med_left + med_right)
        else:
            convergence_deg = 0.0

        # Normalization: map [0, severe_thresh (35.0 deg)] to [0, 1]
        severe_th = float(config.get("severe_threshold", 35.0))
        norm_val = min(1.0, max(0.0, convergence_deg / severe_th))

        # Severity mapping: S0 (<= 2.5 deg) to S4 (> 30.0 deg)
        cutoffs = config.get("cutoffs", [2.5, 10.0, 20.0, 30.0])
        if convergence_deg <= cutoffs[0]:
            severity = 0
        elif convergence_deg <= cutoffs[1]:
            severity = 1
        elif convergence_deg <= cutoffs[2]:
            severity = 2
        elif convergence_deg <= cutoffs[3]:
            severity = 3
        else:
            severity = 4

        return FeatureResult(
            raw_value=round(convergence_deg, 4),
            normalized_value=round(norm_val, 4),
            severity=severity,
            status=FeatureStatus.MEASURED,
            direction="higher_is_worse",
            metadata={
                "metric": "perspective_convergence_deg",
                "left_lines": len(left_tilts),
                "right_lines": len(right_tilts),
            },
        )
    except Exception as e:
        return FeatureResult(
            status=FeatureStatus.FAILED,
            direction="higher_is_worse",
            message=f"Perspective extraction failed: {str(e)}",
        )
