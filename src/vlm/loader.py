"""Model Loading and Hardware Environment Management for VLM-IDP."""

from typing import Optional, Dict, Any, Tuple
import torch

from src.vlm.schema import ModelMetadata


class VLMLoader:
    """Manages VLM lifecycle, device assignment, and version metadata."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        model_id = self.config.get("model_identity", {})
        self.metadata = ModelMetadata(
            model_name=model_id.get("name", "Qwen2.5-VL-7B-Instruct"),
            revision=model_id.get("revision", "b450c26581decfcb4c555513ab4deeb85ab1a39d"),
            huggingface_repo=model_id.get("huggingface_repo", "Qwen/Qwen2.5-VL-7B-Instruct"),
            parameter_count=model_id.get("parameter_count", "7.61B"),
            quantization=self.config.get("inference_parameters", {}).get("quantization", "none"),
            dtype=self.config.get("inference_parameters", {}).get("dtype", "float32"),
            license_name=model_id.get("license", "Apache-2.0")
        )
        self.device = self._detect_device()

    def _detect_device(self) -> str:
        """Verify device availability with zero fabrication."""
        if torch.cuda.is_available():
            return "cuda"
        return "cpu"

    def load_model_and_processor(
        self,
        mock_mode: bool = False
    ) -> Tuple[Any, Any, ModelMetadata]:
        """
        Loads model and processor.
        If mock_mode is True, returns lightweight simulated handlers for test isolation.
        """
        if mock_mode:
            return None, None, self.metadata

        # Real loading path via Hugging Face Transformers
        try:
            from transformers import AutoProcessor, Qwen2_5_VLForConditionalGeneration
            repo = self.metadata.huggingface_repo
            rev = self.metadata.revision
            processor = AutoProcessor.from_pretrained(repo, revision=rev)
            model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
                repo,
                revision=rev,
                torch_dtype=getattr(torch, self.metadata.dtype, torch.float32),
                device_map=self.device
            )
            return model, processor, self.metadata
        except Exception as e:
            raise RuntimeError(f"MODEL_LOAD_ERROR: Failed to load VLM from {self.metadata.huggingface_repo}: {e}")
