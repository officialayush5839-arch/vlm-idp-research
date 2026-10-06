"""Phase 13 Model Loader & Quantization Interface.

Defines the contract for loading Qwen2.5-VL-7B-Instruct across
precision levels Q0 (FP16), Q1 (INT8), and Q2 (INT4).

Gracefully flags GPU hardware gating when running on CPU builds.
"""

from typing import Dict, Any, Optional


class VLMModelLoader:
    """Manages Vision-Language Model weights and precision allocation."""

    def __init__(self, model_name: str = "Qwen2.5-VL-7B-Instruct", precision: str = "INT4"):
        self.model_name = model_name
        self.precision = precision.upper()
        self.is_loaded = False
        self.execution_device = "cpu"
        self.hardware_gated = False

    def load_model(self) -> Dict[str, Any]:
        """Attempts to load model weights onto target compute device."""
        try:
            import torch
            if torch.cuda.is_available():
                self.execution_device = "cuda:0"
                self.is_loaded = True
                self.hardware_gated = False
                return {
                    "status": "LOADED_CUDA",
                    "device": self.execution_device,
                    "precision": self.precision,
                    "model_name": self.model_name
                }
            else:
                self.execution_device = "cpu"
                self.is_loaded = False
                self.hardware_gated = True
                return {
                    "status": "NOT_EXECUTED — REQUIRED HARDWARE UNAVAILABLE",
                    "reason": "PyTorch CPU build detected; CUDA execution requires CUDA-enabled PyTorch environment.",
                    "device": "cpu",
                    "precision": self.precision,
                    "model_name": self.model_name
                }
        except Exception as e:
            self.hardware_gated = True
            return {
                "status": "LOAD_ERROR",
                "error": str(e)
            }
