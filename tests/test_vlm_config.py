"""Unit Tests for Phase 2 Model & Baseline Configuration Files."""

import yaml
from pathlib import Path


def test_model_config_loading():
    """Verify configs/phase2/model_config.yaml is valid and frozen."""
    config_path = Path("configs/phase2/model_config.yaml")
    assert config_path.exists()

    with open(config_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    assert "model_identity" in data
    assert data["model_identity"]["name"] == "Qwen2.5-VL-7B-Instruct"
    assert data["model_identity"]["huggingface_repo"] == "Qwen/Qwen2.5-VL-7B-Instruct"
    assert len(data["model_identity"]["revision"]) == 40  # Full SHA commit hash
    assert data["generation_parameters"]["temperature"] == 0.0
    assert data["generation_parameters"]["do_sample"] is False


def test_baseline_config_loading():
    """Verify configs/phase2/baseline_config.yaml defines B0, B1, B2."""
    config_path = Path("configs/phase2/baseline_config.yaml")
    assert config_path.exists()

    with open(config_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    assert "baselines" in data
    assert "B0" in data["baselines"]
    assert "B1" in data["baselines"]
    assert "B2" in data["baselines"]
    assert data["fairness_safeguards"]["identical_document_identity"] is True
