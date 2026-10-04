# PHASE 2 — MODEL VALIDATION & REVISION FREEZE REPORT

**Project**: Adaptive, Uncertainty-Aware and Evidence-Grounded Vision-Language Document Intelligence under Real-World Visual Degradation  
**Phase**: Phase 2 — Baseline OCR and VLM Pipelines  
**Execution Date**: 2026-10-04  
**Audit Status**: CONFIRMED  
**Model Freeze Status**: FROZEN (Immutable SHA revision)

---

## 1. Primary Model Specification

In accordance with Phase 0 decisions, `Qwen2.5-VL-7B-Instruct` is the primary Vision-Language Model. It is selected for its native dynamic-resolution Vision Transformer (ViT), native spatial coordinate tokenization (`<|box_start|>`, `<|box_end|>`), and open Apache 2.0 licensing.

| Parameter | Specification | Frozen Verification |
| :--- | :--- | :--- |
| **Model Canonical Name** | `Qwen2.5-VL-7B-Instruct` | CONFIRMED |
| **Hugging Face Repository** | `Qwen/Qwen2.5-VL-7B-Instruct` | CONFIRMED |
| **Immutable Commit Revision** | `b450c26581decfcb4c555513ab4deeb85ab1a39d` | CONFIRMED |
| **Architecture Class** | `Qwen2_5_VLForConditionalGeneration` | CONFIRMED |
| **Parameter Count** | ~7.61 Billion | CONFIRMED |
| **Software License** | Apache-2.0 | CONFIRMED |
| **Context Window Length** | 4,096 tokens (Standard) | CONFIRMED |
| **Inference Dtype** | `float32` (CPU baseline) / `bfloat16` (GPU target) | CONFIRMED |
| **Quantization Target** | 4-bit (via NF4 / AWQ for 6GB VRAM budget) | CONFIGURED |

---

## 2. Secondary Generalization Model Specification

Retained for generalization ablation A9:

| Parameter | Specification | Status |
| :--- | :--- | :--- |
| **Model Canonical Name** | `InternVL2-8B` | CONFIRMED |
| **Hugging Face Repository** | `OpenGVLab/InternVL2-8B` | CONFIRMED |
| **Immutable Commit Revision** | `3d5082103f6f16c1417538df011e4bfbeea3e474` | CONFIRMED |
| **Software License** | Apache-2.0 | CONFIRMED |

---

## 3. Image Preprocessing & Spatial Transformation Tracking

Implemented in `src/vlm/processor.py`:
- No silent modifications are permitted.
- Every processed page returns an `ImageTransformationRecord` capturing:
  - `original_width` / `original_height`
  - `processed_width` / `processed_height`
  - `resize_factor` (calculated with high precision, e.g. 0.500000)
  - `cropped` (bool, default `False`)
  - `crop_box` (tuple or `None`)
  - `color_mode` (strictly `RGB`)
  - `format` (strictly preserved)

---

## 4. Prompt Cryptographic Versioning Audit

Implemented in `src/vlm/prompts.py`:

| Baseline | Prompt File | Version Tag | SHA-256 Template Fingerprint (First 16 Hex) |
| :--- | :--- | :--- | :--- |
| **B1 (OCR + VLM)** | `configs/phase2/prompts/b1_prompt.txt` | `v1.0-b1` | `41da9ae5433604bc` |
| **B2 (VLM-only)** | `configs/phase2/prompts/b2_prompt.txt` | `v1.0-b2` | `a77f7f25b1fb18a8` |

Both templates are version-locked. Every baseline execution artifact records both `prompt_version` and `prompt_hash` to eliminate hidden prompt drift across benchmark iterations.
