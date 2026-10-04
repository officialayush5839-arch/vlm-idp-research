"""
Coordinate normalization, inverse mapping, and bounding box validation.
Ensures rigorous conversion between pixel coordinates and normalized [0, 1000] space.
"""

from __future__ import annotations

from typing import List, Sequence, Tuple


class BoundingBoxValidationError(ValueError):
    """Raised when a bounding box violates geometric or coordinate invariants."""
    pass


def validate_pixel_bbox(
    bbox: Sequence[float],
    page_width: int,
    page_height: int
) -> Tuple[float, float, float, float]:
    """
    Validate raw pixel bounding box [x0, y0, x1, y1] against page boundaries.
    
    Raises:
        BoundingBoxValidationError if coordinates are negative, inverted, or outside page.
    """
    if len(bbox) != 4:
        raise BoundingBoxValidationError(f"Bounding box must contain exactly 4 coordinates, got {len(bbox)}")

    x0, y0, x1, y1 = bbox

    if page_width <= 0 or page_height <= 0:
        raise BoundingBoxValidationError(f"Invalid page dimensions: {page_width}x{page_height}")

    if x0 < 0 or y0 < 0:
        raise BoundingBoxValidationError(f"Negative coordinates not allowed: ({x0}, {y0})")

    if x1 > page_width or y1 > page_height:
        raise BoundingBoxValidationError(
            f"Coordinates exceed page bounds ({page_width}, {page_height}): ({x1}, {y1})"
        )

    if x1 < x0 or y1 < y0:
        raise BoundingBoxValidationError(f"Inverted bounding box coordinates: [{x0}, {y0}, {x1}, {y1}]")

    return float(x0), float(y0), float(x1), float(y1)


def normalize_coordinates(
    bbox: Sequence[float],
    page_width: int,
    page_height: int
) -> List[int]:
    """
    Normalize pixel coordinates [x0, y0, x1, y1] to integer range [0, 1000].
    
    Returns:
        [nx0, ny0, nx1, ny1] integers in range [0, 1000]
    """
    x0, y0, x1, y1 = validate_pixel_bbox(bbox, page_width, page_height)

    nx0 = int(round((x0 / page_width) * 1000.0))
    ny0 = int(round((y0 / page_height) * 1000.0))
    nx1 = int(round((x1 / page_width) * 1000.0))
    ny1 = int(round((y1 / page_height) * 1000.0))

    # Clamp to [0, 1000] for floating point rounding boundaries
    nx0 = max(0, min(1000, nx0))
    ny0 = max(0, min(1000, ny0))
    nx1 = max(0, min(1000, nx1))
    ny1 = max(0, min(1000, ny1))

    return [nx0, ny0, nx1, ny1]


def denormalize_coordinates(
    norm_bbox: Sequence[int],
    page_width: int,
    page_height: int
) -> List[float]:
    """
    Map normalized coordinates [0, 1000] back to original pixel dimensions.
    
    Returns:
        [x0, y0, x1, y1] in pixel units.
    """
    if len(norm_bbox) != 4:
        raise BoundingBoxValidationError(f"Normalized box must contain 4 elements, got {len(norm_bbox)}")

    nx0, ny0, nx1, ny1 = norm_bbox

    for val in (nx0, ny0, nx1, ny1):
        if val < 0 or val > 1000:
            raise BoundingBoxValidationError(f"Normalized coordinate {val} outside [0, 1000]")

    if nx1 < nx0 or ny1 < ny0:
        raise BoundingBoxValidationError(f"Inverted normalized coordinates: {norm_bbox}")

    x0 = (nx0 / 1000.0) * page_width
    y0 = (ny0 / 1000.0) * page_height
    x1 = (nx1 / 1000.0) * page_width
    y1 = (ny1 / 1000.0) * page_height

    return [x0, y0, x1, y1]


def compute_iou(box_a: Sequence[float], box_b: Sequence[float]) -> float:
    """
    Compute Intersection-over-Union (IoU) between two bounding boxes.
    Boxes formatted as [x0, y0, x1, y1].
    """
    inter_x0 = max(box_a[0], box_b[0])
    inter_y0 = max(box_a[1], box_b[1])
    inter_x1 = min(box_a[2], box_b[2])
    inter_y1 = min(box_a[3], box_b[3])

    inter_w = max(0.0, inter_x1 - inter_x0)
    inter_h = max(0.0, inter_y1 - inter_y0)
    inter_area = inter_w * inter_h

    area_a = max(0.0, box_a[2] - box_a[0]) * max(0.0, box_a[3] - box_a[1])
    area_b = max(0.0, box_b[2] - box_b[0]) * max(0.0, box_b[3] - box_b[1])

    union_area = area_a + area_b - inter_area
    if union_area <= 0:
        return 0.0

    return inter_area / union_area
