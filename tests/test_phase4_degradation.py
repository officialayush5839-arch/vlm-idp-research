"""
Unit Tests for Phase 4 Degradation Generation and Coordinate Preservation.
Strictly verifies Sections 9, 12, 13, 61, and 71 of the Phase 4 specification.
"""

import tempfile
from pathlib import Path
from PIL import Image
from src.benchmark.degradation_runner import DegradationRunner, transform_bbox_geometric
from src.benchmark.schema import BenchmarkSample, DegradationCondition


def test_all_nine_families_execution():
    with tempfile.TemporaryDirectory() as tmp_dir:
        runner = DegradationRunner(cache_dir=Path(tmp_dir))
        clean_img = Image.new("RGB", (300, 200), color=(250, 250, 250))
        sample = BenchmarkSample(
            sample_id="test_samp",
            document_id="doc_test",
            dataset="DocVQA",
            split="test",
            page_idx=0,
            total_pages=1,
            image=clean_img,
            task_type="vqa",
            question="What is the title?",
            ground_truth_answers=["Invoice"],
            ground_truth_bboxes=[[100, 100, 400, 300]],
            source_sha256="clean_hash",
        )

        families = [
            ("gaussian_blur", "sigma", 2.0),
            ("jpeg_compression", "quality", 50),
            ("gaussian_noise", "sigma", 15.0),
            ("skew_rotation", "angle_deg", 3.0),
            ("illumination", "alpha", 0.50),
            ("occlusion", "area_ratio", 0.10),
            ("resolution_reduction", "scale_factor", 0.50),
            ("perspective_distortion", "tilt_deg", 15.0),
            ("mixed_degradation", "tier", 2),
        ]

        for fam, param_name, param_val in families:
            cond = DegradationCondition(
                family=fam,
                severity=2,
                parameter_name=param_name,
                parameter_value=param_val,
                seed=42,
            )
            deg_sample, sha = runner.generate_degraded_sample(sample, cond)
            assert deg_sample.image.size == clean_img.size
            assert len(sha) == 64
            assert deg_sample.metadata["degradation_family"] == fam
            assert deg_sample.metadata["severity"] == 2


def test_bounding_box_coordinate_preservation():
    bbox = [100, 100, 300, 400]
    w, h = 600, 400

    # Clean / non-geometric corruptions do not move bbox
    assert transform_bbox_geometric(bbox, "gaussian_blur", 3, w, h) == bbox
    assert transform_bbox_geometric(bbox, "gaussian_noise", 3, w, h) == bbox
    assert transform_bbox_geometric(bbox, "jpeg_compression", 3, w, h) == bbox

    # Skew rotation moves bbox but keeps within [0, 1000]
    rot_bbox = transform_bbox_geometric(bbox, "skew_rotation", 3, w, h)
    assert len(rot_bbox) == 4
    for coord in rot_bbox:
        assert 0 <= coord <= 1000
    assert rot_bbox[0] < rot_bbox[2]
    assert rot_bbox[1] < rot_bbox[3]

    # Perspective distortion moves bbox but keeps within [0, 1000]
    persp_bbox = transform_bbox_geometric(bbox, "perspective_distortion", 3, w, h)
    assert len(persp_bbox) == 4
    for coord in persp_bbox:
        assert 0 <= coord <= 1000
    assert persp_bbox[0] < persp_bbox[2]
    assert persp_bbox[1] < persp_bbox[3]
