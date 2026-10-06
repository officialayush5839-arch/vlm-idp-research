# MODEL SELECTION & QUANTIZATION ARCHITECTURE JUSTIFICATION

**Project:** Vision-Language Models for Intelligent Document Processing under Real-World Visual Degradation  
**Phase:** Phase 13 — Physical GPU VLM Inference, Quantization & End-to-End System Benchmarking  
**Date:** 2026-10-06  
**Auditor:** Research-Grade AI/ML Systems Engineer  
**Status:** APPROVED FOR BENCHMARK SPECIFICATION

---

## 1. Primary Model Architecture Selection: Qwen2.5-VL-7B-Instruct

### 1.1 Technical Justification:
1. **Document Understanding Benchmark Dominance:** Qwen2.5-VL-7B establishes leading open-weight performance across standard document QA and visual grounding benchmarks (DocVQA, InfoVQA, OCRBench), matching or exceeding proprietary models of significantly larger parameter counts.
2. **Native Dynamic Resolution:** Unlike fixed-resolution vision encoders (e.g. standard CLIP $224\times 224$ or $336\times 336$ patches), Qwen2.5-VL handles dynamic aspect ratios and arbitrary resolutions using 2D Rotary Position Embeddings (2D-RoPE), which is critical for legibility in dense multi-column PDF layouts.
3. **Open Weights & Commercial Permissiveness:** Released under Apache-2.0 open-source licensing, ensuring complete reproducibility and local execution without cloud API lock-in.

---

## 2. Quantization Feasibility on 6GB NVIDIA Hardware

A central constraint of local commodity hardware (e.g. the host NVIDIA GeForce RTX 3050 6GB Laptop GPU) is physical VRAM capacity:

| Precision Level | Parameter Bits | Weight Footprint | Estimated KV Cache (2k tokens) | Total VRAM Required | Feasibility on 6GB GPU |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Q0: FP16 / BF16** | 16 bits | $15.2\text{ GB}$ | $\sim 1.0\text{ GB}$ | $\sim 16.2\text{ GB}$ | **INFEASIBLE (Out of Memory)** |
| **Q1: INT8** | 8 bits | $7.9\text{ GB}$ | $\sim 0.6\text{ GB}$ | $\sim 8.5\text{ GB}$ | **MARGINAL / INFEASIBLE (> 6GB)** |
| **Q2: INT4 (AWQ/NF4)** | 4 bits | $4.2\text{ GB}$ | $\sim 0.4\text{ GB}$ | $\sim 4.6\text{ GB}$ | **FEASIBLE ($\sim 1.5\text{ GB}$ Headroom)** |

**Conclusion:** 4-bit quantization (INT4 via AWQ or BitsAndBytes NormalFloat4) is mathematically necessary to deploy a modern 7B parameter Vision-Language Model on a 6GB VRAM budget. Quantization experiments must establish whether INT4 causes unacceptable degradation in document OCR fidelity or spatial evidence grounding.
