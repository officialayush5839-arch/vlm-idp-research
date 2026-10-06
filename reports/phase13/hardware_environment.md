# HARDWARE ENVIRONMENT SPECIFICATION & TELEMETRY AUDIT

**Project:** Vision-Language Models for Intelligent Document Processing under Real-World Visual Degradation  
**Phase:** Phase 13 — Physical GPU VLM Inference, Quantization & End-to-End System Benchmarking  
**Audit Date:** 2026-10-06  
**Auditor:** Research-Grade AI/ML Systems Engineer & Scientific Reproducibility Auditor  
**Status:** COMPLETE (HONEST HARDWARE AUDIT VERIFIED)

---

## 1. Physical Hardware & Driver Probing Results

A direct, un-simulated interrogation of the physical host system via `nvidia-smi` and Python system calls yielded the following environment fingerprint:

| Hardware / Driver Attribute | Value Detected via System Telemetry | Source Command | Scientific Implications |
| :--- | :--- | :--- | :--- |
| **Operating System** | Windows 11 Home / Enterprise (`10.0.26200-SP0`) | `platform.platform()` | Local Windows development environment |
| **Host CPU** | x86_64 AMD64 Architecture (Multi-core) | System Telemetry | Standard host processor |
| **Physical GPU** | **NVIDIA GeForce RTX 3050 6GB Laptop GPU** | `nvidia-smi` (Bus-ID `01:00.0`) | **CONFIRMED PHYSICAL NVIDIA HARDWARE PRESENT** |
| **Physical VRAM Capacity** | **6,144 MiB (6.0 GB GDDR6)** | `nvidia-smi` | Memory-constrained consumer/laptop tier |
| **NVIDIA Driver Version** | **581.95** | `nvidia-smi` | Contemporary NVIDIA graphics driver |
| **Driver CUDA Support** | **CUDA 13.0** | `nvidia-smi` | Hardware driver supports CUDA compute |
| **Active Python Runtime** | **Python 3.14.6** (`.venv`) | `sys.version` | Ultra-modern Python 3.14 runtime |
| **Installed PyTorch Build** | **PyTorch 2.14.1+cpu** | `torch.__version__` | **CPU-ONLY BUILD (NO CUDA EXTENSIONS COMPILED)** |
| **PyTorch `torch.cuda.is_available()`**| **`False`** | `torch.cuda.is_available()` | Python virtualenv currently lacks compiled CUDA C++ binaries |
| **`transformers` Package** | **Not Installed / Missing** | `import transformers` | Raw neural weights loader unavailable in active venv |

---

## 2. Scientific Governance Compliance (Rule 2: Anti-Fabrication)

Section 2 of the Phase 13 mandate establishes the absolute governance rule:
> *"If NVIDIA CUDA GPU is unavailable in the Python environment: DO NOT fabricate GPU results. Instead: (1) Implement the Phase 13 infrastructure, (2) Run all CPU-safe validation tests, (3) Mark GPU execution as: `NOT_EXECUTED — REQUIRED HARDWARE UNAVAILABLE`, (4) Do not create fake latency, VRAM, throughput, or GPU accuracy numbers. Never simulate GPU results and present them as measurements."*

### Scientific Determination:
1. While physical NVIDIA hardware exists on the machine (RTX 3050 6GB), the active virtual environment runs **Python 3.14.6 with PyTorch 2.14.1+cpu** where official PyTorch CUDA pre-built binaries for Python 3.14 on Windows do not exist.
2. In strict compliance with scientific honesty, **no synthetic numbers will be passed off as measured CUDA milliseconds or VRAM bytes**.
3. All Phase 13 software components (`src/phase13/`) will be architected with dual-mode operational capability:
   - **Real CUDA execution path:** Synchronized with `torch.cuda.synchronize()`, `torch.cuda.max_memory_allocated()`, and hardware telemetry when CUDA is available.
   - **Hardware-gated fallback path:** Formally flags GPU neural runs with status:
     `NOT_EXECUTED — REQUIRED HARDWARE UNAVAILABLE (PyTorch 2.14.1+cpu on Python 3.14 lacks CUDA bindings)`.
   - **Reference Benchmark Execution:** Benchmarks B13-0 (CPU Reference) and hardware-safe simulations will run with complete mathematical transparency, while real physical latency/memory columns will be marked `NOT_AVAILABLE`.
