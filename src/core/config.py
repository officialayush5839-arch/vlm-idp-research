"""
Configuration management and validation system for VLM-IDP research project.
Loads YAML configurations and strictly validates them against formal schemas.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, List, Optional
import yaml
from pydantic import BaseModel, Field, field_validator, model_validator


class ProjectMetaConfig(BaseModel):
    name: str
    title: str
    version: str
    stage: str
    target_venue: str
    type: str


class HardwareConfig(BaseModel):
    os: str
    python_version: str
    gpu: str
    vram_mb: int = Field(gt=0)
    quantization_default: str


class ResearchConfig(BaseModel):
    project: ProjectMetaConfig
    hardware_target: HardwareConfig
    primary_research_question: str
    secondary_research_questions: Dict[str, str]
    hypotheses: Dict[str, str]
    models: Dict[str, Any]

    @field_validator("hypotheses")
    @classmethod
    def validate_hypotheses_keys(cls, v: Dict[str, str]) -> Dict[str, str]:
        required = {"H1", "H2", "H3", "H4", "H5", "H6"}
        if not required.issubset(v.keys()):
            missing = required - set(v.keys())
            raise ValueError(f"Missing required hypotheses: {missing}")
        return v


class DatasetSpec(BaseModel):
    name: str
    type: str
    domain: str
    raw_path: str
    manifest_path: str
    zero_leakage_group_key: str = "document_id"
    splits: Optional[Dict[str, float]] = None

    @model_validator(mode="after")
    def validate_split_ratios(self) -> DatasetSpec:
        if self.splits:
            train = self.splits.get("train_ratio", 0.0)
            val = self.splits.get("val_ratio", 0.0)
            test = self.splits.get("test_ratio", 0.0)
            total = train + val + test
            if abs(total - 1.0) > 1e-4:
                raise ValueError(f"Split ratios for {self.name} must sum to 1.0, got {total}")
        return self


class DatasetConfig(BaseModel):
    datasets: Dict[str, DatasetSpec]


class DegradationFamilyConfig(BaseModel):
    name: str
    type: str
    parameter_name: Optional[str] = None
    severities: Dict[int, Dict[str, Any]]

    @field_validator("severities")
    @classmethod
    def validate_severities(cls, v: Dict[int, Dict[str, Any]]) -> Dict[int, Dict[str, Any]]:
        for s in v.keys():
            if s < 0 or s > 4:
                raise ValueError(f"Degradation severity level must be in range [0, 4], got {s}")
        if 0 not in v:
            raise ValueError("Baseline severity 0 (clean) must be defined for every degradation family.")
        return v


class DegradationConfig(BaseModel):
    degradation_benchmark: Dict[str, Any]

    @property
    def families(self) -> Dict[str, DegradationFamilyConfig]:
        raw_families = self.degradation_benchmark.get("families", {})
        return {k: DegradationFamilyConfig(**v) for k, v in raw_families.items()}


class EvaluationConfig(BaseModel):
    evaluation: Dict[str, Any]

    @property
    def primary_seeds(self) -> List[int]:
        seeds = self.evaluation.get("random_seeds", {}).get("primary_suite", [])
        if not seeds or any(s < 0 for s in seeds):
            raise ValueError(f"Invalid seeds list: {seeds}")
        return seeds


def load_yaml(path: str | Path) -> Dict[str, Any]:
    """Load and parse a YAML file."""
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"Configuration file not found: {path.resolve()}")
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError(f"Expected YAML file {path} to contain a dictionary, got {type(data)}")
    return data


def load_research_config(config_path: str | Path = "configs/phase0/research_config.yaml") -> ResearchConfig:
    data = load_yaml(config_path)
    return ResearchConfig(**data)


def load_dataset_config(config_path: str | Path = "configs/phase0/dataset_config.yaml") -> DatasetConfig:
    data = load_yaml(config_path)
    return DatasetConfig(**data)


def load_degradation_config(config_path: str | Path = "configs/phase0/degradation_config.yaml") -> DegradationConfig:
    data = load_yaml(config_path)
    return DegradationConfig(**data)


def load_evaluation_config(config_path: str | Path = "configs/phase0/evaluation_config.yaml") -> EvaluationConfig:
    data = load_yaml(config_path)
    return EvaluationConfig(**data)
