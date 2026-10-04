"""
Compression and JPEG Blockiness Quality Feature Extractor.
Implements 8x8 block boundary discontinuity analysis per Wang et al.
"""

from __future__ import annotations

from typing import Any, Dict
import numpy as np

from src.quality.schema import FeatureResult, FeatureStatus


def measure_compression(
    gray_image: np.ndarray,
    config: Dict[str, Any],
) -> FeatureResult:
    """
    Measures JPEG blockiness artifacts along 8x8 DCT grid boundaries.
    Higher blockiness discontinuity indicates more aggressive compression.

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
    if H < 16 or W < 16:
        return FeatureResult(
            status=FeatureStatus.NOT_APPLICABLE,
            direction="higher_is_worse",
            message="Image dimensions too small for 8x8 blockiness analysis.",
        )

    try:
        img_f = gray_image.astype(np.float64)

        # 1. Horizontal block boundaries: columns 8, 16, 24, ...
        # Boundary differences |I(:, 8k - 1) - I(:, 8k)|
        col_indices = np.arange(8, W, 8)
        if len(col_indices) > 0:
            boundary_diffs_h = np.abs(img_f[:, col_indices] - img_f[:, col_indices - 1])
            mean_boundary_h = np.mean(boundary_diffs_h)

            # Interior differences (columns not at 8k boundary)
            interior_cols = [c for c in range(1, W) if c % 8 != 0]
            interior_diffs_h = np.abs(img_f[:, interior_cols] - img_f[:, [c - 1 for c in interior_cols]])
            mean_interior_h = np.mean(interior_diffs_h)
        else:
            mean_boundary_h = 0.0
            mean_interior_h = 1.0

        # 2. Vertical block boundaries: rows 8, 16, 24, ...
        row_indices = np.arange(8, H, 8)
        if len(row_indices) > 0:
            boundary_diffs_v = np.abs(img_f[row_indices, :] - img_f[row_indices - 1, :])
            mean_boundary_v = np.mean(boundary_diffs_v)

            interior_rows = [r for r in range(1, H) if r % 8 != 0]
            interior_diffs_v = np.abs(img_f[interior_rows, :] - img_f[[r - 1 for r in interior_rows], :])
            mean_interior_v = np.mean(interior_diffs_v)
        else:
            mean_boundary_v = 0.0
            mean_interior_v = 1.0

        mean_boundary = (mean_boundary_h + mean_boundary_v) / 2.0
        mean_interior = max(1e-4, (mean_interior_h + mean_interior_v) / 2.0)

        # Relative blockiness score: ratio of boundary jump to interior roughness
        blockiness_ratio = float((mean_boundary - mean_interior) / (mean_boundary + mean_interior + 1e-4))
        # Clip to non-negative score
        blockiness_score = max(0.0, blockiness_ratio)

        # Normalization: map [0, severe_thresh (0.35)] to [0, 1]
        severe_th = float(config.get("severe_threshold", 0.35))
        norm_val = min(1.0, max(0.0, blockiness_score / severe_th))

        # Severity mapping: S0 (<= 0.08) to S4 (> 0.38)
        cutoffs = config.get("cutoffs", [0.08, 0.16, 0.26, 0.38])
        if blockiness_score <= cutoffs[0]:
            severity = 0
        elif blockiness_score <= cutoffs[1]:
            severity = 1
        elif blockiness_score <= cutoffs[2]:
            severity = 2
        elif blockiness_score <= cutoffs[3]:
            severity = 3
        else:
            severity = 4

        return FeatureResult(
            raw_value=round(blockiness_score, 4),
            normalized_value=round(norm_val, 4),
            severity=severity,
            status=FeatureStatus.MEASURED,
            direction="higher_is_worse",
            metadata={
                "metric": "blockiness_discontinuity",
                "mean_boundary_diff": round(mean_boundary, 3),
                "mean_interior_diff": round(mean_interior, 3),
            },
        )
    except Exception as e:
        return FeatureResult(
            status=FeatureStatus.FAILED,
            direction="higher_is_worse",
            message=f"Compression extraction failed: {str(e)}",
        )
