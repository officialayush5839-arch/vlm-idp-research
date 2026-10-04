"""Common Abstract Baseline Interface and Standardized Result Schemas."""

from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
from PIL import Image
from pydantic import BaseModel, Field, ConfigDict


class BaselineSample(BaseModel):
    """Encapsulates a single document question-answering evaluation instance."""
    model_config = ConfigDict(arbitrary_types_allowed=True)

    sample_id: str
    document_id: str
    page_idx: int = 0
    image: Any = Field(description="PIL Image instance", exclude=True)
    question: str
    ground_truth_answers: List[str] = Field(default_factory=list)


class BaselineResult(BaseModel):
    """Standardized Run Artifact Format matching Section 29 requirements."""
    run_id: str
    baseline: str
    document_id: str
    page_id: str
    question_id: str
    model: str
    model_revision: str
    prompt_version: Optional[str] = None
    prompt_hash: Optional[str] = None
    seed: int
    device: str
    dtype: str
    quantization: str
    answer: str
    ground_truth_answers: List[str] = Field(default_factory=list)
    latency_ms: Optional[float] = None
    gpu_peak_memory_mb: Optional[float] = None
    status: str = "SUCCESS"
    error_type: Optional[str] = None
    error_message: Optional[str] = None


class Baseline(ABC):
    """Abstract Base Class for Phase 2 Evaluation Baselines."""

    def __init__(self, baseline_id: str, config: Optional[Dict[str, Any]] = None):
        self.baseline_id = baseline_id
        self.config = config or {}

    @abstractmethod
    def run(self, sample: BaselineSample, run_id: str, seed: int = 42) -> BaselineResult:
        """Execute baseline processing pipeline on a single sample."""
        pass
