# Phase 6: Long-Document Multimodal Retrieval Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement a scientifically validated, zero-leakage, deterministic Hierarchical Multimodal Retrieval subsystem (coarse page retrieval + fine region retrieval + multimodal fusion + optional reranker + standardized `EvidencePackage`) to reduce the computational burden of document-level VLM reasoning while preserving high evidence recall across clean and degraded documents.

**Architecture:** Hierarchical document indexing and retrieval architecture comprising pure-Python deterministic BM25 lexical search, dense text projection retrieval, multi-scale visual layout feature retrieval, configurable hybrid score fusion ($\alpha=0.60$), cross-modal reranker, $[0, 1000]$ normalized spatial region selector, and standardized JSON `EvidencePackage` serialization with complete cryptographic provenance.

**Tech Stack:** Python 3.14.6, PyTorch (CPU-only), scikit-learn, numpy, pydantic, Pillow, PyYAML, pytest.

**Spec:** PRD (`prd.md`), Architecture (`architecture.md`), Rules (`rules.md`), Phases (`phases.md`), Research Protocol (`research_protocol.md`), and Master Implementation Prompt for Phase 6.

## Global Constraints
- Preserve Phase 0 through Phase 5.1 scientific immutability (commits `e38c12d`, `bde2b53`, `609ac2d`, `d7cb76f`, `1caa4b0`, `deacf9a`, `a01bed0`, `3dfa2a2`).
- Zero test-set leakage: No test queries, test answers, or test degradation severity may influence retrieval indices, top-$K$, or fusion weights $\alpha$.
- Strict anti-fabrication: Never invent numbers, recall, MRR, nDCG, latency, or VLM page reduction. Use `NOT_RUN`, `CONFIRMED`, `NOT_AVAILABLE`.
- Software-only execution: Local CPU-only deterministic execution without cloud APIs or external unverified downloads.
- Local commit only: `feat(phase6): implement long-document multimodal retrieval`. DO NOT push to remote. DO NOT start Phase 7.

## Review Focus
1. Non-text pages or empty OCR strings: BM25 must gracefully handle empty tokens with zero score without crashing or throwing ZeroDivisionError.
2. Single-page documents vs multi-page documents: Page reduction ratio must be well-defined ($1 - \min(K, N)/N$ or 0 when $N \le K$).
3. Score normalization edge cases: Min-max normalization when $\max = \min$ (uniform scores) must default safely to 0.5 or 1.0 without dividing by zero.
4. Bounding box coordinates: Region retrieval must strictly enforce normalized integer bounds $[0, 1000]$ with $[x_{\min}, y_{\min}, x_{\max}, y_{\max}]$.
5. Run ID collision: Cryptographic hash and structured format `run_P6_{dataset}_{method}_{doc}_{query}_s{seed}` must produce unique IDs across all experimental runs.

---

### Task 1: Configuration System (`configs/phase6/`)
**Files:**
- Create: `configs/phase6/retrieval_config.yaml`
- Create: `configs/phase6/embedding_config.yaml`
- Create: `configs/phase6/index_config.yaml`
- Create: `configs/phase6/fusion_config.yaml`
- Create: `configs/phase6/reranker_config.yaml`
- Create: `configs/phase6/evaluation_config.yaml`
- Create: `configs/phase6/experiment_matrix.yaml`
- Test: `tests/test_phase6_schema.py`

**Steps:**
- [ ] Create YAML configuration files specifying retrieval pipeline parameters, fusion weight $\alpha=0.60$, candidate cutoffs $K \in \{1, 3, 5, 10, 20\}$, region cutoffs $M \in \{1, 3, 5\}$, and dataset matrices.
- [ ] Verify configurations load cleanly with PyYAML.

---

### Task 2: Core Retrieval Schemas (`src/retrieval/schema.py`)
**Files:**
- Create: `src/retrieval/schema.py`
- Test: `tests/test_phase6_schema.py`

**Steps:**
- [ ] Define Pydantic models: `DocumentPageRecord`, `DocumentRegionRecord`, `RetrievalQuery`, `PageRetrievalResult`, `RegionRetrievalResult`, `EvidencePackage`, `RetrievalMetricsResult`.
- [ ] Write unit tests in `tests/test_phase6_schema.py` verifying model validation, serialization, and coordinate bounding constraints.
- [ ] Run pytest to verify all schema tests pass.

---

### Task 3: Lexical Retrieval Engine (`src/retrieval/bm25.py` & `src/retrieval/text_index.py`)
**Files:**
- Create: `src/retrieval/bm25.py`
- Create: `src/retrieval/text_index.py`
- Test: `tests/test_phase6_bm25.py`

**Steps:**
- [ ] Implement deterministic BM25Okapi ($k_1=1.5, b=0.75$) with pure-Python tokenization, length normalization, and smoothed IDF.
- [ ] Implement `TextIndex` for page-level inverted index creation, document storage, and query scoring.
- [ ] Write unit tests in `tests/test_phase6_bm25.py` testing exact keyword matches, ranking order, and empty query/document edge cases.
- [ ] Run pytest to verify BM25 tests pass.

---

### Task 4: Dense Text & Visual Vector Engines (`src/retrieval/dense_retrieval.py` & `src/retrieval/visual_index.py`)
**Files:**
- Create: `src/retrieval/dense_retrieval.py`
- Create: `src/retrieval/visual_index.py`
- Test: `tests/test_phase6_dense_retrieval.py`
- Test: `tests/test_phase6_visual_retrieval.py`

**Steps:**
- [ ] Implement `DenseTextRetriever` using scikit-learn TF-IDF / LSA projection with normalized vector cosine similarity.
- [ ] Implement `VisualRetriever` using multi-scale spatial grid color/gradient descriptors (or lightweight deterministic CNN feature representation) normalized to unit hypersphere.
- [ ] Write tests in `tests/test_phase6_dense_retrieval.py` and `tests/test_phase6_visual_retrieval.py`.
- [ ] Run pytest to verify dense and visual retrieval tests pass.

---

### Task 5: Multimodal Fusion & Reranker (`src/retrieval/fusion.py` & `src/retrieval/reranker.py`)
**Files:**
- Create: `src/retrieval/fusion.py`
- Create: `src/retrieval/reranker.py`
- Test: `tests/test_phase6_fusion.py`
- Test: `tests/test_phase6_reranker.py`

**Steps:**
- [ ] Implement `MultimodalFusion` supporting min-max and rank-based score normalization and weighted linear combination $S = \alpha S_{\text{text}} + (1 - \alpha) S_{\text{visual}}$ ($\alpha=0.60$).
- [ ] Implement `CrossModalReranker` filtering top-$K$ page candidates down to top-$M$ with region-level cross-modal alignment scoring.
- [ ] Write tests in `tests/test_phase6_fusion.py` and `tests/test_phase6_reranker.py`.
- [ ] Run pytest to verify fusion and reranking tests pass.

---

### Task 6: Region Retrieval, Evidence Packaging & Provenance (`src/retrieval/region.py`, `src/retrieval/evidence.py`, `src/retrieval/provenance.py`)
**Files:**
- Create: `src/retrieval/region.py`
- Create: `src/retrieval/evidence.py`
- Create: `src/retrieval/provenance.py`
- Test: `tests/test_phase6_evidence.py`
- Test: `tests/test_phase6_provenance.py`

**Steps:**
- [ ] Implement sub-page region indexing and retrieval with $[0, 1000]$ normalized bounding box scoring.
- [ ] Implement `EvidencePackageBuilder` packaging selected pages, selected regions, confidence scores, and parent metadata into an immutable `EvidencePackage`.
- [ ] Implement cryptographic provenance tracking run IDs (`run_P6_...`), document hashes, query hashes, config hashes, and git commit hash.
- [ ] Write tests in `tests/test_phase6_evidence.py` and `tests/test_phase6_provenance.py`.
- [ ] Run pytest to verify evidence and provenance tests pass.

---

### Task 7: Retrieval Metrics & Unified Pipeline (`src/retrieval/metrics.py`, `src/retrieval/page_index.py`, `src/retrieval/pipeline.py`)
**Files:**
- Create: `src/retrieval/metrics.py`
- Create: `src/retrieval/page_index.py`
- Create: `src/retrieval/pipeline.py`
- Modify: `src/retrieval/__init__.py`
- Test: `tests/test_phase6_metrics.py`
- Test: `tests/test_phase6_determinism.py`
- Test: `tests/test_phase6_no_leakage.py`
- Test: `tests/test_phase6_trace_identity.py`
- Test: `tests/test_phase6_partition_integrity.py`

**Steps:**
- [ ] Implement retrieval evaluation metrics: Recall@K ($K \in \{1, 3, 5, 10, 20\}$), MRR, nDCG@K, Page Recall, Region Recall, VLM Page Reduction Ratio ($1 - N_{\text{VLM}}/N_{\text{total}}$), and latency timers.
- [ ] Implement `PageIndex` and master `MultimodalRetrievalPipeline` orchestrating document page extraction, indexing, query execution, and evidence packaging for baselines B6-0 through B6-5.
- [ ] Write tests for metrics, determinism, zero-leakage AST verification, trace identity, and partition integrity.
- [ ] Run pytest to verify all unit tests pass.

---

### Task 8: Experiment Runners & Scripts (`scripts/run_phase6_*.py`)
**Files:**
- Create: `scripts/run_phase6_index.py`
- Create: `scripts/run_phase6_smoke.py`
- Create: `scripts/run_phase6_validation.py`
- Create: `scripts/run_phase6_benchmark.py`
- Create: `scripts/run_phase6_ablations.py`

**Steps:**
- [ ] Implement index builder script for multi-page synthetic and sampled evaluation documents across clean and degraded variants.
- [ ] Implement smoke test script verifying full pipeline execution and artifact persistence.
- [ ] Implement validation script performing calibration and parameter verification on validation partition.
- [ ] Implement full benchmark script executing B6-0 through B6-5 across all conditions, computing bootstrap statistical significance ($B=10,000$) for H4.
- [ ] Implement ablations script running A1–A8 retrieval ablations.
- [ ] Run smoke test, validation, benchmark, and ablations scripts.

---

### Task 9: Phase 6 Documentation & Reports (`reports/phase6/` & `PHASE6_REPORT.md`)
**Files:**
- Create: `reports/phase6/` (16 detailed reports)
- Create: `reports/phase6/PHASE6_REPORT.md` (Comprehensive master report with all 30 sections)

**Steps:**
- [ ] Generate all 16 detailed reports from empirical benchmark and ablation results.
- [ ] Generate comprehensive `PHASE6_REPORT.md` incorporating all 30 required sections, evidence packages, latency profiles, statistical significance, and formal H4 evaluation.

---

### Task 10: Governance Updates & Final Sign-Off
**Files:**
- Modify: `task.md`
- Modify: `phases.md`
- Modify: `memory.md`

**Steps:**
- [ ] Update `task.md` with all Phase 6 tasks marked PASS with empirical evidence.
- [ ] Update `phases.md` marking Phase 6 complete.
- [ ] Update `memory.md` recording all Phase 6 conclusions, metrics, and artifact paths.
- [ ] Run full repository test suite (all 178 regression tests + all Phase 6 tests).
- [ ] Create clean local git commit `feat(phase6): implement long-document multimodal retrieval`.
