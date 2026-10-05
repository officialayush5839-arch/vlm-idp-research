"""
Unit tests for Phase 7 Spatial Region Validation and Coordinate Arithmetic.
"""

import pytest
from src.evidence.region_validator import (
    clip_bbox_1000,
    is_valid_bbox_1000,
    bbox_1000_to_pixel,
    pixel_to_bbox_1000,
    compute_iou,
    compute_containment,
    SpatialRegionValidator
)


def test_clip_bbox_1000():
    # Out of bounds and inverted coordinates
    raw = (-50, 1050, 800, 200)
    clipped = clip_bbox_1000(raw)
    assert clipped[0] == 0
    assert clipped[1] == 200
    assert clipped[2] == 800
    assert clipped[3] == 1000


def test_is_valid_bbox_1000():
    assert is_valid_bbox_1000((100, 100, 500, 500)) is True
    # Zero width
    assert is_valid_bbox_1000((100, 100, 100, 500)) is False
    # Negative coord
    assert is_valid_bbox_1000((-10, 100, 500, 500)) is False
    # Over 1000
    assert is_valid_bbox_1000((100, 100, 500, 1050)) is False


def test_coordinate_conversions():
    page_w, page_h = 2000, 1000
    bbox_1000 = (100, 200, 500, 800)
    px = bbox_1000_to_pixel(bbox_1000, page_w, page_h)
    assert px == (200, 200, 1000, 800)

    back_1000 = pixel_to_bbox_1000(px, page_w, page_h)
    assert back_1000 == bbox_1000


def test_compute_iou():
    box1 = (100, 100, 300, 300)  # area 200*200 = 40,000
    box2 = (200, 200, 400, 400)  # area 200*200 = 40,000
    # intersection: [200, 200, 300, 300] = 100*100 = 10,000
    # union = 40000 + 40000 - 10000 = 70,000
    # IoU = 10000 / 70000 = 1/7 ~= 0.142857
    iou = compute_iou(box1, box2)
    assert pytest.approx(iou, 1e-4) == 0.142857

    # Identical
    assert compute_iou(box1, box1) == 1.0

    # Disjoint
    box3 = (400, 400, 600, 600)
    assert compute_iou(box1, box3) == 0.0


def test_compute_containment():
    outer = (100, 100, 500, 500)
    inner = (200, 200, 300, 300)
    # inner is completely inside outer
    assert compute_containment(inner, outer) == 1.0
    # outer is partially inside inner
    assert compute_containment(outer, inner) < 1.0


def test_spatial_region_validator():
    validator = SpatialRegionValidator(
        iou_threshold_relaxed=0.50,
        iou_threshold_strict=0.75,
        min_region_area=100
    )

    gt_boxes = [
        (100, 100, 300, 300),
        (500, 500, 800, 800)
    ]

    # Perfect match on first gt
    res_exact = validator.validate_region((100, 100, 300, 300), gt_boxes)
    assert res_exact["max_iou"] == 1.0
    assert res_exact["passes_relaxed"] is True
    assert res_exact["passes_strict"] is True
    assert res_exact["best_match_index"] == 0

    # Strict failure, relaxed pass (e.g. 60% IoU)
    # Box with high overlap: (100, 100, 300, 250) -> area 200*150 = 30000. inter=30000, union=40000 -> IoU = 0.75
    # Let's test a box with IoU ~ 0.60
    cand_partial = (100, 100, 300, 230)
    res_part = validator.validate_region(cand_partial, gt_boxes)
    assert res_part["passes_relaxed"] is True
    assert res_part["passes_strict"] is False

    # Complete miss
    res_miss = validator.validate_region((900, 900, 950, 950), gt_boxes)
    assert res_miss["max_iou"] == 0.0
    assert res_miss["passes_relaxed"] is False
    assert res_miss["passes_strict"] is False
