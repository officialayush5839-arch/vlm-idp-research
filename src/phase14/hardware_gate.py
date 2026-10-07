"""Phase 14 Hardware Gate & Environment Inspector.

Strictly probes the physical machine for:
- Host OS and architecture
- Physical GPU presence and specs via nvidia-smi
- CUDA driver version and compatibility
- PyTorch CUDA enablement: torch.__version__, torch.cuda.is_available(), torch.cuda.device_count()
- Allocatable VRAM & Memory Limits

Zero-fabrication rule: If torch.cuda.is_available() is False, gates physical execution as BLOCKED.
"""

import sys
import platform
import subprocess
import shutil
from typing import Dict, Any

def inspect_hardware_gate() -> Dict[str, Any]:
    gate_data = {
        "os_name": platform.system(),
        "os_release": platform.release(),
        "os_version": platform.version(),
        "architecture": platform.machine(),
        "python_version": sys.version.split()[0],
        "python_executable": sys.executable,
        "physical_gpu_detected": False,
        "gpu_vendor": "Unknown",
        "gpu_model": "None",
        "gpu_total_vram_mb": 0,
        "gpu_driver_version": "None",
        "cuda_driver_version": "None",
        "pytorch_version": "None",
        "pytorch_cuda_version": "None",
        "cuda_available_in_pytorch": False,
        "cuda_device_count": 0,
        "cuda_device_name": "None",
        "physical_execution_state": "BLOCKED"
    }

    # 1. Probe physical GPU via nvidia-smi
    nvidia_smi_path = shutil.which("nvidia-smi") or r"C:\Windows\system32\nvidia-smi.exe"
    try:
        cmd = [
            nvidia_smi_path,
            "--query-gpu=gpu_name,driver_version,memory.total",
            "--format=csv,noheader,nounits"
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        lines = res.stdout.strip().splitlines()
        if lines:
            parts = [p.strip() for p in lines[0].split(",")]
            gate_data["physical_gpu_detected"] = True
            gate_data["gpu_vendor"] = "NVIDIA"
            gate_data["gpu_model"] = parts[0]
            gate_data["gpu_driver_version"] = parts[1]
            gate_data["gpu_total_vram_mb"] = int(float(parts[2]))
    except Exception as e:
        gate_data["nvidia_smi_error"] = str(e)

    # 2. Probe CUDA version via nvidia-smi banner
    try:
        res = subprocess.run([nvidia_smi_path], capture_output=True, text=True, check=True)
        for line in res.stdout.splitlines():
            if "CUDA Version:" in line:
                cuda_part = line.split("CUDA Version:")[1].split("|")[0].strip()
                gate_data["cuda_driver_version"] = cuda_part
                break
    except Exception:
        pass

    # 3. Probe PyTorch CUDA API
    try:
        import torch
        gate_data["pytorch_version"] = torch.__version__
        gate_data["pytorch_cuda_version"] = str(torch.version.cuda)
        gate_data["cuda_available_in_pytorch"] = torch.cuda.is_available()
        gate_data["cuda_device_count"] = torch.cuda.device_count()

        if torch.cuda.is_available() and torch.cuda.device_count() > 0:
            gate_data["cuda_device_name"] = torch.cuda.get_device_name(0)
            gate_data["physical_execution_state"] = "READY"
        else:
            gate_data["physical_execution_state"] = "BLOCKED"
    except ImportError:
        gate_data["pytorch_version"] = "NOT_INSTALLED"
        gate_data["physical_execution_state"] = "BLOCKED"

    return gate_data

if __name__ == "__main__":
    import json
    info = inspect_hardware_gate()
    print(json.dumps(info, indent=2))
