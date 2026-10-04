"""B0: OCR-Only Baseline Implementation."""

import time
from typing import Optional, Dict, Any
from src.baselines.base import Baseline, BaselineSample, BaselineResult
from src.ocr.base import OCRBackend
from src.ocr.paddle import PaddleOCRBackend


class B0OCRBaseline(Baseline):
    """B0: OCR-only baseline extracting answer text from detected OCR layout tokens."""

    def __init__(self, ocr_backend: Optional[OCRBackend] = None, config: Optional[Dict[str, Any]] = None):
        super().__init__("B0", config)
        self.ocr_backend = ocr_backend or PaddleOCRBackend(config.get("ocr", {}) if config else {})

    def _extract_heuristic_answer(self, ocr_text: str, question: str) -> str:
        """Rule-based text heuristic: find line with highest keyword overlap to question."""
        if not ocr_text.strip():
            return ""

        lines = [line.strip() for line in ocr_text.splitlines() if line.strip()]
        if not lines:
            return ""

        q_words = set(question.lower().replace("?", "").split())
        best_line = lines[0]
        max_overlap = -1

        for line in lines:
            line_words = set(line.lower().split())
            overlap = len(q_words.intersection(line_words))
            if overlap > max_overlap:
                max_overlap = overlap
                best_line = line

        return best_line

    def run(self, sample: BaselineSample, run_id: str, seed: int = 42) -> BaselineResult:
        start_time = time.perf_counter()
        try:
            ocr_res = self.ocr_backend.extract(
                image=sample.image,
                page_idx=sample.page_idx,
                document_id=sample.document_id
            )
            answer = self._extract_heuristic_answer(ocr_res.full_text, sample.question)
            latency_ms = (time.perf_counter() - start_time) * 1000.0

            return BaselineResult(
                run_id=run_id,
                baseline=self.baseline_id,
                document_id=sample.document_id,
                page_id=f"page_{sample.page_idx}",
                question_id=sample.sample_id,
                model=f"OCR_{self.ocr_backend.engine_name}",
                model_revision=self.ocr_backend.engine_version,
                prompt_version="None",
                prompt_hash="None",
                seed=seed,
                device="cpu",
                dtype="string",
                quantization="none",
                answer=answer,
                ground_truth_answers=sample.ground_truth_answers,
                latency_ms=round(latency_ms, 2),
                gpu_peak_memory_mb=None,
                status="SUCCESS"
            )
        except Exception as e:
            latency_ms = (time.perf_counter() - start_time) * 1000.0
            return BaselineResult(
                run_id=run_id,
                baseline=self.baseline_id,
                document_id=sample.document_id,
                page_id=f"page_{sample.page_idx}",
                question_id=sample.sample_id,
                model=f"OCR_{self.ocr_backend.engine_name}",
                model_revision=self.ocr_backend.engine_version,
                seed=seed,
                device="cpu",
                dtype="string",
                quantization="none",
                answer="",
                ground_truth_answers=sample.ground_truth_answers,
                latency_ms=round(latency_ms, 2),
                gpu_peak_memory_mb=None,
                status="FAILED",
                error_type="OCR_ERROR",
                error_message=str(e)
            )
