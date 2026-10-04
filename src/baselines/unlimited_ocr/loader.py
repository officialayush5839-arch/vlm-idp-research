"""Model Loader for Unlimited-OCR (B0-U)."""

from typing import Optional, Dict, Any, Tuple
import torch

from src.baselines.unlimited_ocr.metadata import UnlimitedOCRMetadata


class UnlimitedOCRLoader:
    """Manages Unlimited-OCR model lifecycle and hardware assignment."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        model_id = self.config.get("model_identity", {})
        self.metadata = UnlimitedOCRMetadata(
            model_name=model_id.get("name", "Unlimited-OCR"),
            huggingface_repo=model_id.get("huggingface_repo", "baidu/Unlimited-OCR"),
            revision=model_id.get("revision", "4f9b8c2e1d7a6053b8921e4c70d45f3a9e218c9b"),
            architecture=model_id.get("architecture", "UnlimitedOCRForConditionalGeneration"),
            backbone=model_id.get("backbone", "DeepSeek-V2 MoE (3.3B) + SAM-ViT-B + CLIP-L"),
            parameter_count=model_id.get("parameter_count", "3.3B"),
            license_name=model_id.get("license", "MIT"),
            max_context_tokens=self.config.get("inference_parameters", {}).get("max_context_tokens", 32768)
        )
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

    def load(self, mock_mode: bool = False) -> Tuple[Any, Any, UnlimitedOCRMetadata]:
        """Loads model and processor, supporting mock mode for test isolation."""
        if mock_mode:
            return None, None, self.metadata

        try:
            from transformers import AutoModelForVision2Seq, AutoProcessor
            repo = self.metadata.huggingface_repo
            rev = self.metadata.revision
            processor = AutoProcessor.from_pretrained(repo, revision=rev, trust_remote_code=True)
            model = AutoModelForVision2Seq.from_pretrained(
                repo,
                revision=rev,
                torch_dtype=torch.float32 if self.device == "cpu" else torch.bfloat16,
                device_map=self.device,
                trust_remote_code=True
            )
            return model, processor, self.metadata
        except Exception as e:
            raise RuntimeError(f"MODEL_LOAD_ERROR: Failed to load Unlimited-OCR from {self.metadata.huggingface_repo}: {e}")
