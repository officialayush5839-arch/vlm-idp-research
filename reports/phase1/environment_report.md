# PHASE 1 — ENVIRONMENT & RUNTIME DIAGNOSTIC REPORT

**Project**: Adaptive, Uncertainty-Aware and Evidence-Grounded Vision-Language Document Intelligence under Real-World Visual Degradation  
**Phase**: Phase 1 — Repository, Environment, Infrastructure & Document Ingestion  
**Execution Date**: 2026-10-04  
**Audit Status**: CONFIRMED  
**Anti-Fabrication Notice**: All hardware, software, runtime, and diagnostic fields in this report are measured directly from the active runtime environment. No values are simulated or projected.

---

## 1. Host Operating System & Hardware Platform

| Parameter | Observed Value | Status |
| :--- | :--- | :--- |
| **Operating System** | Windows 11 (Windows-11-10.0.26200-SP0) | CONFIRMED |
| **Platform Architecture** | AMD64 (x86_64) | CONFIRMED |
| **Physical Host CPU** | AMD64 Family 25 Model 80 Stepping 0 (8 Cores / 16 Threads) | CONFIRMED |
| **Physical GPU** | NVIDIA GeForce RTX 3050 6GB Laptop GPU | CONFIRMED |
| **NVIDIA Driver Version** | 581.95 (Supports CUDA 13.0 API) | CONFIRMED |
| **GPU Dedicated VRAM** | 6144 MiB (6.0 GB GDDR6) | CONFIRMED |

---

## 2. Python & Virtual Environment Specification

| Parameter | Observed Value | Status |
| :--- | :--- | :--- |
| **Python Version** | 3.14.6 (tags/v3.14.6:16fd5da, Feb 10 2026) | CONFIRMED |
| **Virtual Environment Path** | `c:\Users\ARYAN - AYUSH\OneDrive\Desktop\Nlp\vlm-idp-research\.venv` | CONFIRMED |
| **Package Installer** | pip 26.0 | CONFIRMED |
| **Build Backend** | `hatchling` (configured in `pyproject.toml`) | CONFIRMED |
| **Test Runner** | pytest 9.1.1 (with `pythonpath = ["."]`) | CONFIRMED |

---

## 3. PyTorch & CUDA Acceleration Diagnostic

Per Section 7 and Section 35 of the research protocol and anti-fabrication constitution:
CUDA availability must reflect actual runtime operational status. Because pre-built CUDA wheels on PyTorch's official repository currently target Python versions up to 3.13, the active Python 3.14 virtual environment utilizes the official `torch-2.14.1+cpu` release.

```
============================================================
VLM-IDP SYSTEM & RUNTIME DIAGNOSTIC OUTPUT
============================================================
Operating System      : Windows-11-10.0.26200-SP0
Python Version        : 3.14.6
Architecture          : AMD64
PyTorch Version       : 2.14.1+cpu
CUDA Available        : False
CUDA Runtime Version  : None
Device Count          : 0
GPU Device Name       : None
Total Dedicated VRAM  : 0.0 MB (via PyTorch)
Physical GPU Present  : NVIDIA GeForce RTX 3050 6GB Laptop GPU (via nvidia-smi)
CUDA Smoke Test       : SKIPPED_CUDA_UNAVAILABLE
============================================================
```

| Parameter | PyTorch Observed | System Observed | Status |
| :--- | :--- | :--- | :--- |
| **PyTorch Version** | `2.14.1+cpu` | - | CONFIRMED |
| **Torchvision Version** | `0.29.1+cpu` | - | CONFIRMED |
| **CUDA Available (PyTorch)** | `False` | `True` (Driver supports CUDA 13.0) | CONFIRMED |
| **Device Mode** | CPU-Only fallback | Physical GPU idle | CONFIRMED |

### Phase 1 Impact Assessment
- **Ingestion & Normalization**: Completely unaffected. PyMuPDF, Pillow, and coordinate normalization do not require CUDA.
- **Reproducibility & Hash Validation**: Completely unaffected. Cryptographic SHA-256 and NumPy seed determinism execute with zero hardware discrepancy.
- **Phase 2 Baseline Preparation**: When VLM inference is initialized in Phase 2, a quantized model (e.g. 4-bit via bitsandbytes/llama.cpp/vLLM) or a Python 3.12/3.13 CUDA-accelerated environment can be invoked to utilize the 6GB VRAM on the RTX 3050.

---

## 4. Installed Dependency Registry (Freeze)

```text
accelerate==1.13.0
black==26.1.0
filelock==3.25.0
fsspec==2026.2.0
hatchling==1.27.0
jinja2==3.1.6
markupsafe==3.0.3
mpmath==1.3.0
mypy==1.19.1
networkx==3.6.1
numpy==2.4.2
pillow==12.1.1
pluggy==1.6.0
pydantic==2.12.5
pydantic_core==2.41.5
pymupdf==1.27.1
pypdf==6.7.5
pytest==9.1.1
pytest-cov==7.0.1
pyyaml==6.0.3
regex==2026.2.20
ruff==0.15.6
safetensors==0.7.0
scipy==1.17.1
sympy==1.14.0
tokenizers==0.22.2
torch==2.14.1+cpu
torchvision==0.29.1+cpu
tqdm==4.67.3
transformers==4.57.6
typing_extensions==4.15.0
```

---

## 5. Verification Sign-Off

- [x] Host OS, CPU, and physical GPU documented
- [x] Python 3.14.6 environment isolated under `.venv`
- [x] PyTorch runtime status recorded truthfully as CPU-only (`torch.cuda.is_available() == False`)
- [x] Anti-fabrication rules strictly preserved
