"""
Skew and Rotation Quality Feature Extractor.
Measures document orientation angle using Hough Line Transform.
Non-destructive: calculates angle without altering source image.
"""

from __future__ import annotations

import math
from typing import Any, Dict
import cv2
import numpy as np

from src.quality.schema import FeatureResult, FeatureStatus


def measure_skew(
    gray_image: np.ndarray,
    config: Dict[str, Any],
) -> FeatureResult:
    """
    Measures document skew angle (in degrees) using Probabilistic Hough Lines.

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
    if H < 20 or W < 20:
        return FeatureResult(
            raw_value=0.0,
            normalized_value=0.0,
            severity=0,
            status=FeatureStatus.NOT_APPLICABLE,
            direction="higher_is_worse",
            message="Image dimensions too small for reliable skew estimation.",
        )

    try:
        # Edge detection
        edges = cv2.Canny(gray_image, 50, 150, apertureSize=3)

        # Detect line segments using Probabilistic Hough Transform
        min_line_len = int(config.get("min_line_length", min(50, W // 10)))
        max_line_gap = int(config.get("max_line_gap", 10))
        lines = cv2.HoughLinesP(
            edges,
            rho=1,
            theta=np.pi / 180,
            threshold=int(config.get("hough_threshold", 50)),
            minLineLength=max(10, min_line_len),
            maxLineGap=max_line_gap,
        )

        detected_angles = []
        if lines is not None:
            for raw_line in lines:
                line = np.asarray(raw_line).flatten()
                if len(line) < 4:
                    continue
                x1, y1, x2, y2 = line[0], line[1], line[2], line[3]
                dx = x2 - x1
                dy = y2 - y1
                if dx == 0:
                    continue
                angle_rad = math.atan2(dy, dx)
                angle_deg = math.degrees(angle_rad)

                # Focus on near-horizontal text lines (e.g. within [-45, 45] degrees)
                if -45.0 <= angle_deg <= 45.0:
                    detected_angles.append(angle_deg)

        if detected_angles:
            # Median angle is resilient against vertical borders and outliers
            median_angle = float(np.median(detected_angles))
            abs_skew_deg = abs(median_angle)
            num_lines = len(detected_angles)
        else:
            # Fallback: projection profile method or zero if no dominant lines found
            abs_skew_deg = 0.0
            num_lines = 0

        # Normalization: map [0, severe_thresh (10.0 deg)] to [0, 1]
        severe_th = float(config.get("severe_threshold", 10.0))
        norm_val = min(1.0, max(0.0, abs_skew_deg / severe_th))

        # Severity mapping: S0 (0 <= 0.5 deg) to S4 (> 7.5 deg)
        cutoffs = config.get("cutoffs", [0.5, 2.0, 4.0, 7.5])
        if abs_skew_deg <= cutoffs[0]:
            severity = 0
        elif abs_skew_deg <= cutoffs[1]:
            severity = 1
        elif abs_skew_deg <= cutoffs[2]:
            severity = 2
        elif abs_skew_deg <= cutoffs[3]:
            severity = 3
        else:
            severity = 4

        return FeatureResult(
            raw_value=round(abs_skew_deg, 4),
            normalized_value=round(norm_val, 4),
            severity=severity,
            status=FeatureStatus.MEASURED,
            direction="higher_is_worse",
            metadata={
                "metric": "skew_angle_deg",
                "detected_lines_count": num_lines,
                "signed_angle_deg": round(median_angle if detected_angles else 0.0, 4),
            },
        )
    except Exception as e:
        return FeatureResult(
            status=FeatureStatus.FAILED,
            direction="higher_is_worse",
            message=f"Skew extraction failed: {str(e)}",
        )
