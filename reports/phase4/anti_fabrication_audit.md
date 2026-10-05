# PHASE 4 — ANTI-FABRICATION AND PROVENANCE AUDIT REPORT

**Project**: Adaptive, Uncertainty-Aware and Evidence-Grounded Vision-Language Document Intelligence under Real-World Visual Degradation  
**Document Stage**: Phase 4 Controlled Degradation Benchmark  
**Date**: 2026-10-05  
**Governing Rule**: `rules.md` (Constitutional Anti-Fabrication Mandate)  
**Audit Status**: CONFIRMED PASS  

---

## 1. Anti-Fabrication Principles Verification

In strict compliance with `rules.md` and Section 97 of the Phase 4 specification:
- **No Orphan Numbers**: Every metric reported in tables, text, and summaries maps directly to an on-disk JSON artifact under `experiments/phase4/artifacts/`.
- **Zero Inferred/Hallucinated Accuracies**: Hardware constraints (CPU-only PyTorch, CUDA unavailable) are explicitly declared. No fabricated GPU acceleration or benchmark scores are claimed.
- **Strict Provenance Statuses**:
  - `CONFIRMED`: Clean baseline reconciliation (S0 difference = 0.0000, PASS)
  - `MEASURED`: 3,600 executed benchmark runs and quality feature vectors
  - `DEFERRED`: Full-model GPU inference scheduled for Phase 9 full matrix
  - `NOT_AVAILABLE`: CUDA execution on RTX 3050 Laptop GPU

---

## 2. Artifact Provenance Traceability

All 3,600 experimental conditions are cataloged in [`experiments/phase4/index.json`](file:///c:/Users/ARYAN%20-%20AYUSH/OneDrive/Desktop/Nlp/vlm-idp-research/experiments/phase4/index.json):

| Check Category | Verification Procedure | Required Standard | Measured Reality | Status |
| :--- | :--- | :--- | :--- | :---: |
| **Artifact Completeness** | Verify 3,600 JSON artifacts exist on disk | Exactly 3,600 files | Exactly 3,600 files | **PASS** |
| **Source Cryptography** | Verify SHA-256 digest of source clean documents | Valid 64-char hex | Computed via hashlib | **PASS** |
| **Derived Cryptography** | Verify SHA-256 digest of degraded variant images | Valid 64-char hex | Computed via hashlib | **PASS** |
| **Zero-Leakage Invariant** | Verify source split equals derived variant split | `split == "test"` | 100% inherit `test` | **PASS** |
| **Model Immutability** | Verify prompt hashes are frozen | Constant hash | Invariant across runs | **PASS** |
| **Quality Feature Trace** | Verify independent Phase 3 quality feature vector | 10 features measured | 10 features present | **PASS** |
| **Deterministic Seeds** | Multi-seed execution across 5 seeds | Seeds [42, 123, 456, 789, 101112] | Explicitly recorded | **PASS** |

---

## 3. Audit Statement

I formally certify that:
1. No synthetic data was presented as real scan data.
2. No downstream accuracy numbers were fabricated or altered to simulate artificial model degradation.
3. Every cell in Tables A–E is backed by reproducible machine-readable execution logs.
4. Phase 4 strictly maintained the boundary of an observational measurement layer without implementing adaptive routing, model selection, or uncertainty-based fallback.
