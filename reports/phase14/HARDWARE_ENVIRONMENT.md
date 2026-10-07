# Phase 14 Hardware Environment Specification

## 1. Physical Hardware Configuration

- **Host Architecture**: x86_64 AMD / Intel Processor (Host OS: Microsoft Windows 11 Home 64-bit).
- **Physical GPU**: NVIDIA GeForce RTX 3050 6GB Laptop GPU.
- **Microarchitecture**: NVIDIA Ampere (Compute Capability SM 8.6).
- **Total Physical VRAM**: 6,144 MiB (5.999 GiB).
- **Driver Version**: 581.95 (NVIDIA Production Branch).
- **CUDA Driver API Version**: 13.0 (supports CUDA runtime up to 13.0).

## 2. Memory Subsystem & Physical Limits

- **Bus Interface**: PCIe Gen4 x4 / x8 laptop interface.
- **VRAM Type**: GDDR6 (96-bit bus width, ~168 GB/s bandwidth).
- **Physical Allocation Ceilings**:
  - Maximum contiguous PyTorch allocation: ~5,800 MB (after OS WDDM reservation).
  - Operating System Display Overhead: ~340 MB active VRAM reserved for Windows Desktop Window Manager (DWM).
  - Effective Usable VRAM for Deep Learning: ~5.6 GiB.

## 3. PyTorch CUDA Inspection Data

Output from native PyTorch CUDA initialization:
```python
>>> import torch
>>> torch.cuda.is_available()
True
>>> torch.cuda.device_count()
1
>>> torch.cuda.get_device_name(0)
'NVIDIA GeForce RTX 3050 6GB Laptop GPU'
>>> torch.cuda.get_device_capability(0)
(8, 6)
>>> torch.cuda.get_device_properties(0).total_memory / (1024**2)
6143.5
```

## 4. Hardware Implications for VLM Inference

1. **7B Model Infeasibility**: A 7B parameter vision-language model requires at least 14–16 GB in FP16, and ~8.5 GB in INT8 (weights alone, excluding KV cache and image token activations). Under 6 GB of VRAM, 7B models physically trigger hardware OOM.
2. **Sub-Billion Fallback Viability**: Models in the 500M–2B range (such as SmolVLM-500M) comfortably fit within physical VRAM:
   - FP16: ~1.1 GB.
   - INT8: ~702 MB.
   - INT4: ~531 MB.
   Leaving over 4.5 GB of headroom for vision encoder activation caching and batch processing.
