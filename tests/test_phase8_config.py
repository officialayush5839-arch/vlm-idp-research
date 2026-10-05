"""
Unit tests for Phase 8 Configuration Loading.
"""

import os
import yaml


def test_phase8_configs_exist_and_parse():
    config_dir = "configs/phase8"
    expected_configs = [
        "uncertainty_config.yaml",
        "calibration_config.yaml",
        "abstention_config.yaml",
        "evaluation_config.yaml",
        "experiment_matrix.yaml"
    ]

    for cfg_name in expected_configs:
        path = os.path.join(config_dir, cfg_name)
        assert os.path.exists(path), f"Missing config: {path}"
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            assert data is not None
            assert data.get("phase") == "PHASE_8"
