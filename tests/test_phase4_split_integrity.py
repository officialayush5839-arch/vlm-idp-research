"""
Unit Tests for Zero-Leakage Split Integrity and Partition Inheritance.
Strictly verifies Section 6 and 70 of the Phase 4 specification.
"""

import tempfile
from pathlib import Path
from PIL import Image
from src.benchmark.manifest import ManifestManager, compute_sha256
from src.benchmark.degradation_runner import DegradationRunner
from src.benchmark.schema import BenchmarkSample, DegradationCondition


def test_zero_leakage_manifest_partition_inheritance():
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        mgr = ManifestManager(
            raw_dir=tmp_path / "raw",
            manifest_dir=tmp_path / "manifests",
            splits_dir=tmp_path / "splits",
        )
        samples = mgr.generate_standard_evaluation_corpus()
        assert len(samples) >= 4

        deg_runner = DegradationRunner(cache_dir=tmp_path / "degraded")

        for sample in samples:
            assert sample.split == "test"
            # Verify clean sample zero leakage
            assert mgr.verify_zero_leakage(sample.document_id, sample.sample_id, "test")
            assert not mgr.verify_zero_leakage(sample.document_id, sample.sample_id, "train")
            assert not mgr.verify_zero_leakage(sample.document_id, sample.sample_id, "val")

            # Generate degraded variant
            cond = DegradationCondition(
                family="gaussian_blur",
                severity=3,
                parameter_name="sigma",
                parameter_value=4.0,
                seed=42,
            )
            deg_sample, _ = deg_runner.generate_degraded_sample(sample, cond)

            # Invariant: Derived variant partition MUST be identical to source
            assert deg_sample.split == sample.split
            assert deg_sample.document_id == sample.document_id
            assert mgr.verify_zero_leakage(deg_sample.document_id, deg_sample.sample_id, "test")
            assert not mgr.verify_zero_leakage(deg_sample.document_id, deg_sample.sample_id, "train")


def test_cryptographic_document_hashing_invariance():
    img = Image.new("RGB", (200, 200), color=(240, 240, 240))
    sha_1 = compute_sha256(img)
    sha_2 = compute_sha256(img)
    assert sha_1 == sha_2
    assert len(sha_1) == 64
