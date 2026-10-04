# PHASE 2 — BASELINE EXPERIMENT REGISTRY

**Project**: Adaptive, Uncertainty-Aware and Evidence-Grounded Vision-Language Document Intelligence under Real-World Visual Degradation  
**Phase**: Phase 2 — Baseline OCR and VLM Pipelines  
**Execution Date**: 2026-10-04  
**Audit Status**: CONFIRMED

---

## 1. Baseline Hierarchy Specification

| Baseline ID | Name | Architectural Description | Models Involved | OCR Engine | Prompt Version | Config File | Implementation Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **B0** | OCR-only | Optical character recognition layout extraction with rule-based entity selection. | None | PaddleOCR (Primary), Tesseract (Baseline) | N/A | `configs/phase2/baseline_config.yaml` | **VALIDATED** |
| **B1** | OCR + VLM | Dual-input VLM conditioning on document page image and full extracted OCR text tokens. | Qwen2.5-VL-7B-Instruct | PaddleOCR | `v1.0-b1` (`41da9ae5433604bc`) | `configs/phase2/baseline_config.yaml` | **VALIDATED** |
| **B2** | VLM-only | Direct Vision-Language Model inference conditioned solely on page image without external text. | Qwen2.5-VL-7B-Instruct | None | `v1.0-b2` (`a77f7f25b1fb18a8`) | `configs/phase2/baseline_config.yaml` | **VALIDATED** |
| **B3** | VLM + Text RAG | Dense chunk retrieval over OCR text followed by VLM reader answering. | Qwen2.5-VL-7B + BGE | PaddleOCR | Reserved Phase 6 | `protocol/baseline_protocol.md` | PLANNED |
| **B4** | VLM + Multimodal Retrieval | Page-level visual embeddings with dense layout retrieval. | Qwen2.5-VL-7B + ColPali/BGE | Optional | Reserved Phase 6 | `protocol/baseline_protocol.md` | PLANNED |
| **B5** | VLM + Spatial Grounding | VLM answer generation with explicit spatial bounding box coordinates. | Qwen2.5-VL-7B | None | Reserved Phase 7 | `protocol/baseline_protocol.md` | PLANNED |
| **B6** | Fixed Preprocessing + VLM | Universal image enhancement (denoise/contrast/deskew) prior to fixed VLM inference. | Qwen2.5-VL-7B | None | Reserved Phase 5 | `protocol/baseline_protocol.md` | PLANNED |
| **PROPOSED** | Integrated Adaptive System | Quality Assessment + Adaptive Routing + Multimodal Index + Evidence Grounding + Uncertainty. | Full Ensemble | Adaptive | Multi-stage | Frozen Protocol | PLANNED |

---

## 2. Phase 2 Validated Baselines Execution Registry

| Run ID | Baseline ID | Target Benchmark | Partition | Sample Count | Random Seed | Hardware Device | Status | Summary Artifact |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `run_smoke_b0` | **B0** | DocVQA Synthetic | `val` | 5 | 42 | CPU | **SUCCESS** | `experiments/phase2/E2-SMOKE-B0_summary.json` |
| `run_smoke_b1` | **B1** | DocVQA Synthetic | `val` | 5 | 42 | CPU | **SUCCESS** | `experiments/phase2/E2-SMOKE-B1_summary.json` |
| `run_smoke_b2` | **B2** | DocVQA Synthetic | `val` | 5 | 42 | CPU | **SUCCESS** | `experiments/phase2/E2-SMOKE-B2_summary.json` |
| `run_repro_b0` | **B0** | DocVQA Synthetic | `val` | 5 | 42 | CPU | **SUCCESS** | `experiments/phase2/E2-REPRO-B0_summary.json` |

---

## 3. Baseline Fairness Rules

In accordance with Section 48 and Section 49:
1. **Identical Inputs**: All baselines evaluate on identical document IDs, page IDs, and question IDs.
2. **Identical Preprocessing**: Image normalization, aspect-ratio scaling, and color space conversion are identical across baselines.
3. **Identical Evaluation**: Answer evaluation uses the exact same `normalize_answer()`, Exact Match, Token F1, and ANLS implementations in `src/evaluation/metrics.py`.
4. **Zero Test-Set Tuning**: All generation hyperparameters and prompt templates remain completely frozen without adaptation.
