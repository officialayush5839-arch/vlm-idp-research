"""Baseline Adapter for Unlimited-OCR (B0-U)."""

import time
from typing import Optional, Dict, Any
from src.baselines.base import Baseline, BaselineSample, BaselineResult
from src.baselines.unlimited_ocr.backend import UnlimitedOCRBackend
from src.baselines.unlimited_ocr.loader import UnlimitedOCRLoader


class B0UnlimitedOCRBaseline(Baseline):
    """B0-U: Unlimited-OCR End-to-End Multimodal OCR Baseline Adapter."""

    def __init__(
        self,
        backend: Optional[UnlimitedOCRBackend] = None,
        config: Optional[Dict[str, Any]] = None
    ):
        super().__init__("B0-U", config)
        if backend is not None:
            self.backend = backend
        else:
            loader = UnlimitedOCRLoader(config)
            model, processor, metadata = loader.load(mock_mode=True)
            self.backend = UnlimitedOCRBackend(
                model=model,
                processor=processor,
                metadata=metadata,
                device=loader.device,
                mock_mode=True
            )

    def _extract_answer_from_text(self, transcription: str, question: str) -> str:
        """Finds the line or element most relevant to the question."""
        if not transcription.strip():
            return ""

        lines = [line.strip() for line in transcription.splitlines() if line.strip()]
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

        # If line contains colon, return trailing value (e.g. "Total Amount: $1,450.00" -> "$1,450.00")
        if ":" in best_line:
            parts = best_line.split(":", 1)
            if parts[1].strip():
                return parts[1].strip()

        return best_line

    def run(self, sample: BaselineSample, run_id: str, seed: int = 42) -> BaselineResult:
        """Executes B0-U inference on sample and returns standardized BaselineResult."""
        start_time = time.perf_counter()
        try:
            res = self.backend.transcribe(
                image=sample.image,
                document_id=sample.document_id,
                page_id=f"page_{sample.page_idx}"
            )
            answer = self._extract_answer_from_text(res.normalized_text, sample.question)
            latency_ms = (time.perf_counter() - start_time) * 1000.0

            return BaselineResult(
                run_id=run_id,
                baseline=self.baseline_id,
                document_id=sample.document_id,
                page_id=f"page_{sample.page_idx}",
                question_id=sample.sample_id,
                model="Unlimited-OCR",
                model_revision=self.backend.metadata.revision,
                prompt_version="grounding-v1",
                prompt_hash="8c2e1d7a6053b892",
                seed=seed,
                device=self.backend.device,
                dtype="float32",
                quantization="none",
                answer=answer,
                ground_truth_answers=sample.ground_truth_answers,
                latency_ms=round(latency_ms, 2),
                gpu_peak_memory_mb=res.gpu_peak_memory_mb,
                status=res.status,
                error_type=res.error_type,
                error_message=res.error_message
            )
        except Exception as e:
            latency_ms = (time.perf_counter() - start_time) * 1000.0
            return BaselineResult(
                run_id=run_id,
                baseline=self.baseline_id,
                document_id=sample.document_id,
                page_id=f"page_{sample.page_idx}",
                question_id=sample.sample_id,
                model="Unlimited-OCR",
                model_revision=self.backend.metadata.revision,
                prompt_version="grounding-v1",
                prompt_hash="8c2e1d7a6053b892",
                seed=seed,
                device=self.backend.device,
                dtype="float32",
                quantization="none",
                answer="",
                ground_truth_answers=sample.ground_truth_answers,
                latency_ms=round(latency_ms, 2),
                gpu_peak_memory_mb=None,
                status="FAILED",
                error_type="PROCESSING_ERROR",
                error_message=str(e)
            )
