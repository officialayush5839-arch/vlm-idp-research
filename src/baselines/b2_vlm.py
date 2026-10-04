"""B2: VLM-Only Baseline Implementation."""

import time
from typing import Optional, Dict, Any
from src.baselines.base import Baseline, BaselineSample, BaselineResult
from src.vlm.inference import VLMInferenceEngine
from src.vlm.prompts import PromptManager


class B2VLMBaseline(Baseline):
    """B2: Direct Vision-Language Model inference without OCR or text retrieval."""

    def __init__(
        self,
        vlm_engine: VLMInferenceEngine,
        prompt_manager: Optional[PromptManager] = None,
        config: Optional[Dict[str, Any]] = None
    ):
        super().__init__("B2", config)
        self.vlm_engine = vlm_engine
        self.prompt_manager = prompt_manager or PromptManager()
        self.prompt_file = self.config.get("prompt_file", "configs/phase2/prompts/b2_prompt.txt")

    def run(self, sample: BaselineSample, run_id: str, seed: int = 42) -> BaselineResult:
        start_time = time.perf_counter()
        try:
            # Format B2 Prompt
            prompt_text, p_ver, p_hash = self.prompt_manager.format_prompt(
                prompt_file=self.prompt_file,
                version_tag="v1.0-b2",
                question=sample.question
            )

            # Direct VLM Generation
            vlm_res = self.vlm_engine.generate(
                image=sample.image,
                prompt=prompt_text,
                prompt_version=p_ver,
                prompt_hash=p_hash
            )

            total_latency_ms = (time.perf_counter() - start_time) * 1000.0

            return BaselineResult(
                run_id=run_id,
                baseline=self.baseline_id,
                document_id=sample.document_id,
                page_id=f"page_{sample.page_idx}",
                question_id=sample.sample_id,
                model=vlm_res.model_metadata.model_name,
                model_revision=vlm_res.model_metadata.revision,
                prompt_version=p_ver,
                prompt_hash=p_hash,
                seed=seed,
                device=self.vlm_engine.device,
                dtype=vlm_res.model_metadata.dtype,
                quantization=vlm_res.model_metadata.quantization,
                answer=vlm_res.answer,
                ground_truth_answers=sample.ground_truth_answers,
                latency_ms=round(total_latency_ms, 2),
                gpu_peak_memory_mb=vlm_res.gpu_peak_memory_mb,
                status=vlm_res.status,
                error_type="PROCESSING_ERROR" if vlm_res.status == "FAILED" else None,
                error_message=vlm_res.error_message
            )
        except Exception as e:
            total_latency_ms = (time.perf_counter() - start_time) * 1000.0
            return BaselineResult(
                run_id=run_id,
                baseline=self.baseline_id,
                document_id=sample.document_id,
                page_id=f"page_{sample.page_idx}",
                question_id=sample.sample_id,
                model=self.vlm_engine.metadata.model_name,
                model_revision=self.vlm_engine.metadata.revision,
                prompt_version="v1.0-b2",
                prompt_hash="None",
                seed=seed,
                device=self.vlm_engine.device,
                dtype=self.vlm_engine.metadata.dtype,
                quantization=self.vlm_engine.metadata.quantization,
                answer="",
                ground_truth_answers=sample.ground_truth_answers,
                latency_ms=round(total_latency_ms, 2),
                gpu_peak_memory_mb=None,
                status="FAILED",
                error_type="PROCESSING_ERROR",
                error_message=str(e)
            )
