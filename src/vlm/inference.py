"""VLM Inference Engine with Precise Latency & Resource Accounting."""

import time
from typing import Optional, Dict, Any
from PIL import Image
import torch

from src.vlm.schema import VLMResult, VLMGenerationConfig, TimingBreakdown, ModelMetadata
from src.vlm.processor import VLMImageProcessor


class VLMInferenceEngine:
    """Executes Vision-Language inference with deterministic synchronization."""

    def __init__(
        self,
        model: Any,
        processor: Any,
        metadata: ModelMetadata,
        device: str = "cpu",
        mock_mode: bool = False
    ):
        self.model = model
        self.processor = processor
        self.metadata = metadata
        self.device = device
        self.mock_mode = mock_mode
        self.image_processor = VLMImageProcessor()

    def generate(
        self,
        image: Image.Image,
        prompt: str,
        prompt_version: str,
        prompt_hash: str,
        gen_config: Optional[VLMGenerationConfig] = None
    ) -> VLMResult:
        config = gen_config or VLMGenerationConfig()
        overall_start = time.perf_counter()

        # Preprocessing phase
        prep_start = time.perf_counter()
        processed_img, transform_record = self.image_processor.process(image)
        prep_ms = (time.perf_counter() - prep_start) * 1000.0

        # Inference phase
        if self.device == "cuda" and torch.cuda.is_available():
            torch.cuda.synchronize()
            torch.cuda.reset_peak_memory_stats()

        infer_start = time.perf_counter()

        if self.mock_mode or self.model is None:
            # Deterministic mock inference for fast testing
            time.sleep(0.01)  # small synthetic delay for non-zero timing
            raw_response = f"Answer generated from prompt: {prompt[:40]}..."
            answer = raw_response.split(":")[-1].strip()
        else:
            try:
                with torch.inference_mode():
                    messages = [
                        {
                            "role": "user",
                            "content": [
                                {"type": "image", "image": processed_img},
                                {"type": "text", "text": prompt}
                            ]
                        }
                    ]
                    text_input = self.processor.apply_chat_template(
                        messages, tokenize=False, add_generation_prompt=True
                    )
                    image_inputs, video_inputs = self.processor.image_processor(
                        images=[processed_img], return_tensors="pt"
                    )
                    inputs = self.processor(
                        text=[text_input],
                        images=image_inputs,
                        padding=True,
                        return_tensors="pt"
                    ).to(self.device)

                    generated_ids = self.model.generate(
                        **inputs,
                        max_new_tokens=config.max_new_tokens,
                        do_sample=config.do_sample,
                        temperature=config.temperature if config.do_sample else None,
                        top_p=config.top_p if config.do_sample else None
                    )
                    generated_ids_trimmed = [
                        out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
                    ]
                    raw_response = self.processor.batch_decode(
                        generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
                    )[0]
                    answer = raw_response.strip()
            except Exception as e:
                total_ms = (time.perf_counter() - overall_start) * 1000.0
                return VLMResult(
                    answer="",
                    raw_response="",
                    model_metadata=self.metadata,
                    generation_metadata=config,
                    prompt_version=prompt_version,
                    prompt_hash=prompt_hash,
                    timing=TimingBreakdown(
                        preprocessing_ms=round(prep_ms, 2),
                        inference_ms=0.0,
                        postprocessing_ms=0.0,
                        total_latency_ms=round(total_ms, 2)
                    ),
                    gpu_peak_memory_mb=None,
                    status="FAILED",
                    error_message=f"PROCESSING_ERROR: {str(e)}"
                )

        if self.device == "cuda" and torch.cuda.is_available():
            torch.cuda.synchronize()
            gpu_peak_mb = round(torch.cuda.max_memory_allocated() / (1024 * 1024), 2)
        else:
            gpu_peak_mb = None

        infer_ms = (time.perf_counter() - infer_start) * 1000.0

        # Postprocessing phase
        post_start = time.perf_counter()
        clean_answer = answer.strip()
        post_ms = (time.perf_counter() - post_start) * 1000.0

        total_ms = (time.perf_counter() - overall_start) * 1000.0

        return VLMResult(
            answer=clean_answer,
            raw_response=raw_response,
            model_metadata=self.metadata,
            generation_metadata=config,
            prompt_version=prompt_version,
            prompt_hash=prompt_hash,
            timing=TimingBreakdown(
                preprocessing_ms=round(prep_ms, 2),
                inference_ms=round(infer_ms, 2),
                postprocessing_ms=round(post_ms, 2),
                total_latency_ms=round(total_ms, 2)
            ),
            gpu_peak_memory_mb=gpu_peak_mb,
            status="SUCCESS"
        )
