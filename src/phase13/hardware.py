"""Phase 13 Hardware Probe & Systems Telemetry Module.

Detects host CPU, physical GPU, CUDA availability, VRAM capacity,
and enforces zero-fabrication logging rules.
"""

import os
import platform
import subprocess
from typing import Dict, Any


def detect_hardware_environment() -> Dict[str, Any]:
    """Probes physical host hardware and driver environment."""
    info: Dict[str, Any] = {
        "os": platform.platform(),
        "python_version": platform.python_version(),
        "cpu_arch": platform.machine(),
        "cuda_available_in_pytorch": False,
        "physical_gpu_detected": False,
        "gpu_model": "None",
        "total_vram_mib": 0,
        "driver_version": "None",
        "driver_cuda_version": "None",
        "telemetry_source": "system"
    }

    # Check PyTorch CUDA bindings
    try:
        import torch
        info["pytorch_version"] = torch.__version__
        info["cuda_available_in_pytorch"] = torch.cuda.is_available()
        if torch.cuda.is_available():
            info["gpu_model"] = torch.cuda.get_device_name(0)
            info["total_vram_mib"] = int(torch.cuda.get_device_properties(0).total_memory / (1024 * 1024))
    except Exception:
        info["pytorch_version"] = "unknown"

    # Query nvidia-smi if available on Windows/Linux host
    try:
        res = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,memory.total,driver_version", "--format=csv,noheader,nounits"],
            capture_output=True,
            text=True,
            check=True
        )
        lines = res.stdout.strip().split("\n")
        if lines and lines[0]:
            parts = [p.strip() for p in lines[0].split(",")]
            info["physical_gpu_detected"] = True
            info["gpu_model"] = parts[0]
            info["total_vram_mib"] = int(float(parts[1]))
            info["driver_version"] = parts[2]
            info["telemetry_source"] = "nvidia-smi"
    except Exception:
        pass

    return info


if __name__ == "__main__":
    hw = detect_hardware_environment()
    print("Detected Hardware Environment:")
    for k, v in hw.items():
        print(f"  {k}: {v}")
