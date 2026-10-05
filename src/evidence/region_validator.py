"""
Spatial Region Validation and Coordinate Arithmetic for Phase 7 Evidence Grounding.
Operates on normalized integer coordinates in range [0, 1000] and converts
to absolute pixel space.
"""

from typing import Tuple, List, Dict, Any, Optional
import math


def clip_bbox_1000(bbox: Tuple[int, int, int, int]) -> Tuple[int, int, int, int]:
    """
    Clip bounding box coordinates to valid normalized range [0, 1000].
    Enforces x_min <= x_max and y_min <= y_max.
    """
    xmin, ymin, xmax, ymax = bbox
    xmin = max(0, min(1000, int(xmin)))
    ymin = max(0, min(1000, int(ymin)))
    xmax = max(0, min(1000, int(xmax)))
    ymax = max(0, min(1000, int(ymax)))

    if xmin > xmax:
        xmin, xmax = xmax, xmin
    if ymin > ymax:
        ymin, ymax = ymax, ymin

    return (xmin, ymin, xmax, ymax)


def is_valid_bbox_1000(bbox: Tuple[int, int, int, int], min_area: int = 1) -> bool:
    """
    Check if bounding box is non-degenerate and within [0, 1000].
    """
    xmin, ymin, xmax, ymax = bbox
    if not (0 <= xmin <= 1000 and 0 <= ymin <= 1000 and 0 <= xmax <= 1000 and 0 <= ymax <= 1000):
        return False
    if xmax <= xmin or ymax <= ymin:
        return False
    area = (xmax - xmin) * (ymax - ymin)
    return area >= min_area


def bbox_1000_to_pixel(
    bbox_1000: Tuple[int, int, int, int],
    page_width_px: int,
    page_height_px: int
) -> Tuple[int, int, int, int]:
    """
    Convert normalized [0, 1000] coordinates to absolute pixel coordinates.
    """
    xmin, ymin, xmax, ymax = clip_bbox_1000(bbox_1000)
    px_xmin = int(round((xmin / 1000.0) * page_width_px))
    px_ymin = int(round((ymin / 1000.0) * page_height_px))
    px_xmax = int(round((xmax / 1000.0) * page_width_px))
    px_ymax = int(round((ymax / 1000.0) * page_height_px))
    return (px_xmin, px_ymin, px_xmax, px_ymax)


def pixel_to_bbox_1000(
    bbox_pixel: Tuple[int, int, int, int],
    page_width_px: int,
    page_height_px: int
) -> Tuple[int, int, int, int]:
    """
    Convert absolute pixel coordinates to normalized [0, 1000] coordinates.
    """
    if page_width_px <= 0 or page_height_px <= 0:
        raise ValueError(f"Page dimensions must be > 0. Got: {page_width_px}x{page_height_px}")
    px_xmin, px_ymin, px_xmax, px_ymax = bbox_pixel
    norm_xmin = int(round((max(0, px_xmin) / page_width_px) * 1000.0))
    norm_ymin = int(round((max(0, px_ymin) / page_height_px) * 1000.0))
    norm_xmax = int(round((min(page_width_px, px_xmax) / page_width_px) * 1000.0))
    norm_ymax = int(round((min(page_height_px, px_ymax) / page_height_px) * 1000.0))
    return clip_bbox_1000((norm_xmin, norm_ymin, norm_xmax, norm_ymax))


def compute_iou(
    box1: Tuple[int, int, int, int],
    box2: Tuple[int, int, int, int]
) -> float:
    """
    Compute Intersection over Union (IoU) between two bounding boxes.
    Assumes (x_min, y_min, x_max, y_max).
    Returns value in [0.0, 1.0].
    """
    x1_min, y1_min, x1_max, y1_max = clip_bbox_1000(box1)
    x2_min, y2_min, x2_max, y2_max = clip_bbox_1000(box2)

    inter_xmin = max(x1_min, x2_min)
    inter_ymin = max(y1_min, y2_min)
    inter_xmax = min(x1_max, x2_max)
    inter_ymax = min(y1_max, y2_max)

    if inter_xmax <= inter_xmin or inter_ymax <= inter_ymin:
        return 0.0

    inter_area = (inter_xmax - inter_xmin) * (inter_ymax - inter_ymin)
    area1 = (x1_max - x1_min) * (y1_max - y1_min)
    area2 = (x2_max - x2_min) * (y2_max - y2_min)

    union_area = area1 + area2 - inter_area
    if union_area <= 0:
        return 0.0

    return round(float(inter_area) / float(union_area), 6)


def compute_containment(
    candidate_box: Tuple[int, int, int, int],
    target_box: Tuple[int, int, int, int]
) -> float:
    """
    Compute proportion of candidate_box contained within target_box.
    Returns value in [0.0, 1.0].
    """
    x1_min, y1_min, x1_max, y1_max = clip_bbox_1000(candidate_box)
    x2_min, y2_min, x2_max, y2_max = clip_bbox_1000(target_box)

    inter_xmin = max(x1_min, x2_min)
    inter_ymin = max(y1_min, y2_min)
    inter_xmax = min(x1_max, x2_max)
    inter_ymax = min(y1_max, y2_max)

    if inter_xmax <= inter_xmin or inter_ymax <= inter_ymin:
        return 0.0

    inter_area = (inter_xmax - inter_xmin) * (inter_ymax - inter_ymin)
    cand_area = (x1_max - x1_min) * (y1_max - y1_min)
    if cand_area <= 0:
        return 0.0

    return round(float(inter_area) / float(cand_area), 6)


class SpatialRegionValidator:
    """
    Validates spatial regions against ground-truth or candidate layout annotations.
    Configured with strict and relaxed IoU thresholds.
    """

    def __init__(
        self,
        iou_threshold_relaxed: float = 0.50,
        iou_threshold_strict: float = 0.75,
        min_region_area: int = 100
    ):
        self.iou_threshold_relaxed = iou_threshold_relaxed
        self.iou_threshold_strict = iou_threshold_strict
        self.min_region_area = min_region_area

    def validate_region(
        self,
        candidate_bbox: Tuple[int, int, int, int],
        ground_truth_bboxes: List[Tuple[int, int, int, int]]
    ) -> Dict[str, Any]:
        """
        Evaluate candidate box against a list of ground-truth boxes on the same page.
        """
        if not is_valid_bbox_1000(candidate_bbox, min_area=self.min_region_area):
            return {
                "max_iou": 0.0,
                "passes_relaxed": False,
                "passes_strict": False,
                "best_match_box": None,
                "best_match_index": -1,
                "is_valid_geometry": False
            }

        if not ground_truth_bboxes:
            return {
                "max_iou": 0.0,
                "passes_relaxed": False,
                "passes_strict": False,
                "best_match_box": None,
                "best_match_index": -1,
                "is_valid_geometry": True
            }

        best_iou = 0.0
        best_box = None
        best_idx = -1

        for idx, gt_box in enumerate(ground_truth_bboxes):
            iou = compute_iou(candidate_bbox, gt_box)
            if iou > best_iou:
                best_iou = iou
                best_box = gt_box
                best_idx = idx

        return {
            "max_iou": best_iou,
            "passes_relaxed": best_iou >= self.iou_threshold_relaxed,
            "passes_strict": best_iou >= self.iou_threshold_strict,
            "best_match_box": best_box,
            "best_match_index": best_idx,
            "is_valid_geometry": True
        }
