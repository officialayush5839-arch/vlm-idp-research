"""VLM Data Models and Metadata Schemas for Phase 2."""

from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class ModelMetadata(BaseModel):
    """Metadata describing the Vision-Language Model version and configuration."""
    model_name: str
    revision: str
    huggingface_repo: str
    parameter_count: str
    quantization: str = "none"
    dtype: str = "float32"
    license_name: str = "Apache-2.0"


class VLMGenerationConfig(BaseModel):
    """Generation hyperparameter configuration."""
    temperature: float = 0.0
    top_p: float = 1.0
    max_new_tokens: int = 128
    do_sample: bool = False
    repetition_penalty: float = 1.0


class TimingBreakdown(BaseModel):
    """Latency breakdown for inference lifecycle."""
    preprocessing_ms: float = 0.0
    inference_ms: float = 0.0
    postprocessing_ms: float = 0.0
    total_latency_ms: float = 0.0


class VLMResult(BaseModel):
    """Structured result returned by VLM inference."""
    answer: str
    raw_response: str
    model_metadata: ModelMetadata
    generation_metadata: VLMGenerationConfig
    prompt_version: str
    prompt_hash: str
    timing: TimingBreakdown
    gpu_peak_memory_mb: Optional[float] = None
    status: str = "SUCCESS"
    error_message: Optional[str] = None
