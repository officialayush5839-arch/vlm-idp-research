# PHASE 14 ENVIRONMENT COMPATIBILITY AUDIT REPORT

**Date & Time (UTC):** 2026-10-07T09:58:00Z  
**Environment Directory:** `.venv_phase14/`  
**Host Hardware:** NVIDIA GeForce RTX 3050 6GB Laptop GPU  
**CUDA Driver:** 581.95 (CUDA 13.0 compatible)  

---

## 1. Executive Summary

An isolated, reproducible CUDA execution environment has been successfully constructed in `.venv_phase14/` without touching the legacy `.venv/` runtime.

In contrast to Phase 13 where PyTorch was built for CPU-only execution (`torch.cuda.is_available() == False`), the Phase 14 isolated environment successfully runs PyTorch with native CUDA 12.6 support:
- **`torch.cuda.is_available() == True`**
- **Detected Device:** `NVIDIA GeForce RTX 3050 6GB Laptop GPU`
- **Total Physical VRAM:** 6,144 MiB
- **PyTorch CUDA Architecture:** SM 8.6 (Ampere Architecture)

---

## 2. Core Package Manifest

| Package | Requested Version | Installed Version | Python Compatibility | CUDA Compatibility | Installation Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Python** | 3.14.x | 3.14.6 | Native | Windows AMD64 | **CONFIRMED** |
| **torch** | 2.14.1+cu126 | 2.14.1+cu126 | Supported | CUDA 12.6 / SM 8.6 | **CONFIRMED** |
| **torchvision** | 0.29.1 | 0.29.1+cpu | Supported | Torch 2.14.1 | **CONFIRMED** |
| **transformers** | >=5.0.0 | 5.19.0 | Supported | Hugging Face Multi-modal | **CONFIRMED** |
| **bitsandbytes** | >=0.50.0 | 0.50.2 | Supported | Native Windows CUDA DLLs | **CONFIRMED** |
| **accelerate** | >=1.0.0 | 1.15.0 | Supported | Multi-GPU / Device Mapping | **CONFIRMED** |
| **sentence-transformers** | >=6.0.0 | 6.1.0 | Supported | Retrieval Embeddings | **CONFIRMED** |
| **numpy** | >=2.0.0 | 2.5.3 | Supported | Matrix operations | **CONFIRMED** |
| **pandas** | >=3.0.0 | 3.0.6 | Supported | Table data handling | **CONFIRMED** |
| **scipy** | >=1.18.0 | 1.18.1 | Supported | Statistical distributions | **CONFIRMED** |
| **scikit-learn** | >=1.9.0 | 1.9.1 | Supported | Metrics & bootstrap | **CONFIRMED** |
| **Pillow** | >=12.0.0 | 12.3.0 | Supported | Image loading & preprocessing | **CONFIRMED** |
| **PyYAML** | >=6.0.0 | 6.0.3 | Supported | Configuration parsing | **CONFIRMED** |

---

## 3. CUDA Memory Verification

A live device memory interrogation yielded:
- Device ID: `0`
- Initial Allocated Memory: `0.00 MiB`
- Initial Reserved Memory: `0.00 MiB`
- Device Capability: `Ampere SM 8.6`
- Hardware Gate Status: **READY** (`physical_execution_state = READY`)
