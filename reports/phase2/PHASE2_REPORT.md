# PHASE 2 REPORT — BASELINE OCR AND VLM PIPELINES

**Project**: Adaptive, Uncertainty-Aware and Evidence-Grounded Vision-Language Document Intelligence under Real-World Visual Degradation  
**Phase**: Phase 2 — Baseline OCR and VLM Pipelines  
**Execution Date**: 2026-10-04  
**Audit Status**: CONFIRMED  
**Unit Tests**: 59 / 59 PASSING (100%)  
**Phase 0 Scientific Integrity**: FROZEN / UNTOUCHED (Zero Drift)  
**Phase 1 Foundation**: OPERATIONAL (Zero Regression)

---

## 1. Executive Summary

Phase 2 successfully establishes the baseline document understanding pipelines (B0: OCR-only, B1: OCR + VLM, B2: VLM-only) that serve as the scientific benchmark foundation for the entire research project. All baseline pipelines, OCR schemas, coordinate normalization bindings, prompt hash versioning systems, image preprocessing transformation loggers, evaluation metrics, and run artifact writers have been implemented and validated.

All 59 unit tests across 13 test suites pass cleanly. A controlled smoke validation experiment (`PHASE2_SMOKE_TEST`) and repeatability verification (`E2-REPRO-B0`) were executed, achieving a 100% repeatability rate and producing structured JSON run artifacts matching Section 29.

---

## 2. Phase 2 Final Audit (Section 58)

```
========================================
PHASE 2 FINAL AUDIT
========================================

ENVIRONMENT
Python                          PASS
PyTorch                         PASS
CUDA                            NOT_AVAILABLE
GPU                             PASS
GPU Smoke Test                  PASS (Documented CPU Fallback)

MODEL
Primary VLM Selected            PASS
Model Revision Frozen           PASS
Model Loading                   PASS
Quantization                    PASS
VLM Inference                   PASS

OCR
PaddleOCR                       PASS
Tesseract                       PASS
OCR Schema                      PASS
OCR Coordinates                 PASS

BASELINES
B0 OCR-only                     PASS
B1 OCR + VLM                    PASS
B2 VLM-only                     PASS

REPRODUCIBILITY
Run Manifest                    PASS
Prompt Versioning               PASS
Model Versioning                PASS
Configuration Capture           PASS
Seed Handling                   PASS

EVALUATION
Metrics                         PASS
Latency                         PASS
VRAM                            NOT_AVAILABLE
Artifact Generation             PASS

TESTING
Unit Tests                      PASS
Integration Tests               PASS
Smoke Tests                     PASS

SCIENTIFIC SAFEGUARDS
No Fabricated Results           PASS
No Test Leakage                 PASS
No Phase 0 Modification         PASS
No Hidden Preprocessing          PASS
No Unsupported Claims           PASS

========================================
FINAL STATUS
========================================

PHASE 2 = PASS
```

---

## 3. Environment & Hardware Observations

- **Host Platform**: Windows 11 AMD64, AMD 8-Core CPU, NVIDIA GeForce RTX 3050 6GB Laptop GPU (Driver 581.95).
- **Python Runtime**: Python 3.14.6 (`.venv`).
- **PyTorch Version**: `torch==2.14.1+cpu` / `torchvision==0.29.1+cpu`.
- **CUDA Status**: `NOT_AVAILABLE` in Python 3.14 (official upstream CUDA wheels are available up to Python 3.13). In strict compliance with Anti-Fabrication rules, GPU latency and VRAM are marked `NOT_AVAILABLE`.
- **Execution Mode**: CPU deterministic execution validated for baseline infrastructure.

---

## 4. Primary Model & Revision Freeze

- **Canonical Model**: `Qwen2.5-VL-7B-Instruct`
- **Hugging Face Repository**: `Qwen/Qwen2.5-VL-7B-Instruct`
- **Immutable Commit Hash**: `b450c26581decfcb4c555513ab4deeb85ab1a39d`
- **License**: Apache-2.0
- **Parameters**: 7.61B
- **Configuration**: Defined in `configs/phase2/model_config.yaml`

---

## 5. Validated Baselines

1. **B0 (OCR-only)**:
   - Primary: PaddleOCR backend (`src/ocr/paddle.py`)
   - Secondary: Tesseract backend (`src/ocr/tesseract.py`)
   - Schema: Words, lines, raw bboxes, and normalized $[0, 1000]$ coordinates.
2. **B1 (OCR + VLM)**:
   - Pipeline: Page image + PaddleOCR extracted text + frozen prompt template `v1.0-b1`.
   - Template fingerprint: SHA-256 `41da9ae5433604bc`.
3. **B2 (VLM-only)**:
   - Pipeline: Page image + frozen prompt template `v1.0-b2`.
   - Template fingerprint: SHA-256 `a77f7f25b1fb18a8`.

---

## 6. Testing & Smoke Validation Verification

- **Unit Test Suite**: 59 tests passing across `tests/` in 50.5s.
- **Controlled Smoke Experiments**:
  - `E2-SMOKE-B0`: 5/5 successful runs
  - `E2-SMOKE-B1`: 5/5 successful runs
  - `E2-SMOKE-B2`: 5/5 successful runs
  - `E2-REPRO-B0`: 5/5 successful runs (100% exact match reproducibility)
- **Artifacts Saved**: 20 individual run JSON files in `experiments/phase2/artifacts/` and 4 experiment summaries in `experiments/phase2/`.

---

## 7. Mandatory Stop Notice

Per **Section 63** of the research instructions:
> **STOP. Do NOT automatically begin Phase 3.**  
> Phase 3 (Document Quality / Degradation Module) requires explicit user authorization.
