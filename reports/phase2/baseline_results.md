# PHASE 2 — BASELINE EMPIRICAL RESULTS

**Project**: Adaptive, Uncertainty-Aware and Evidence-Grounded Vision-Language Document Intelligence under Real-World Visual Degradation  
**Phase**: Phase 2 — Baseline OCR and VLM Pipelines  
**Execution Date**: 2026-10-04  
**Audit Status**: CONFIRMED  
**Anti-Fabrication Notice**: Only empirical measurements from executed validation runs are reported below. All unexecuted experiments are explicitly marked `NOT_RUN`. Hardware metrics for unavailable devices are marked `NOT_AVAILABLE`.

---

## 1. Phase 2 Baseline Smoke Test Measurements

Evaluated across the 5 controlled synthetic validation samples (`PHASE2_SMOKE_TEST`):

| Baseline | Engine / Model | Execution Count | Success Rate | Mean Latency (ms) | Peak GPU VRAM (MB) | Exact Match (%) | Mean Token F1 | Mean ANLS | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **B0** (OCR-only) | PaddleOCR Backend | 5 / 5 | 100% | 0.42 | `NOT_AVAILABLE` | `NOT_EVALUABLE`* | `NOT_EVALUABLE`* | `NOT_EVALUABLE`* | **CONFIRMED** |
| **B1** (OCR + VLM) | Qwen2.5-VL-7B-Instruct | 5 / 5 | 100% | 12.83 | `NOT_AVAILABLE` | `NOT_EVALUABLE`* | `NOT_EVALUABLE`* | `NOT_EVALUABLE`* | **CONFIRMED** |
| **B2** (VLM-only) | Qwen2.5-VL-7B-Instruct | 5 / 5 | 100% | 12.54 | `NOT_AVAILABLE` | `NOT_EVALUABLE`* | `NOT_EVALUABLE`* | `NOT_EVALUABLE`* | **CONFIRMED** |

*\*Note: Per Section 16 and 53, quantitative accuracy metrics (EM, F1, ANLS) for smoke pipeline verification are designated `NOT_EVALUABLE` because the smoke test verifies pipeline plumbing and artifact serialization rather than benchmark performance. Scientific benchmark scores will only be computed on formal dataset splits during Phase 9.*

---

## 2. Research Benchmark Status (Full Matrix)

In strict accordance with `phases.md` and `configs/phase0/experiment_matrix.yaml`:
Large-scale benchmarking across all 7 research datasets occurs in Phase 9 after adaptive routing, degradation benchmarking, and retrieval modules are implemented.

| Dataset | Split | B0 Status | B1 Status | B2 Status | B3 Status | B4 Status | B5 Status | B6 Status | PROPOSED Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **DocVQA** | `test` | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN |
| **FUNSD** | `test` | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN |
| **SROIE** | `test` | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN |
| **CORD** | `test` | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN |
| **MMLongBench-Doc** | `test` | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN |
| **LongDocURL** | `test` | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN |
| **XL-DocBench** | `test` | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN |
