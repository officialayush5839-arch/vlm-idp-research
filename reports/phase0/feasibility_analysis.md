# Feasibility & Compute Budget Analysis — Phase 0

**Project Title**: Adaptive, Uncertainty-Aware and Evidence-Grounded Vision-Language Document Intelligence under Real-World Visual Degradation  
**Document Stage**: Phase 0 Research Protocol Freeze  
**Last Updated**: 2026-10-04  

---

## 1. Hardware Environment Profiling

The primary development machine environment has been empirically verified:

*   **Operating System**: Windows 11
*   **Host CPU**: Modern multi-core x86_64 host
*   **System RAM**: 16 GB Physical Memory
*   **Target GPU**: NVIDIA GeForce RTX 3050 6GB Laptop GPU
*   **Dedicated VRAM**: 6,144 MiB (6.0 GB)
*   **CUDA Driver Version**: 581.95
*   **Current PyTorch Build**: CPU-only build (`CUDA: False` in global Python 3.14.6)
*   **Phase 1 Prerequisite**: Must install a CUDA-enabled PyTorch build within a dedicated `.venv` virtual environment.

---

## 2. VRAM Feasibility Analysis for 7B Foundation VLMs

A 7B parameter Vision-Language Model in standard 16-bit floating point precision (`bfloat16` or `float16`) requires:
$$\text{Weight Memory} = 7 \times 10^9 \text{ params} \times 2 \text{ bytes} \approx 14.0 \text{ GB VRAM}$$
This exceeds the physical capacity of the 6.0 GB RTX 3050 GPU.

### Mathematical Quantization Budget:
Under **4-bit NormalFloat (NF4)** quantization (via `bitsandbytes` or AWQ):
$$\text{Quantized Weight Memory} = 7 \times 10^9 \text{ params} \times 0.5 \text{ bytes} \approx 3.50 \text{ GB}$$
$$\text{KV Cache (Context Length 2048)} \approx 0.60 \text{ GB}$$
$$\text{Vision Transformer Activation Buffer (1024}\times\text{1024 image)} \approx 1.10 \text{ GB}$$
$$\text{PyTorch / CUDA Context Overhead} \approx 0.50 \text{ GB}$$
$$\textbf{Total Peak VRAM Footprint} \approx \mathbf{5.70 \text{ GB}} \le 6.14 \text{ GB}$$

### Architectural Invariants for Local Execution:
1. **4-Bit Quantization**: Mandatory for all local Qwen2.5-VL 7B and InternVL2 8B inference runs.
2. **Page-by-Page Ingestion**: Long documents must be processed page-by-page or in small chunk batches, never loading 50 high-resolution images simultaneously into VRAM.
3. **Embedding Offloading**: BGE text embeddings and FAISS index lookups run on host CPU / RAM, reserving 100% of dedicated GPU memory for VLM forward passes.

---

## 3. Experiment Matrix Scaling & Budget Estimation

| Run Category | Conditions (Models $\times$ Datasets $\times$ Severities) | Instances per Run | Seeds | Total Query Inferences | Estimated Hardware Status |
|:---|:---:|:---:|:---:|:---:|:---:|
| **Baselines (B0–B6)** | 7 Baselines $\times$ 3 Core Datasets | 500 | 3 | 31,500 | `STATUS = TO_BE_BENCHMARKED` |
| **Degradation Grid** | 4 Models $\times$ 9 Corruptions $\times$ 4 Severities | 250 | 3 | 108,000 | `STATUS = TO_BE_BENCHMARKED` |
| **Long-Document Runs** | 3 Models $\times$ 2 Datasets $\times$ 4 $k$-values | 200 | 3 | 14,400 | `STATUS = TO_BE_BENCHMARKED` |
| **Ablation Matrix (A1–A12)** | 12 Ablation conditions $\times$ 2 Datasets | 250 | 3 | 18,000 | `STATUS = TO_BE_BENCHMARKED` |

> [!NOTE] Empirical Feasibility Rule
> In accordance with the Anti-Fabrication Rule, exact inference timings (seconds per query, total GPU hours) are marked `STATUS = TO_BE_BENCHMARKED`. A calibration script in Phase 1 will benchmark single-query latency ($T_{\text{infer}}$) on local hardware before launching the full matrix.

---

## 4. Prioritized Execution Tiering (Compute Contingency)

To ensure that computational limits do not stall research progress or delay paper delivery, the experiment matrix is stratified into three prioritized tiers:

1. **Tier 1: Core Publication Minimum (Mandatory for IEEE Defense)**:
   - Baselines B0, B1, B2, B6 vs. PROPOSED.
   - 4 critical degradation families: Gaussian Blur, Gaussian Noise, JPEG, Skew.
   - Primary Datasets: DocVQA (QA & Grounding) + FUNSD (Real Degradation) + MMLongBench-Doc (Long Context).
   - 3 random seeds ($S_3 = \{42, 123, 456\}$).
   - *Estimated scale: ~18,000 queries (~35 hours at 7 sec/query)*.
2. **Tier 2: Comprehensive Paper Suite**:
   - Full 9-factor degradation grid across all 5 severities.
   - All 7 baselines (B0–B6) + Ablations A1–A8.
   - 5 random seeds ($S_5$).
3. **Tier 3: Extended Generalization Suite**:
   - Large-scale zero-shot evaluation on CORD, SROIE, and XL-DocBench.
   - Secondary model InternVL2 comparison (A9).
