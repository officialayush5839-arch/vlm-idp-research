"""Unit tests for Phase 9 configuration files."""

from pathlib import Path
import yaml
import pytest

CONFIG_DIR = Path(__file__).resolve().parent.parent / "configs" / "phase9"

EXPECTED_FILES = [
    "reliability_config.yaml",
    "uncertainty_config.yaml",
    "calibration_config.yaml",
    "abstention_config.yaml",
    "threshold_config.yaml",
    "experiment_matrix.yaml",
    "evaluation_config.yaml",
]


def test_all_config_files_exist():
    for fname in EXPECTED_FILES:
        path = CONFIG_DIR / fname
        assert path.exists(), f"Configuration file missing: {fname}"


@pytest.mark.parametrize("fname", EXPECTED_FILES)
def test_valid_yaml_syntax(fname):
    path = CONFIG_DIR / fname
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    assert isinstance(data, dict), f"Config {fname} did not parse as a dict"
    assert len(data) > 0, f"Config {fname} is empty"


def test_reliability_config_structure():
    with open(CONFIG_DIR / "reliability_config.yaml", "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    assert "pipeline" in cfg
    assert "confidence_model" in cfg
    assert "decision_policy" in cfg
    assert "failure_analysis" in cfg
    assert len(cfg["decision_policy"]["levels"]) == 4


def test_uncertainty_config_dimensions():
    with open(CONFIG_DIR / "uncertainty_config.yaml", "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    assert cfg["uncertainty_vector"]["dimensions"] == 8
    assert len(cfg["uncertainty_vector"]["features"]) == 8


def test_calibration_split_isolation():
    with open(CONFIG_DIR / "calibration_config.yaml", "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    assert cfg["calibration"]["dataset_split"] == "val", "Calibration must strictly use val split"


def test_experiment_matrix_baselines_and_seeds():
    with open(CONFIG_DIR / "experiment_matrix.yaml", "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    baseline_ids = [b["id"] for b in cfg["baselines"]]
    assert baseline_ids == ["B9-0", "B9-1", "B9-2", "B9-3", "B9-4", "B9-5"]
    assert cfg["evaluation_seeds"] == [42, 123, 456, 789, 101112]
    assert cfg["bootstrap_replications"] == 10000
    assert cfg["hypothesis"] == "H9"
