"""
Unit tests for configuration loading and validation system.
Ensures invalid configurations fail early with explicit errors.
"""

import pytest
from pydantic import ValidationError
from src.core.config import (
    DatasetSpec,
    DegradationFamilyConfig,
    EvaluationConfig,
    ResearchConfig,
    load_dataset_config,
    load_degradation_config,
    load_evaluation_config,
    load_research_config,
)


@pytest.mark.unit
class TestConfigValidation:

    def test_load_phase0_research_config(self):
        """Verify that the official Phase 0 research config validates against schema."""
        cfg = load_research_config("configs/phase0/research_config.yaml")
        assert cfg.project.name == "vlm-idp-research"
        assert "H1" in cfg.hypotheses
        assert "H6" in cfg.hypotheses
        assert cfg.hardware_target.vram_mb == 6144

    def test_load_phase0_dataset_config(self):
        """Verify that the official Phase 0 dataset config validates against schema."""
        cfg = load_dataset_config("configs/phase0/dataset_config.yaml")
        assert "docvqa" in cfg.datasets
        assert "funsd" in cfg.datasets
        assert cfg.datasets["docvqa"].zero_leakage_group_key == "document_id"

    def test_load_phase0_degradation_config(self):
        """Verify that the official Phase 0 degradation config validates against schema."""
        cfg = load_degradation_config("configs/phase0/degradation_config.yaml")
        assert "gaussian_blur" in cfg.families
        assert 0 in cfg.families["gaussian_blur"].severities
        assert 4 in cfg.families["gaussian_blur"].severities

    def test_load_phase0_evaluation_config(self):
        """Verify that the official Phase 0 evaluation config validates against schema."""
        cfg = load_evaluation_config("configs/phase0/evaluation_config.yaml")
        assert 42 in cfg.primary_seeds
        assert len(cfg.primary_seeds) >= 3

    def test_negative_severity_rejected(self):
        """Severity levels outside [0, 4] must raise ValidationError."""
        invalid_severities = {
            -1: {"sigma": 1.0},
            0: {"sigma": 0.0}
        }
        with pytest.raises(ValidationError, match="severity level must be in range"):
            DegradationFamilyConfig(
                name="Invalid",
                type="test",
                severities=invalid_severities
            )

    def test_missing_severity_zero_rejected(self):
        """Missing baseline severity 0 must raise ValidationError."""
        invalid_severities = {
            1: {"sigma": 1.0},
            2: {"sigma": 2.0}
        }
        with pytest.raises(ValidationError, match="Baseline severity 0"):
            DegradationFamilyConfig(
                name="Invalid",
                type="test",
                severities=invalid_severities
            )

    def test_invalid_split_ratios_rejected(self):
        """Split ratios not summing to 1.0 must raise ValidationError."""
        with pytest.raises(ValidationError, match="must sum to 1.0"):
            DatasetSpec(
                name="BrokenSplit",
                type="test",
                domain="test",
                raw_path="data/raw/test",
                manifest_path="data/manifests/test.json",
                splits={"train_ratio": 0.50, "val_ratio": 0.20, "test_ratio": 0.10}  # Sum = 0.80
            )

    def test_missing_hypotheses_rejected(self):
        """ResearchConfig missing mandatory hypotheses must raise ValidationError."""
        raw_data = {
            "project": {
                "name": "p", "title": "t", "version": "1.0",
                "stage": "s", "target_venue": "v", "type": "t"
            },
            "hardware_target": {
                "os": "Windows", "python_version": "3.14",
                "gpu": "GPU", "vram_mb": 6000, "quantization_default": "4bit"
            },
            "primary_research_question": "PRQ",
            "secondary_research_questions": {"RQ1": "q1"},
            "hypotheses": {"H1": "h1"},  # Missing H2-H6
            "models": {}
        }
        with pytest.raises(ValidationError, match="Missing required hypotheses"):
            ResearchConfig(**raw_data)
