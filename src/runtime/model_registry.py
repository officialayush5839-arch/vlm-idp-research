"""Hardware-Aware Model Capability Registry for Document Extraction Studio.

Enforces zero-fabrication model gating:
- Connects directly to Phase 14 hardware detection (RTX 3050 6GB GDDR6).
- Gating rule: 7B parameter VLMs (Qwen2.5-VL-7B) require >14 GB VRAM for FP16 and >7 GB for INT8,
  and triggered OOM in Phase 14 negative controls. Marked NOT_EXECUTABLE on the validated 6 GB configuration.
- SmolVLM-500M INT4 is physically validated (531 MB footprint, 16.5 tok/s).
- PaddleOCR / Tesseract OCR pipelines are marked SUPPORTED.
"""

from enum import Enum
from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional
from src.phase14.hardware_gate import inspect_hardware_gate

class ModelStatus(str, Enum):
    PHYSICALLY_VALIDATED = "PHYSICALLY_VALIDATED"
    SUPPORTED = "SUPPORTED"
    SUPPORTED_WITH_LIMITATIONS = "SUPPORTED_WITH_LIMITATIONS"
    NOT_RECOMMENDED = "NOT_RECOMMENDED"
    NOT_EXECUTABLE = "NOT_EXECUTABLE"
    NOT_CONFIGURED = "NOT_CONFIGURED"

class ModelSelectionError(RuntimeError):
    """Raised when an unsupported or non-executable model is requested."""
    pass

@dataclass
class ModelCapability:
    model_id: str
    display_name: str
    parameter_size: str
    status: ModelStatus
    device: str
    precision: str
    estimated_vram_mb: int
    limitation_reason: str

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["status"] = self.status.value
        return d

class ModelRegistry:
    """Detects local hardware and maintains strict, un-fabricated model capability states."""

    def __init__(self):
        self._hw_cache: Optional[Dict[str, Any]] = None

    def get_hardware_status(self) -> Dict[str, Any]:
        if self._hw_cache is None:
            self._hw_cache = inspect_hardware_gate()
        return self._hw_cache

    def get_capability_matrix(self) -> Dict[str, ModelCapability]:
        hw = self.get_hardware_status()
        vram = hw.get("gpu_total_vram_mb", 6144)
        cuda_ok = hw.get("cuda_available_in_pytorch", False)

        matrix: Dict[str, ModelCapability] = {}

        # 1. SmolVLM-500M INT4 (Physically Validated in Phase 14)
        matrix["smolvlm-500m"] = ModelCapability(
            model_id="smolvlm-500m",
            display_name="SmolVLM-500M (INT4 NF4)",
            parameter_size="500M",
            status=ModelStatus.PHYSICALLY_VALIDATED if cuda_ok else ModelStatus.SUPPORTED_WITH_LIMITATIONS,
            device="CUDA (RTX 3050)" if cuda_ok else "CPU",
            precision="INT4 NF4 BitsAndBytes" if cuda_ok else "FP32",
            estimated_vram_mb=531,
            limitation_reason="Optimal for local 6 GB GPU; verified throughput 16.5 tok/s."
        )

        # 2. Qwen2.5-VL-7B (Strictly NOT_EXECUTABLE on 6GB configuration)
        matrix["qwen2.5-vl-7b"] = ModelCapability(
            model_id="qwen2.5-vl-7b",
            display_name="Qwen2.5-VL-7B Instruct",
            parameter_size="7B",
            status=ModelStatus.NOT_EXECUTABLE,
            device="CUDA",
            precision="FP16 / INT8",
            estimated_vram_mb=16384,
            limitation_reason="Exceeds 6 GB physical VRAM limit. Phase 14 OOM negative control confirmed NOT_EXECUTABLE on current local configuration."
        )

        # 3. PaddleOCR / Tesseract Hybrid Pipeline (SUPPORTED)
        matrix["paddleocr-pipeline"] = ModelCapability(
            model_id="paddleocr-pipeline",
            display_name="Adaptive OCR + Text Extractor",
            parameter_size="Lightweight (CNN+RNN)",
            status=ModelStatus.SUPPORTED,
            device="CPU / CUDA",
            precision="FP32",
            estimated_vram_mb=250,
            limitation_reason="High spatial precision for receipts, invoices, and degraded scans."
        )

        return matrix

    def select_model(self, model_id: str) -> ModelCapability:
        matrix = self.get_capability_matrix()
        model_id = model_id.lower().strip()
        if model_id not in matrix:
            raise ModelSelectionError(f"Model '{model_id}' is not registered in the system.")

        cap = matrix[model_id]
        if cap.status in (ModelStatus.NOT_EXECUTABLE, ModelStatus.NOT_CONFIGURED):
            raise ModelSelectionError(
                f"Model '{cap.display_name}' is {cap.status.value} on this hardware: {cap.limitation_reason}"
            )

        return cap
