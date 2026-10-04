"""
Configuration management and validation for Phase 3 Quality Assessment.
Computes SHA-256 hashes for configuration provenance.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List, Optional
import yaml
from pydantic import BaseModel, Field

from src.core.config import load_yaml


class FeatureExtractorConfig(BaseModel):
    method: str
    direction: str = "higher_is_worse"
    clean_threshold: float
    severe_threshold: float
    params: Dict[str, Any] = Field(default_factory=dict)


class QualityConfig(BaseModel):
    algorithm_version: str = "1.0.0"
    enabled: bool = True
    fail_fast: bool = False
    preprocessing: Dict[str, Any] = Field(default_factory=dict)
    feature_flags: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
    feature_specs: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
    severity_thresholds: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
    config_hash: str = ""


def compute_dict_hash(data: Dict[str, Any]) -> str:
    """Compute deterministic SHA-256 hash of a dictionary."""
    serialized = json.dumps(data, sort_keys=True, default=str).encode("utf-8")
    return hashlib.sha256(serialized).hexdigest()[:16]


def load_phase3_quality_config(
    quality_config_path: str | Path = "configs/phase3/quality_config.yaml",
    feature_config_path: str | Path = "configs/phase3/feature_config.yaml",
    severity_config_path: str | Path = "configs/phase3/severity_config.yaml",
) -> QualityConfig:
    """Loads and links all Phase 3 YAML configs with SHA-256 provenance hash."""
    q_data = load_yaml(quality_config_path).get("quality_pipeline", {})
    f_data = load_yaml(feature_config_path).get("features", {})
    s_data = load_yaml(severity_config_path).get("severity_mapping", {}).get("thresholds", {})

    combined_dict = {
        "pipeline": q_data,
        "features": f_data,
        "severities": s_data,
    }
    config_hash = compute_dict_hash(combined_dict)

    return QualityConfig(
        algorithm_version=q_data.get("algorithm_version", "1.0.0"),
        enabled=q_data.get("enabled", True),
        fail_fast=q_data.get("fail_fast", False),
        preprocessing=q_data.get("preprocessing", {}),
        feature_flags=q_data.get("features", {}),
        feature_specs=f_data,
        severity_thresholds=s_data,
        config_hash=config_hash,
    )
