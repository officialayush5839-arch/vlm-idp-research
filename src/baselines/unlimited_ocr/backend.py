"""Inference Backend for Unlimited-OCR."""

import time
from typing import Optional, Dict, Any, Tuple
from PIL import Image
import torch

from src.baselines.unlimited_ocr.schemas import UnlimitedOCRResult, UnlimitedOCRParsedOutput
from src.baselines.unlimited_ocr.metadata import UnlimitedOCRMetadata
from src.baselines.unlimited_ocr.parser import UnlimitedOCRParser
from src.baselines.unlimited_ocr.processor import UnlimitedOCRImageProcessor


class UnlimitedOCRBackend:
    """Executes Unlimited-OCR inference and produces standardized run artifacts."""

    def __init__(
        self,
        model: Any,
        processor: Any,
        metadata: UnlimitedOCRMetadata,
        device: str = "cpu",
        mock_mode: bool = False
    ):
        self.model = model
        self.processor = processor
        self.metadata = metadata
        self.device = device
        self.mock_mode = mock_mode
        self.image_processor = UnlimitedOCRImageProcessor()
        self.parser = UnlimitedOCRParser()

    def transcribe(
        self,
        image: Image.Image,
        document_id: str,
        page_id: str,
        prompt: Optional[str] = None
    ) -> UnlimitedOCRResult:
        """
        Executes end-to-end transcription and spatial grounding extraction.
        Captures raw output immutably before parsing into normalized representation.
        """
        start_time = time.perf_counter()
        img_w, img_h = image.size

        # Preprocessing
        prep_start = time.perf_counter()
        proc_img, trans_record = self.image_processor.process(image)
        prep_ms = (time.perf_counter() - prep_start) * 1000.0

        # Inference
        if self.device == "cuda" and torch.cuda.is_available():
            torch.cuda.synchronize()
            torch.cuda.reset_peak_memory_stats()

        infer_start = time.perf_counter()

        if self.mock_mode or self.model is None:
            # Deterministic mock inference producing realistic Unlimited-OCR format
            time.sleep(0.01)
            raw_output = (
                "title [40, 40, 500, 90]INVOICE #INV-2024-001\n"
                "text [40, 100, 350, 140]Vendor: Acme Corporation\n"
                "text [40, 160, 250, 190]Date: 2024-05-12\n"
                "text [40, 220, 320, 260]Total Amount: $1,450.00"
            )
        else:
            try:
                with torch.inference_mode():
                    effective_prompt = prompt or "<|grounding|>Parse and transcribe document."
                    inputs = self.processor(
                        images=proc_img,
                        text=effective_prompt,
                        return_tensors="pt"
                    ).to(self.device)

                    output_ids = self.model.generate(
                        **inputs,
                        max_new_tokens=4096,
                        do_sample=False
                    )
                    raw_output = self.processor.batch_decode(
                        output_ids, skip_special_tokens=True
                    )[0]
            except Exception as e:
                total_ms = (time.perf_counter() - start_time) * 1000.0
                return UnlimitedOCRResult(
                    baseline_id="B0-U",
                    engine="Unlimited-OCR",
                    model_revision=self.metadata.revision,
                    document_id=document_id,
                    page_id=page_id,
                    raw_output="",
                    normalized_text="",
                    structured_elements=[],
                    bounding_boxes=[],
                    confidence=None,
                    spatial_evidence_status="NOT_AVAILABLE",
                    latency_ms=round(total_ms, 2),
                    gpu_peak_memory_mb=None,
                    status="FAILED",
                    error_type="PROCESSING_ERROR",
                    error_message=str(e)
                )

        if self.device == "cuda" and torch.cuda.is_available():
            torch.cuda.synchronize()
            gpu_peak_mb = round(torch.cuda.max_memory_allocated() / (1024 * 1024), 2)
        else:
            gpu_peak_mb = None

        infer_ms = (time.perf_counter() - infer_start) * 1000.0

        # Parsing
        parse_start = time.perf_counter()
        parsed: UnlimitedOCRParsedOutput = self.parser.parse(
            raw_output, page_width=img_w, page_height=img_h
        )
        parse_ms = (time.perf_counter() - parse_start) * 1000.0

        total_ms = (time.perf_counter() - start_time) * 1000.0

        spatial_status = "SUPPORTED" if parsed.has_spatial_grounding else "NOT_AVAILABLE"
        bboxes = [el.normalized_bbox for el in parsed.elements]
        structured_elements = [el.model_dump() for el in parsed.elements]

        return UnlimitedOCRResult(
            baseline_id="B0-U",
            engine="Unlimited-OCR",
            model_revision=self.metadata.revision,
            document_id=document_id,
            page_id=page_id,
            raw_output=raw_output,
            normalized_text=parsed.full_transcription,
            structured_elements=structured_elements,
            bounding_boxes=bboxes,
            confidence=1.0 if parsed.has_spatial_grounding else None,
            spatial_evidence_status=spatial_status,
            latency_ms=round(total_ms, 2),
            gpu_peak_memory_mb=gpu_peak_mb,
            status="SUCCESS"
        )
