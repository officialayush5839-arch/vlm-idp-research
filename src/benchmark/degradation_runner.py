"""
Degradation Runner with Deterministic Image Synthesis and Coordinate Mapping.
Strictly wraps src/quality/synthetic.py per Section 12 of the Phase 4 specification.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import cv2
import numpy as np
from PIL import Image

from src.benchmark.manifest import compute_sha256
from src.benchmark.schema import BenchmarkSample, DegradationCondition
from src.quality.synthetic import apply_degradation


def transform_bbox_geometric(
    bbox: List[int],
    family: str,
    severity: int,
    width: int,
    height: int,
) -> List[int]:
    """
    Transforms normalized [0, 1000] bounding box coordinates through geometric corruptions.
    Computes forward transformation of 4 corner points and extracts new bounding box.
    """
    if severity == 0 or family in [
        "clean",
        "gaussian_blur",
        "gaussian_noise",
        "jpeg_compression",
        "illumination",
        "occlusion",
        "resolution_reduction",
    ]:
        return bbox.copy()

    x1_norm, y1_norm, x2_norm, y2_norm = bbox
    # Denormalize to pixel space
    x1_px = (x1_norm / 1000.0) * width
    y1_px = (y1_norm / 1000.0) * height
    x2_px = (x2_norm / 1000.0) * width
    y2_px = (y2_norm / 1000.0) * height

    pts = np.float32([
        [x1_px, y1_px],
        [x2_px, y1_px],
        [x2_px, y2_px],
        [x1_px, y2_px],
    ])

    if family in ["skew_rotation", "mixed_degradation"]:
        angles = [0.0, 1.0, 3.0, 5.0, 10.0]
        angle = angles[severity]
        center = (width / 2.0, height / 2.0)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        # Transform points
        ones = np.ones(shape=(len(pts), 1))
        pts_ones = np.hstack([pts, ones])
        transformed_pts = M.dot(pts_ones.T).T

    elif family == "perspective_distortion":
        tilts = [0.0, 5.0, 15.0, 25.0, 35.0]
        tilt_deg = tilts[severity]
        tilt_rad = math.radians(tilt_deg)
        delta_x = int((width * 0.4) * math.sin(tilt_rad))
        delta_y = int((height * 0.2) * math.sin(tilt_rad))

        src_pts = np.float32([[0, 0], [width, 0], [width, height], [0, height]])
        dst_pts = np.float32([
            [delta_x, delta_y],
            [width - delta_x, delta_y],
            [width, height - delta_y],
            [0, height - delta_y],
        ])
        M = cv2.getPerspectiveTransform(src_pts, dst_pts)
        pts_reshaped = pts.reshape(-1, 1, 2)
        transformed_pts = cv2.perspectiveTransform(pts_reshaped, M).reshape(-1, 2)
    else:
        transformed_pts = pts

    # Compute enclosing bounding box
    min_x = np.min(transformed_pts[:, 0])
    max_x = np.max(transformed_pts[:, 0])
    min_y = np.min(transformed_pts[:, 1])
    max_y = np.max(transformed_pts[:, 1])

    # Re-normalize to [0, 1000] and clip
    x1_res = int(np.clip(round((min_x / width) * 1000.0), 0, 1000))
    y1_res = int(np.clip(round((min_y / height) * 1000.0), 0, 1000))
    x2_res = int(np.clip(round((max_x / width) * 1000.0), 0, 1000))
    y2_res = int(np.clip(round((max_y / height) * 1000.0), 0, 1000))

    return [x1_res, y1_res, max(x1_res + 1, x2_res), max(y1_res + 1, y2_res)]


class DegradationRunner:
    """Manages deterministic degradation generation and caching."""

    def __init__(self, cache_dir: str | Path = "experiments/phase4/degraded"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def generate_degraded_sample(
        self,
        clean_sample: BenchmarkSample,
        condition: DegradationCondition,
    ) -> Tuple[BenchmarkSample, str]:
        """
        Generates or retrieves cached degraded variant of the clean sample.
        Returns the degraded sample and its cryptographic SHA-256 digest.
        """
        if condition.severity == 0 or condition.family == "clean":
            clean_sha = compute_sha256(clean_sample.image)
            return clean_sample, clean_sha

        cache_filename = (
            f"{clean_sample.document_id}_deg_{condition.family}"
            f"_sev{condition.severity}_seed{condition.seed}.png"
        )
        cache_path = self.cache_dir / cache_filename

        if cache_path.exists():
            degraded_img = Image.open(cache_path).convert("RGB")
            derived_sha = compute_sha256(degraded_img)
        else:
            degraded_img = apply_degradation(
                clean_sample.image,
                condition.family,
                condition.severity,
                seed=condition.seed,
            )
            degraded_img.save(cache_path, format="PNG")
            derived_sha = compute_sha256(degraded_img)

        # Transform bounding boxes
        w, h = clean_sample.image.size
        transformed_bboxes = [
            transform_bbox_geometric(box, condition.family, condition.severity, w, h)
            for box in clean_sample.ground_truth_bboxes
        ]

        degraded_sample = BenchmarkSample(
            sample_id=f"{clean_sample.sample_id}_deg_{condition.family}_s{condition.severity}",
            document_id=clean_sample.document_id,
            dataset=clean_sample.dataset,
            split=clean_sample.split,  # Enforces Zero-Leakage partition inheritance
            page_idx=clean_sample.page_idx,
            total_pages=clean_sample.total_pages,
            image_path=str(cache_path),
            image=degraded_img,
            task_type=clean_sample.task_type,
            question=clean_sample.question,
            ground_truth_answers=clean_sample.ground_truth_answers,
            ground_truth_bboxes=transformed_bboxes,
            source_sha256=clean_sample.source_sha256,
            metadata={
                **clean_sample.metadata,
                "degradation_family": condition.family,
                "severity": condition.severity,
                "parameter_name": condition.parameter_name,
                "parameter_value": condition.parameter_value,
                "seed": condition.seed,
                "derived_sha256": derived_sha,
            },
        )

        return degraded_sample, derived_sha
