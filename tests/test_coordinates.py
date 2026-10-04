"""
Unit tests for coordinate normalization, denormalization, bounding box validation, and IoU.
"""

import pytest
from src.ingestion.coordinates import (
    BoundingBoxValidationError,
    compute_iou,
    denormalize_coordinates,
    normalize_coordinates,
    validate_pixel_bbox,
)


@pytest.mark.unit
class TestCoordinates:

    PAGE_WIDTH = 1000
    PAGE_HEIGHT = 2000

    def test_top_left_normalization(self):
        """Top-left corner box."""
        raw_box = [0, 0, 100, 200]
        norm = normalize_coordinates(raw_box, self.PAGE_WIDTH, self.PAGE_HEIGHT)
        assert norm == [0, 0, 100, 100]

    def test_bottom_right_normalization(self):
        """Bottom-right corner box."""
        raw_box = [900, 1800, 1000, 2000]
        norm = normalize_coordinates(raw_box, self.PAGE_WIDTH, self.PAGE_HEIGHT)
        assert norm == [900, 900, 1000, 1000]

    def test_center_box_normalization(self):
        """Centered bounding box."""
        raw_box = [250, 500, 750, 1500]
        norm = normalize_coordinates(raw_box, self.PAGE_WIDTH, self.PAGE_HEIGHT)
        assert norm == [250, 250, 750, 750]

    def test_round_trip_reversibility(self):
        """Test pixel -> normalized -> pixel round-trip within documented tolerance."""
        # Page size: 850 x 1100 (Standard Letter size at 100 DPI)
        w, h = 850, 1100
        original_box = [120.0, 340.0, 560.0, 780.0]

        norm = normalize_coordinates(original_box, w, h)
        recovered = denormalize_coordinates(norm, w, h)

        # Tolerance: At 1000 units resolution, max quantization error is <= 1.0 pixel
        for orig, rec in zip(original_box, recovered):
            assert abs(orig - rec) <= 1.5, f"Original: {orig}, Recovered: {rec}"

    def test_negative_coordinate_rejected(self):
        """Negative coordinates must raise BoundingBoxValidationError."""
        with pytest.raises(BoundingBoxValidationError, match="Negative coordinates"):
            validate_pixel_bbox([-10, 50, 100, 100], self.PAGE_WIDTH, self.PAGE_HEIGHT)

    def test_out_of_bounds_rejected(self):
        """Coordinates exceeding page dimensions must raise BoundingBoxValidationError."""
        with pytest.raises(BoundingBoxValidationError, match="exceed page bounds"):
            validate_pixel_bbox([0, 0, 1050, 200], self.PAGE_WIDTH, self.PAGE_HEIGHT)

    def test_inverted_coordinates_rejected(self):
        """Inverted boxes where x1 < x0 or y1 < y0 must be rejected."""
        with pytest.raises(BoundingBoxValidationError, match="Inverted bounding box"):
            validate_pixel_bbox([500, 500, 400, 600], self.PAGE_WIDTH, self.PAGE_HEIGHT)

    def test_compute_iou_identical_boxes(self):
        """IoU of identical boxes must be 1.0."""
        box = [100, 100, 200, 200]
        assert compute_iou(box, box) == 1.0

    def test_compute_iou_disjoint_boxes(self):
        """IoU of completely disjoint boxes must be 0.0."""
        box_a = [0, 0, 50, 50]
        box_b = [100, 100, 150, 150]
        assert compute_iou(box_a, box_b) == 0.0

    def test_compute_iou_half_overlap(self):
        """IoU calculation for known 50% spatial overlap."""
        box_a = [0, 0, 100, 100]      # Area 10,000
        box_b = [50, 0, 150, 100]      # Area 10,000, Inter: 50x100 = 5000, Union: 15000
        expected = 5000.0 / 15000.0     # 1/3
        assert abs(compute_iou(box_a, box_b) - expected) < 1e-5
