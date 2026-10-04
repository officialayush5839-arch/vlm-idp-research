"""B1: OCR + VLM Baseline Implementation."""

import time
from typing import Optional, Dict, Any
from src.baselines.base import Baseline, BaselineSample, BaselineResult
from src.ocr.base import OCRBackend
from src.ocr.paddle import PaddleOCRBackend
from src.vlm.inference import VLMInferenceEngine
from src.vlm.prompts import PromptManager


class B1OCRVLMBaseline(Baseline):
    """B1: Combines page image and OCR extracted text as dual input to VLM."""

    def __init__(
        self,
        vlm_engine: VLMInferenceEngine,
        ocr_backend: Optional[OCRBackend] = None,
        prompt_manager: Optional[PromptManager] = None,
        config: Optional[Dict[str, Any]] = None
    ):
        super().__init__("B1", config)
        self.vlm_engine = vlm_engine
        self.ocr_backend = ocr_backend or PaddleOCRBackend(config.get("ocr", {}) if config else {})
        self.prompt_manager = prompt_manager or PromptManager()
        self.prompt_file = self.config.get("prompt_file", "configs/phase2/prompts/b1_prompt.txt")

    def run(self, sample: BaselineSample, run_id: str, seed: int = 42) -> BaselineResult:
        start_time = time.perf_counter()
        try:
            # Step 1: Run OCR
            ocr_res = self.ocr_backend.extract(
                image=sample.image,
                page_idx=sample.page_idx,
                document_id=sample.document_id
            )

            # Step 2: Format B1 Prompt
            prompt_text, p_ver, p_hash = self.prompt_manager.format_prompt(
                prompt_file=self.prompt_file,
                version_tag="v1.0-b1",
                question=sample.question,
                ocr_text=ocr_res.full_text or "No text detected."
            )

            # Step 3: Run VLM
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
                prompt_version="v1.0-b1",
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
