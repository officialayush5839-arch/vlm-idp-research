"""
Model Runner for Phase 4 Baseline Execution.
Reuses frozen baselines from Phase 2 and 2.5 without code duplication or prompt drift.
"""

from __future__ import annotations

import time
from typing import Any, Dict, List, Optional
from PIL import Image

from src.baselines.base import Baseline, BaselineSample, BaselineResult
from src.baselines.b0_ocr import B0OCRBaseline
from src.baselines.b1_ocr_vlm import B1OCRVLMBaseline
from src.baselines.b2_vlm import B2VLMBaseline
from src.baselines.unlimited_ocr.adapter import B0UnlimitedOCRBaseline
from src.benchmark.schema import BenchmarkSample, ModelExecutionResult
from src.vlm.loader import VLMLoader
from src.vlm.inference import VLMInferenceEngine


class ModelRunner:
    """Orchestrates model execution across all four baselines (B0, B1, B2, B0-U)."""

    def __init__(self, execution_config: Optional[Dict[str, Any]] = None):
        self.config = execution_config or {}

        # Shared mock VLM engine for B1 and B2
        loader = VLMLoader()
        model, processor, metadata = loader.load_model_and_processor(mock_mode=True)
        self.vlm_engine = VLMInferenceEngine(
            model, processor, metadata, device="cpu", mock_mode=True
        )

        # Baselines
        self.b0 = B0OCRBaseline()
        self.b1 = B1OCRVLMBaseline(vlm_engine=self.vlm_engine)
        self.b2 = B2VLMBaseline(vlm_engine=self.vlm_engine)
        self.b0_u = B0UnlimitedOCRBaseline()

    def run_model(
        self,
        model_id: str,
        sample: BenchmarkSample,
        run_id: str,
        seed: int = 42,
    ) -> ModelExecutionResult:
        """
        Executes a single baseline on the given sample.
        Ensures strict prompt freezing and zero label leakage into models.
        """
        # Adapt BenchmarkSample to BaselineSample
        baseline_sample = BaselineSample(
            sample_id=sample.sample_id,
            document_id=sample.document_id,
            page_idx=sample.page_idx,
            image=sample.image,
            question=sample.question,
            ground_truth_answers=sample.ground_truth_answers,
        )

        t0 = time.perf_counter()

        if model_id == "B0":
            res = self.b0.run(baseline_sample, run_id=run_id, seed=seed)
            predicted_bboxes = []
            if hasattr(self.b0, "last_ocr_result") and self.b0.last_ocr_result:
                predicted_bboxes = [
                    line.bounding_box for line in self.b0.last_ocr_result.lines
                ]
            latency = (time.perf_counter() - t0) * 1000.0

            return ModelExecutionResult(
                model_id="B0",
                model_name=res.model,
                revision_sha=res.model_revision,
                prompt_version=None,
                prompt_hash=None,
                device=res.device,
                dtype=res.dtype,
                quantization=res.quantization,
                answer=res.answer,
                predicted_bboxes=predicted_bboxes,
                latency_ms=res.latency_ms or latency,
                status=res.status,
                error_type=res.error_type,
                error_message=res.error_message,
            )

        elif model_id == "B1":
            res = self.b1.run(baseline_sample, run_id=run_id, seed=seed)
            latency = (time.perf_counter() - t0) * 1000.0

            return ModelExecutionResult(
                model_id="B1",
                model_name=res.model,
                revision_sha=res.model_revision,
                prompt_version=res.prompt_version,
                prompt_hash=res.prompt_hash,
                device=res.device,
                dtype=res.dtype,
                quantization=res.quantization,
                answer=res.answer,
                predicted_bboxes=[],
                latency_ms=res.latency_ms or latency,
                status=res.status,
                error_type=res.error_type,
                error_message=res.error_message,
            )

        elif model_id == "B2":
            res = self.b2.run(baseline_sample, run_id=run_id, seed=seed)
            latency = (time.perf_counter() - t0) * 1000.0

            return ModelExecutionResult(
                model_id="B2",
                model_name=res.model,
                revision_sha=res.model_revision,
                prompt_version=res.prompt_version,
                prompt_hash=res.prompt_hash,
                device=res.device,
                dtype=res.dtype,
                quantization=res.quantization,
                answer=res.answer,
                predicted_bboxes=[],
                latency_ms=res.latency_ms or latency,
                status=res.status,
                error_type=res.error_type,
                error_message=res.error_message,
            )

        elif model_id == "B0-U":
            res = self.b0_u.run(baseline_sample, run_id=run_id, seed=seed)
            latency = (time.perf_counter() - t0) * 1000.0

            predicted_bboxes = []
            if hasattr(self.b0_u, "last_result") and self.b0_u.last_result:
                predicted_bboxes = [
                    elem.bounding_box
                    for elem in self.b0_u.last_result.layout_elements
                    if elem.bounding_box
                ]

            return ModelExecutionResult(
                model_id="B0-U",
                model_name=res.model,
                revision_sha=res.model_revision,
                prompt_version=res.prompt_version,
                prompt_hash=res.prompt_hash,
                device=res.device,
                dtype=res.dtype,
                quantization=res.quantization,
                answer=res.answer,
                predicted_bboxes=predicted_bboxes,
                latency_ms=res.latency_ms or latency,
                status=res.status,
                error_type=res.error_type,
                error_message=res.error_message,
            )

        else:
            raise ValueError(f"Unknown baseline model ID: {model_id}")
