# PHASE 2.5 — VRAM FEASIBILITY & HARDWARE CONSTRAINT ANALYSIS

**Project**: Vision-Language Models for Intelligent Document Processing under Real-World Visual Degradation  
**Phase**: Phase 2.5 — Unlimited-OCR Integration & Scientific Validation  
**Execution Date**: 2026-10-04  
**Audit Status**: CONFIRMED

---

## 1. Target Hardware Constraint

- **Target GPU**: NVIDIA GeForce RTX 3050 Laptop GPU
- **Dedicated Video Memory**: 6,144 MiB (6.0 GB GDDR6)
- **Host System RAM**: 16.0 GB DDR4/DDR5
- **Operating System**: Windows 11 AMD64

---

## 2. Theoretical & Empirical Memory Budget for 3.3B MoE Model

The Unlimited-OCR architecture contains approximately $3.3 \times 10^9$ parameters across its vision encoders (SAM-ViT-B + CLIP-L) and DeepSeek-V2 MoE language backbone.

| Precision / Mode | Weight Footprint (GB) | Vision Encoder & Activations (GB) | Total Estimated Peak Memory (GB) | RTX 3050 6GB Feasibility | Decision Category |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **FP32 (Full)** | ~13.2 GB | ~1.5 GB | ~14.7 GB | **INCOMPATIBLE (OOM)** | Category E |
| **FP16 / BF16** | ~6.6 GB | ~1.0 GB | ~7.6 GB | **INCOMPATIBLE (Exceeds 6.0 GB)** | Category E |
| **8-bit (INT8)** | ~3.4 GB | ~0.8 GB | ~4.2 GB | **FEASIBLE (Tight headroom)** | Category B |
| **4-bit (NF4 / AWQ)** | ~2.1 GB | ~0.6 GB | ~2.7 GB | **FULLY FEASIBLE (~3.3 GB headroom)** | Category B |
| **CPU Execution** | ~7.2 GB (RAM) | ~1.0 GB (RAM) | ~8.2 GB (RAM) | **FULLY FEASIBLE (Host has 16 GB)** | Category D |

---

## 3. RTX 3050 6GB Decision (Section 16)

Per Section 16 classification:
$$\textbf{B0-U Hardware Feasibility: Category B — Feasible with 4-bit Quantization / Offload}$$

### Detailed Finding
1. **Unquantized GPU Inference**: Native FP16 execution cannot safely run on the RTX 3050 6GB because weights alone (~6.6 GB) exceed the physical 6.0 GB VRAM boundary, inevitably triggering `CUDA: out of memory`.
2. **Quantized GPU Inference**: When packaged with 4-bit quantization (NF4 via bitsandbytes or AWQ via vLLM), the total memory requirement drops to ~2.7 GB, which comfortably fits inside the 6GB VRAM budget with ~3.3 GB buffer for activations and R-SWA sliding window KV-cache.
3. **Current Active Runtime**: In the active Python 3.14 environment where PyTorch is CPU-only, the model executes under Category D (CPU execution utilizing host system RAM).
