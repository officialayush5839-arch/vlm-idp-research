"""Tests for Phase 15 Hardware-Aware Model Capability Registry."""

import pytest
from src.runtime.model_registry import (
    ModelRegistry,
    ModelStatus,
    ModelCapability,
    ModelSelectionError,
)

def test_hardware_detection():
    registry = ModelRegistry()
    hw = registry.get_hardware_status()
    assert "os_name" in hw
    assert "physical_gpu_detected" in hw
    assert "gpu_total_vram_mb" in hw

def test_model_capability_registry():
    registry = ModelRegistry()
    matrix = registry.get_capability_matrix()
    
    assert "smolvlm-500m" in matrix
    assert "qwen2.5-vl-7b" in matrix
    assert "paddleocr-pipeline" in matrix

    # Qwen2.5-VL-7B must be NOT_EXECUTABLE on the 6GB configuration
    qwen = matrix["qwen2.5-vl-7b"]
    assert qwen.status == ModelStatus.NOT_EXECUTABLE
    assert "6 GB" in qwen.limitation_reason

    # SmolVLM-500M must be PHYSICALLY_VALIDATED or SUPPORTED
    smol = matrix["smolvlm-500m"]
    assert smol.status in (ModelStatus.PHYSICALLY_VALIDATED, ModelStatus.SUPPORTED)

    # PaddleOCR pipeline must be SUPPORTED
    ocr = matrix["paddleocr-pipeline"]
    assert ocr.status == ModelStatus.SUPPORTED

def test_safe_model_selection_rejects_qwen():
    registry = ModelRegistry()
    with pytest.raises(ModelSelectionError, match="NOT_EXECUTABLE"):
        registry.select_model("qwen2.5-vl-7b")

def test_safe_model_selection_accepts_supported():
    registry = ModelRegistry()
    selected = registry.select_model("smolvlm-500m")
    assert selected.model_id == "smolvlm-500m"
