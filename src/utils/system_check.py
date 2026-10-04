"""
Environment, hardware, and CUDA runtime diagnostic utility for VLM-IDP.
Executes small controlled tensor smoke tests and reports exact hardware states.
Run with: python -m src.utils.system_check
"""

from __future__ import annotations

import platform
import sys
from typing import Any, Dict


def run_system_check() -> Dict[str, Any]:
    """Inspect and report the exact system hardware and machine-learning runtime."""
    results: Dict[str, Any] = {
        "os": platform.platform(),
        "python": sys.version.split()[0],
        "machine": platform.machine(),
        "torch_installed": False,
        "torch_version": "NOT_INSTALLED",
        "cuda_available": False,
        "cuda_runtime_version": "None",
        "gpu_count": 0,
        "gpu_name": "None",
        "gpu_total_memory_mb": 0.0,
        "cuda_smoke_test": "SKIPPED_NO_CUDA"
    }

    try:
        import torch
        results["torch_installed"] = True
        results["torch_version"] = torch.__version__
        results["cuda_available"] = torch.cuda.is_available()
        results["cuda_runtime_version"] = str(torch.version.cuda)

        if torch.cuda.is_available():
            results["gpu_count"] = torch.cuda.device_count()
            results["gpu_name"] = torch.cuda.get_device_name(0)
            total_bytes = torch.cuda.get_device_properties(0).total_memory
            results["gpu_total_memory_mb"] = round(total_bytes / (1024 * 1024), 2)

            # Controlled micro smoke test
            try:
                x = torch.ones((100, 100), device="cuda:0")
                y = x @ x
                torch.cuda.synchronize()
                allocated_mb = torch.cuda.memory_allocated(0) / (1024 * 1024)
                reserved_mb = torch.cuda.memory_reserved(0) / (1024 * 1024)
                del x, y
                torch.cuda.empty_cache()
                results["cuda_smoke_test"] = f"PASS (Allocated: {allocated_mb:.2f}MB, Reserved: {reserved_mb:.2f}MB)"
            except Exception as e:
                results["cuda_smoke_test"] = f"FAIL ({e})"
        else:
            results["cuda_smoke_test"] = "SKIPPED_CUDA_UNAVAILABLE"

    except ImportError:
        pass

    return results


def print_system_report() -> None:
    """Print formatted system diagnostic summary to stdout."""
    res = run_system_check()
    print("=" * 60)
    print("VLM-IDP SYSTEM & RUNTIME DIAGNOSTIC")
    print("=" * 60)
    print(f"Operating System      : {res['os']}")
    print(f"Python Version        : {res['python']}")
    print(f"Architecture          : {res['machine']}")
    print(f"PyTorch Version       : {res['torch_version']}")
    print(f"CUDA Available        : {res['cuda_available']}")
    print(f"CUDA Runtime Version  : {res['cuda_runtime_version']}")
    print(f"Device Count          : {res['gpu_count']}")
    print(f"GPU Device Name       : {res['gpu_name']}")
    print(f"Total Dedicated VRAM  : {res['gpu_total_memory_mb']} MB")
    print(f"CUDA Smoke Test       : {res['cuda_smoke_test']}")
    print("=" * 60)


if __name__ == "__main__":
    print_system_report()
