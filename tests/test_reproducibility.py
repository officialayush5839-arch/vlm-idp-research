"""
Unit tests for reproducibility utilities, environment logging, and run manifests.
"""

import json
import random
import numpy as np
import pytest
from src.evaluation.reproducibility import (
    create_run_id,
    get_environment_info,
    get_git_commit,
    seed_everything,
    write_run_manifest,
)


@pytest.mark.reproducibility
class TestReproducibility:

    def test_seed_everything_deterministic_numpy(self):
        """Setting seed must generate identical random sequences."""
        seed_everything(12345)
        arr1 = np.random.randn(5)

        seed_everything(12345)
        arr2 = np.random.randn(5)

        np.testing.assert_array_equal(arr1, arr2)

    def test_seed_everything_deterministic_python_random(self):
        """Setting seed must generate identical python random choices."""
        seed_everything(999)
        seq1 = [random.randint(0, 1000) for _ in range(10)]

        seed_everything(999)
        seq2 = [random.randint(0, 1000) for _ in range(10)]

        assert seq1 == seq2

    def test_get_environment_info_structure(self):
        """Environment info must contain all required provenance fields."""
        info = get_environment_info()
        assert "os" in info
        assert "python_version" in info
        assert "git_commit" in info
        assert "timestamp_utc" in info
        assert "cuda_available" in info

    def test_get_git_commit_returns_valid_string(self):
        """Git commit must return a non-empty string."""
        commit = get_git_commit()
        assert isinstance(commit, str)
        assert len(commit) > 0

    def test_create_run_id_unique_and_formatted(self):
        """Run ID must contain prefix and seed."""
        run_id = create_run_id(prefix="exp_test", seed=42)
        assert run_id.startswith("exp_test_")
        assert "_s42" in run_id

    def test_write_run_manifest(self, tmp_path):
        """Run manifest must write a valid JSON file with configuration and metrics."""
        run_id = "test_run_001"
        config = {"model": "Qwen2.5-VL-7B", "batch_size": 1}
        metrics = {"f1": 0.88, "anls": 0.85}

        manifest_path = write_run_manifest(
            run_id=run_id,
            output_dir=tmp_path,
            config=config,
            metrics=metrics,
            seed=42,
            status="COMPLETED"
        )

        assert manifest_path.is_file()
        with open(manifest_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert data["run_id"] == run_id
        assert data["seed"] == 42
        assert data["metrics"]["f1"] == 0.88
        assert data["configuration"]["model"] == "Qwen2.5-VL-7B"
        assert "environment" in data
