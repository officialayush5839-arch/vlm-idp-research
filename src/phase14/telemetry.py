"""Phase 14 Real-Time GPU Telemetry and CUDA Memory Profiler.

Leverages official PyTorch CUDA APIs:
- torch.cuda.synchronize()
- torch.cuda.memory_allocated()
- torch.cuda.memory_reserved()
- torch.cuda.max_memory_allocated()
- torch.cuda.max_memory_reserved()

And nvidia-smi telemetry:
- Power draw (Watts)
- GPU temperature (C)
- Core clock & SM utilization
"""

import time
import subprocess
import shutil
from typing import Dict, Any, Optional

class PhysicalCUDAMonitor:
    def __init__(self, device_id: int = 0):
        self.device_id = device_id
        self.nvidia_smi = shutil.which("nvidia-smi") or r"C:\Windows\system32\nvidia-smi.exe"
        self._torch_available = False
        try:
            import torch
            if torch.cuda.is_available():
                self._torch = torch
                self._torch_available = True
        except ImportError:
            self._torch = None

    def reset_peak_memory(self):
        if self._torch_available:
            self._torch.cuda.reset_peak_memory_stats(self.device_id)

    def synchronize(self):
        if self._torch_available:
            self._torch.cuda.synchronize(self.device_id)

    def get_cuda_memory_mb(self) -> Dict[str, float]:
        if not self._torch_available:
            return {
                "allocated_mb": 0.0,
                "reserved_mb": 0.0,
                "max_allocated_mb": 0.0,
                "max_reserved_mb": 0.0
            }
        return {
            "allocated_mb": round(self._torch.cuda.memory_allocated(self.device_id) / (1024 * 1024), 2),
            "reserved_mb": round(self._torch.cuda.memory_reserved(self.device_id) / (1024 * 1024), 2),
            "max_allocated_mb": round(self._torch.cuda.max_memory_allocated(self.device_id) / (1024 * 1024), 2),
            "max_reserved_mb": round(self._torch.cuda.max_memory_reserved(self.device_id) / (1024 * 1024), 2),
        }

    def get_hardware_telemetry(self) -> Dict[str, Any]:
        telemetry = {
            "power_draw_w": None,
            "gpu_temp_c": None,
            "gpu_util_pct": None,
            "mem_util_pct": None
        }
        try:
            cmd = [
                self.nvidia_smi,
                f"--id={self.device_id}",
                "--query-gpu=power.draw,temperature.gpu,utilization.gpu,utilization.memory",
                "--format=csv,noheader,nounits"
            ]
            res = subprocess.run(cmd, capture_output=True, text=True, check=True)
            lines = res.stdout.strip().splitlines()
            if lines:
                parts = [p.strip() for p in lines[0].split(",")]
                telemetry["power_draw_w"] = float(parts[0]) if parts[0] != "[Not Supported]" else None
                telemetry["gpu_temp_c"] = float(parts[1])
                telemetry["gpu_util_pct"] = float(parts[2])
                telemetry["mem_util_pct"] = float(parts[3])
        except Exception:
            pass
        return telemetry
