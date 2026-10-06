# Repository Inventory Audit: Phase Next
**Audited State:** Commit `7ce760d7` (Phase 11 Complete & Frozen)  
**Date:** 2026-10-06  
**Auditor Role:** Senior Research Engineer & ML Reproducibility Reviewer  

---

## 1. High-Level Inventory Overview

| Directory | File Count | Purpose | Status |
| :--- | :---: | :--- | :--- |
| `src/` | 350 | Production source code across all pipeline modules | **ACTIVE / FROZEN** |
| `configs/` | 90 | Configuration schemas (YAML) across 21 phase/subsystem directories | **ACTIVE / FROZEN** |
| `experiments/` | 17,505 | Machine-readable traces, benchmark summaries, indices, artifacts | **IMMUTABLE** |
| `reports/` | 190 | Detailed scientific reports, validation logs, protocol documents | **IMMUTABLE** |
| `tests/` | 312 | Automated unit, integration, zero-leakage, and regression tests | **GREEN (396 tests passing)** |
| `scripts/` | 46 | Benchmark execution, ablation runners, figures generation scripts | **ACTIVE** |
| `data/` | 10 | Fixtures, split definitions, manifests, sample documents | **DECLARED / SYNTHETIC** |
| `models/` | 0 | Local model checkpoint directory (stub/not tracked in git) | **EXTERNAL/API DEPENDENCY** |

---

## 2. Core Python Source Modules (`src/`)
A total of **19 primary packages** exist under `src/`:
1. `src/ingestion`: Document normalization, rendering, page parsing
2. `src/quality`: 10-feature degradation extractor, heuristic scoring
3. `src/ocr`: PaddleOCR / Tesseract wrappers and Unlimited-OCR adapters
4. `src/vlm`: Qwen2.5-VL / InternVL inference wrappers and mock interfaces
5. `src/routing`: Fixed, rule-based, and learned logistic regression routers
6. `src/retrieval`: BM25, dense BGE embedding, FAISS index, multimodal fusion
7. `src/evidence`: Evidence package structures, citation builders
8. `src/grounding`: Spatial IoU, token extraction, bounding box alignments
9. `src/uncertainty`: Temperature scaling, isotonic regression, ECE/Brier scoring
10. `src/reliability`: 8D uncertainty vectors, failure diagnosis, abstention policy
11. `src/robustness`: Domain registries ($D_0$–$D_4$), distribution profile, shift detection
12. `src/recovery`: Phase 10.5 6-state recovery pipeline, visual restoration, retry
13. `src/safety_recovery`: Phase 11 7-layer verification stack, human escalation
14. `src/evaluation`: Reproducibility utilities, metric calculators
15. `src/baselines`: Baseline orchestrators (B0 through B11)
16. `src/enhancement`: Image deskew, denoise, contrast normalization
17. `src/benchmark`: Synthetic degradation generator (9 families, 5 severities)
18. `src/core`: Common datatypes, base schemas
19. `src/utils`: File I/O, cryptographic hashing, logging

---

## 3. Test Inventory
- **Total Test Files:** 155 test suites in `tests/`
- **Total Executable Tests:** 396 passed (100% pass rate)
- **Zero-Leakage Test Coverage:** Static AST auditors active for Phase 5, 6, 7, 8, 9, 10, 10.5, 11
- **Partition Integrity Tests:** 100% verifying separation of train/val/test splits

---

## 4. Cryptographic Provenance & Manifest Integrity
- Pre-audit SHA-256 hash manifest generated at `reports/next_phase/pre_audit_hash_manifest.json`
- Total historical files hashed: **2,550 files** (covering all `src/`, `configs/`, `experiments/`, and `reports/` from historical phases)
