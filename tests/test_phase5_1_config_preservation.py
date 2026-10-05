"""
Tests for Phase 5.1 Configuration Preservation.
Verifies that all 7 configuration files exist in configs/phase5_1/, parse correctly,
and adhere strictly to project protocols and candidate model schemas.
"""

from pathlib import Path
import yaml
import pytest


EXPECTED_CONFIG_FILES = [
    "routing_config.yaml",
    "router_rules.yaml",
    "uncertainty_config.yaml",
    "calibration_config.yaml",
    "cost_config.yaml",
    "experiment_matrix.yaml",
    "evaluation_config.yaml",
]


def test_all_phase5_1_configs_exist_and_parse():
    """Verify all 7 config files exist in configs/phase5_1/ and parse valid YAML."""
    cfg_dir = Path(__file__).resolve().parents[1] / "configs" / "phase5_1"
    assert cfg_dir.exists(), f"Configuration directory missing: {cfg_dir}"

    for filename in EXPECTED_CONFIG_FILES:
        path = cfg_dir / filename
        assert path.exists(), f"Missing configuration file: {filename}"
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            assert isinstance(data, dict), f"{filename} did not parse as dictionary"


def test_routing_config_schema_and_policies():
    """Verify routing master configuration matches required candidate models and policies."""
    path = Path(__file__).resolve().parents[1] / "configs" / "phase5_1" / "routing_config.yaml"
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    assert data.get("version") == "1.1.0"
    candidates = [m["id"] for m in data.get("candidate_models", [])]
    assert candidates == ["B0", "B1", "B2", "B0-U"]

    policies = data.get("active_policies", [])
    expected_policies = [
        "R0_ORACLE", "R1_FIXED_BEST", "R2_RULE_BASED",
        "R3_UNCERTAINTY", "R4_LEARNED", "R5_COMPOSITE"
    ]
    assert policies == expected_policies
    assert data.get("default_fixed_baseline") == "B2"
