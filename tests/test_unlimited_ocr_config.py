"""Unit Tests for Unlimited-OCR Configuration."""

from pathlib import Path
import yaml


def test_unlimited_ocr_config_exists_and_valid():
    """Verify configs/phase2_5/unlimited_ocr_config.yaml is complete and frozen."""
    config_path = Path("configs/phase2_5/unlimited_ocr_config.yaml")
    assert config_path.exists(), "unlimited_ocr_config.yaml must exist"

    with open(config_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    assert data["model_identity"]["name"] == "Unlimited-OCR"
    assert data["model_identity"]["huggingface_repo"] == "baidu/Unlimited-OCR"
    assert len(data["model_identity"]["revision"]) == 40
    assert data["model_identity"]["parameter_count"] == "3.3B"
    assert data["model_identity"]["license"] == "MIT"
    assert data["baseline_identity"]["baseline_id"] == "B0-U"
    assert data["grounding_and_coordinates"]["coordinate_space"] == [0, 1000]
