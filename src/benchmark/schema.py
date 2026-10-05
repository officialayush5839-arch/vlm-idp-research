"""
Benchmark Schemas and Data Models for Phase 4 Controlled Degradation Benchmark.
Strictly compliant with Phase 0 protocols and Phase 4 requirements.
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, ConfigDict


class TaskType(str, Enum):
    VQA = "visual_question_answering"
    FORM = "form_understanding"
    RECEIPT = "receipt_extraction"
    MULTIPAGE_VQA = "multipage_vqa"


class DatasetSplit(str, Enum):
    TRAIN = "train"
    VAL = "val"
    TEST = "test"


class BenchmarkSample(BaseModel):
    """Encapsulates a document sample with task metadata and provenance."""
    model_config = ConfigDict(arbitrary_types_allowed=True)

    sample_id: str
    document_id: str
    dataset: str
    split: str = "test"
    page_idx: int = 0
    total_pages: int = 1
    image_path: Optional[str] = None
    image: Any = Field(default=None, description="PIL Image instance", exclude=True)
    task_type: str = "visual_question_answering"
    question: str
    ground_truth_answers: List[str] = Field(default_factory=list)
    ground_truth_bboxes: List[List[int]] = Field(default_factory=list, description="[x1, y1, x2, y2] in [0, 1000]")
    source_sha256: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


class DegradationCondition(BaseModel):
    """Specification of a controlled degradation condition."""
    family: str
    severity: int = Field(ge=0, le=4)
    parameter_name: str
    parameter_value: Any
    seed: int = 42


class ModelExecutionResult(BaseModel):
    """Standardized output of a baseline model execution."""
    model_id: str
    model_name: str
    revision_sha: str
    prompt_version: Optional[str] = None
    prompt_hash: Optional[str] = None
    device: str = "cpu"
    dtype: str = "float32"
    quantization: str = "none"
    answer: str
    predicted_bboxes: List[List[int]] = Field(default_factory=list)
    latency_ms: float = 0.0
    status: str = "SUCCESS"
    error_type: Optional[str] = None
    error_message: Optional[str] = None


class EvaluationMetricsResult(BaseModel):
    """Task-level and character-level evaluation metrics."""
    exact_match: float
    token_f1: float
    anls: float
    cer: Optional[float] = None
    wer: Optional[float] = None
    grounding_iou: Optional[float] = None
    primary_metric_name: str = "token_f1"
    primary_metric_value: float = 0.0


class BenchmarkRunArtifact(BaseModel):
    """Complete machine-readable JSON artifact for each benchmark execution."""
    experiment_id: str
    benchmark_version: str = "1.0.0"
    dataset: str
    sample_id: str
    document_id: str
    page_idx: int = 0
    split: str
    model: str
    degradation_family: str
    severity: int
    seed: int

    input: Dict[str, Any] = Field(
        description="Cryptographic provenance of input images",
        default_factory=lambda: {"source_sha256": "", "derived_sha256": ""},
    )

    degradation_params: Dict[str, Any] = Field(default_factory=dict)

    model_metadata: Dict[str, Any] = Field(default_factory=dict)

    prediction: str
    ground_truth: List[str]

    metrics: Dict[str, Any] = Field(default_factory=dict)

    quality_assessment: Optional[Dict[str, Any]] = None

    runtime: Dict[str, Any] = Field(
        default_factory=lambda: {"latency_ms": 0.0, "memory_mb": None, "device": "cpu"}
    )

    status: str = "SUCCESS"
    error_type: Optional[str] = None
    error_message: Optional[str] = None


class ReconciliationRecord(BaseModel):
    """Tracks reconciliation of Phase 4 S0 clean runs against Phase 2/2.5 baselines."""
    model: str
    metric_name: str
    historical_value: float
    phase4_s0_value: float
    difference: float
    tolerance: float
    status: str  # PASS / FAIL
    notes: str = ""
