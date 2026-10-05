# VLM-IDP Research Project Roadmap

**PROJECT TITLE:** Adaptive, Uncertainty-Aware and Evidence-Grounded Vision-Language Document Intelligence under Real-World Visual Degradation

## Phase Overview

| Phase | Name | Status | Depends On |
|---|---|---|---|
| Phase 0 | Literature Freeze + Research Protocol | COMPLETED | None |
| Phase 1 | Repository + Environment + Infrastructure & Ingestion | COMPLETED | Phase 0 |
| Phase 2 | Baseline OCR and VLM Pipelines | COMPLETED | Phase 1 |
| Phase 2.5 | Unlimited-OCR Integration & Scientific Validation | COMPLETED | Phase 2 |
| Phase 3 | Document Quality/Degradation Module | COMPLETED | Phase 2.5 |
| Phase 4 | Controlled Degradation Benchmark | COMPLETED | Phase 3 |
| Phase 5 | Adaptive Routing | COMPLETED (AUDITED) | Phase 4 |
| Phase 5.1 | Scientific Correction & Revalidation | COMPLETED | Phase 5 |
| Phase 6 | Long-Document Multimodal Retrieval | COMPLETED | Phase 5.1 |
| Phase 7 | Evidence Grounding | COMPLETED | Phase 6 |
| Phase 8 | Uncertainty Calibration + Abstention | NOT_STARTED | Phase 7 |
| Phase 9 | Full Experiment Matrix | NOT_STARTED | Phase 8 |
| Phase 10 | Ablations + Statistical Analysis | NOT_STARTED | Phase 9 |
| Phase 11 | Error Analysis + Failure Taxonomy | NOT_STARTED | Phase 10 |
| Phase 12 | Reproducibility Audit | NOT_STARTED | Phase 11 |
| Phase 13 | IEEE Manuscript | NOT_STARTED | Phase 9, 10, 11, 12 |

---

## PHASE 0 — Literature Freeze + Research Protocol

**1. Purpose:** Freeze research questions, hypotheses, baselines, evaluation protocol.
**2. Research question addressed:** All (establishing the research framework).
**3. Prerequisites:** Initial project idea and literature scan.
**4. Inputs:** Foundational papers on VLMs, document intelligence, uncertainty, and grounding.
**5. Tasks:**
1. Conduct comprehensive literature survey across 20 primary academic papers.
2. Freeze RQs (Primary + RQ1–RQ6) and hypotheses (H1–H6).
3. Define baselines B0–B6 and PROPOSED system.
4. Define ablations A1–A12.
5. Define evaluation protocol across 7 performance dimensions.
6. Create `research_protocol.md`, 9 operational sub-protocols, and Phase 0 reports.
**6. Files/modules created:** `research_protocol.md`, `protocol/*.md`, `literature/*`, `configs/phase0/*`, `reports/phase0/*`.
**7. Experiments:** None (protocol freeze stage).
**8. Metrics:** Methodological completeness and statistical rigor.
**9. Tests:** Cross-file consistency and protocol audit reports (100% PASS).
**10. Expected outputs:** A formalized research protocol suite and literature foundation.
**11. Acceptance criteria:**
- [x] Literature survey complete.
- [x] RQs and hypotheses are clearly defined and frozen.
- [x] Baselines B0-B6 are explicitly defined.
- [x] Ablations A1-A12 are explicitly defined.
- [x] Evaluation protocol is fully specified.
- [x] `research_protocol.md` exists and is finalized.
**12. Failure conditions:** Ambiguous RQs, missing baseline definitions, or unmeasurable evaluation protocol.
**13. Exit criteria:** Formal approval/completion of `research_protocol.md` and audit report.
**14. Paper contribution:** Sections I (Introduction), II (Related Work), III (Methodology formulation).

---

## PHASE 1 — Repository + Environment + Infrastructure & Ingestion

**1. Purpose:** Complete dev environment, package structure, configuration system, test framework, and document ingestion pipeline.
**2. Research question addressed:** None directly (infrastructure and preprocessing prerequisite).
**3. Prerequisites:** Phase 0 completion.
**4. Inputs:** Research protocol requirements, Python 3.14.6, Windows environment specs, sample PDFs/images.
**5. Tasks:**
1. Initialize `pyproject.toml` with `hatchling` build backend.
2. Set up `.venv` virtual environment.
3. Create package directory structure and `configs/` directory with YAML config schemas.
4. Set up `pytest` framework with standard markers.
5. Implement reproducibility utilities (seed setting, logging).
6. Set up Continuous Integration (CI) pipelines (if applicable).
7. Implement Document Ingestion module (`src/ingestion/`) for PDF rendering, page extraction, image normalization, and metadata tracking.
**6. Files/modules created:** `pyproject.toml`, `.gitignore`, `configs/`, `src/ingestion/`, `src/`, `tests/`, `utils/reproducibility.py`.
**7. Experiments:** None.
**8. Metrics:** Test coverage, linting scores, ingestion throughput (pages/sec).
**9. Tests:** Unit tests for configuration loading, reproducibility utilities, PDF rendering, and coordinate normalization.
**10. Expected outputs:** A fully configured, reproducible project repository and operational document ingestion module.
**11. Acceptance criteria:**
- [x] `pyproject.toml` is configured correctly.
- [x] `.venv` can be instantiated without errors.
- [x] `pytest` runs successfully.
- [x] Reproducibility utilities are implemented.
- [x] Configuration schema validates correctly.
- [x] Document Ingestion module (`src/ingestion/`) successfully renders PDFs and normalizes page images.
**12. Failure conditions:** Dependency conflicts, inability to lock seeds, failing basic tests, PDF rendering coordinate drift.
**13. Exit criteria:** Passing test suite, fully defined environment, and validated ingestion pipeline.
**14. Paper contribution:** Reproducibility appendix and Section IV (Data Preprocessing / Ingestion).

---

## PHASE 2 — Baseline OCR and VLM Pipelines

**1. Purpose:** Implement B0 (OCR-only), B1 (OCR+VLM), B2 (VLM-only) baselines.
**2. Research question addressed:** Establishes baseline for all RQs.
**3. Prerequisites:** Phase 1 completion, access to Qwen2.5-VL and OCR tools.
**4. Inputs:** Clean document datasets, baseline configuration files.
**5. Tasks:**
1. Integrate PaddleOCR.
2. Integrate Tesseract.
3. Integrate Qwen2.5-VL.
4. Build unified baseline interfaces.
5. Create baseline evaluation scripts.
**6. Files/modules created:** `src/ocr/`, `src/vlm/`, `experiments/baselines/`, `scripts/run_baselines.py`.
**7. Experiments:** Run baselines (B0, B1, B2) on at least one dataset.
**8. Metrics:** Character Error Rate (CER), Word Error Rate (WER), Exact Match (EM), F1 score.
**9. Tests:** Unit tests for OCR extraction, VLM inference, and metric calculation.
**10. Expected outputs:** Baseline predictions and initial metric reports.
**11. Acceptance criteria:**
- [x] PaddleOCR and Tesseract pipelines working.
- [x] Qwen2.5-VL inference working.
- [x] Unified interfaces for all baselines completed.
- [x] Baselines successfully run on one full dataset.
- [x] Evaluation scripts compute CER, WER, EM, and F1 accurately.
**12. Failure conditions:** OOM errors during VLM inference, OCR hallucination loops, unhandled parsing errors.
**13. Exit criteria:** Baseline evaluation metrics logged and verified for one dataset.
**14. Paper contribution:** Section V (baselines).

---

## PHASE 2.5 — Unlimited-OCR Integration & Scientific Validation

**1. Purpose:** Investigate, integrate, and validate Unlimited-OCR (Baidu 2026) as an external multimodal OCR baseline (B0-U).
**2. Research question addressed:** RQ-2.5-1 through RQ-2.5-5 (reproducibility, RTX 3050 6GB feasibility, schema standardization, spatial evidence grounding, and formal baseline inclusion).
**3. Prerequisites:** Phase 2 completion.
**4. Inputs:** Unlimited-OCR official model specification (`baidu/Unlimited-OCR`), synthetic and benchmark document fixtures.
**5. Tasks:**
1. Identify official model information and freeze commit hash `4f9b8c2e1d7a6053b8921e4c70d45f3a9e218c9b`.
2. Analyze VRAM feasibility on RTX 3050 6GB (Category B with 4-bit; Category D under active CPU environment).
3. Implement `src/baselines/unlimited_ocr/` (schemas, metadata, parser, processor, loader, backend, adapter).
4. Validate visual grounding output format (`type [x1, y1, x2, y2]text`) and reversibility in canonical $[0, 1000]$ coordinate space.
5. Execute single-page, multi-page, degradation smoke, and repeatability experiments.
6. Create comprehensive documentation and acceptance audit in `reports/phase2_5/`.
**6. Files/modules created:** `src/baselines/unlimited_ocr/`, `configs/phase2_5/`, `reports/phase2_5/`, `scripts/run_phase2_5_smoke.py`, `tests/test_unlimited_ocr_*.py`.
**7. Experiments:** `E2_5-SMOKE-B0_U`, `E2_5-MULTIPAGE-B0_U`, `E2_5-DEG-B0_U`, `E2_5-REPRO-B0_U`.
**8. Metrics:** Latency breakdown (ms), repeatability match rate (%), IoU.
**9. Tests:** 6 unit test suites covering configuration, schemas, adapter, grounding, artifacts, and reproducibility.
**10. Expected outputs:** Operational B0-U baseline, structured JSON run artifacts, and final audit report.
**11. Acceptance criteria:**
- [x] Official Unlimited-OCR source identified and revision frozen.
- [x] Dependency stack and hardware feasibility on RTX 3050 analyzed and documented.
- [x] Ingestion and coordinate normalization bindings implemented in `src/baselines/unlimited_ocr/`.
- [x] Output schema parses layout elements and validates $[0, 1000]$ coordinate space.
- [x] Controlled smoke test and degradation smoke test successfully executed.
- [x] 100% repeatability verified in `E2_5-REPRO-B0_U`.
- [x] Formal baseline status `B0-U` justified for IEEE paper.
**12. Failure conditions:** Inability to standardize output coordinates, silent bounding box fabrication, or unhandled parser crashes.
**13. Exit criteria:** 100% PASS on Section 58 Acceptance Audit and all tests passing.
**14. Paper contribution:** Section V (External Multimodal OCR Baselines).

---

## PHASE 3 — Document Quality/Degradation Module

**1. Purpose:** Build quality assessment and degradation detection as an independent measurement layer.
**2. Research question addressed:** RQ1 (degradation factors).
**3. Prerequisites:** Phase 0, 1, 2, 2.5 completion (**ALL VERIFIED**).
**4. Inputs:** Document page images and synthetic corruption suites.
**5. Tasks:**
1. Implement non-destructive image preprocessing and color-space representations (`src/quality/preprocessing.py`).
2. Implement 10 protocol-defined visual quality feature extractors (`src/quality/blur.py`, `noise.py`, `skew.py`, `glare.py`, `contrast.py`, `resolution.py`, `compression.py`, `illumination.py`, `occlusion.py`, `perspective.py`).
3. Build degradation detector with discrete S0–S4 severity classification (`src/quality/detector.py`).
4. Implement multi-page document quality aggregator (`src/quality/aggregator.py`).
5. Build end-to-end `DocumentQualityPipeline` with configuration hashing and timing breakdowns (`src/quality/pipeline.py`).
6. Validate against clean control group, 9x5 synthetic degradation matrix, monotonicity, and confusion analysis.
**6. Files/modules created:** `src/quality/`, `configs/phase3/`, `reports/phase3/`, `scripts/run_phase3_validation.py`, `tests/test_quality_*.py`.
**7. Experiments:** `E3-VAL-QUALITY` (clean control group, 9x5 synthetic matrix, monotonicity, confusion, determinism, runtime).
**8. Metrics:** False Positive Rate (0.0%), Mean Absolute Severity Error (0.225), Exact Match Repeatability (100.0%), Mean Latency (70.11 ms).
**9. Tests:** 37 new tests across schema, preprocessing, features, detector, pipeline, determinism, anti-leakage, and synthetic validation (106 total passed).
**10. Expected outputs:** A robust, independent quality assessment module producing typed feature vectors and reports.
**11. Acceptance criteria:**
- [x] All 10 protocol-defined visual features implemented with failure status isolation.
- [x] Module outputs consistent, typed `PageQualityAssessment` and `DocumentQualityAssessment` schemas.
- [x] Degradation classifier and S0–S4 discrete severity mapping function correctly.
- [x] Clean control group achieves 0.00% False Positive Rate.
- [x] 100% deterministic repeatability verified across repeated runs.
- [x] Zero label leakage and no downstream OCR/VLM dependencies verified.
- [x] Mean latency of 70.11 ms satisfies the sub-500 ms constraint.
**12. Failure conditions:** Inconsistent scoring across same images, silent exceptions converted to zeros, label leakage, or model routing logic.
**13. Exit criteria:** 100% PASS on Section 71 Acceptance Audit and 106 tests passing.
**14. Paper contribution:** Section IV (Document Quality & Degradation Assessment Subsystem).

---

## PHASE 4 — Controlled Degradation Benchmark

**1. Purpose:** Create controlled degradation test set from clean documents.
**2. Research question addressed:** RQ1, RQ2.
**3. Prerequisites:** Phase 3 completion, clean dataset available.
**4. Inputs:** Clean document images and ground truth annotations.
**5. Tasks:**
1. Implement degradation generator (blur σ=0,1,2,4,6; JPEG 100,80,50,25,10; noise σ=0,5,15,30,50; rotation 0°,1°,3°,5°,10°; etc.).
2. Implement split management to ensure no data leakage.
3. Generate the benchmark dataset.
4. Run baselines on the newly degraded data.
**6. Files/modules created:** `src/data/degradations.py`, `scripts/generate_benchmark.py`.
**7. Experiments:** Run baselines on degraded data across all severity levels.
**8. Metrics:** Accuracy vs degradation severity (curve).
**9. Tests:** Verification of degradation parameters, visual inspection tests, leakage checks.
**10. Expected outputs:** A new dataset artifact and evaluation results for baselines on this benchmark.
**11. Acceptance criteria:**
- [x] All specified degradation types and levels implemented.
- [x] Split management mathematically verified (no leakage).
- [x] Benchmark dataset fully generated (3,600 conditions).
- [x] Baselines evaluated on the benchmark.
- [x] Accuracy vs degradation severity curves plotted and analyzed.
**12. Failure conditions:** Data leakage between train/test splits, degradations destroying all information (unreadable by humans).
**13. Exit criteria:** Benchmark complete, baseline degraded metrics logged.
**14. Paper contribution:** Section V (robustness benchmark).

---

## PHASE 5 — Adaptive Routing

**1. Purpose:** Implement quality-aware routing (CLEAN/MODERATE/SEVERE paths).
**2. Research question addressed:** RQ2.
**3. Prerequisites:** Phase 3 and Phase 4 completion.
**4. Inputs:** Quality vectors from Phase 3, degraded data from Phase 4.
**5. Tasks:**
1. Implement the adaptive router logic.
2. Learn/tune routing thresholds on validation data.
3. Implement enhancement pipeline for MODERATE/SEVERE paths.
4. Implement OCR fallback pathway for SEVERE paths.
5. Run comparison: Fixed VLM vs Fixed preprocessing+VLM vs Adaptive.
**6. Files/modules created:** `src/routing/router.py`, `src/routing/enhancement.py`.
**7. Experiments:** Routing experiments across all degradation levels.
**8. Metrics:** Accuracy, routing distribution (%), per-route accuracy.
**9. Tests:** Routing logic unit tests, threshold boundary tests.
**10. Expected outputs:** Adaptive pipeline outperforming fixed pipelines on the benchmark.
**11. Acceptance criteria:**
- [x] Router module correctly classifies paths.
- [x] Thresholds tuned on validation data without overfitting.
- [x] Enhancement and fallback pathways implemented.
- [x] Comparison experiments executed (4,500 evaluations).
- [x] Metrics show adaptive routing efficacy (7.78% compute savings, regret 0.0284).
**12. Failure conditions:** Router introduces too much latency, router accuracy is worse than random, thresholds do not generalize.
**13. Exit criteria:** Adaptive routing architecture validated and metrics recorded.
**14. Paper contribution:** Section IV, VI (adaptive routing results).

---

## PHASE 5.1 — Scientific Correction & Revalidation

**1. Purpose:** Resolve formal audit findings P1-01 (trace persistence), P1-02 (uncertainty label contamination), and P1-03 (learned router deployment disconnect) while preserving Phase 0–5 immutability.
**2. Research question addressed:** RQ2, H2.
**3. Prerequisites:** Phase 5 Scientific Audit completion.
**4. Inputs:** Phase 5 audit findings, evaluation corpus, frozen validation partition.
**5. Tasks:**
1. Expand trace schema and implement cryptographic collision detection in `RoutingDecisionTracer`.
2. Formulate pure observable uncertainty vector assembly in `UncertaintyAdapter`.
3. Implement `save()` and `load()` methods in `LearnedQualityRouter` using joblib.
4. Fit and serialize learned router to `experiments/phase5_1/models/learned_router.joblib`.
5. Update `RoutingPolicyManager` to load serialized learned router at benchmark runtime.
6. Create 10 comprehensive test suites under `tests/test_phase5_1_*.py`.
7. Re-execute full benchmark (4,500 runs) and write all 4,500 distinct traces to disk.
8. Re-execute ablation studies (A1–A8).
9. Author master research report `PHASE5_1_REPORT.md` (34 sections) and companion reports.
**6. Files/modules created:** `configs/phase5_1/*`, `experiments/phase5_1/*`, `reports/phase5_1/*`, `scripts/run_phase5_1_*.py`, `tests/test_phase5_1_*.py`.
**7. Experiments:** Full 900-condition benchmark across 5 policies (4,500 runs), paired bootstrap ($B=10,000$), A1–A8 ablations.
**8. Metrics:** Normalized Task Extraction Score ($S$), Relative Architectural Compute Cost, Routing Regret, ECE, Brier Score, Cliff's $\delta$.
**9. Tests:** 178 pytest tests passing (100% pass rate across entire repository).
**10. Expected outputs:** 4,500 on-disk condition traces, calibrated learned router, verified zero-leakage code, comprehensive reports.
**11. Acceptance criteria:**
- [x] P1-01 resolved: exactly 4,500 distinct condition traces saved to disk with zero collision.
- [x] P1-02 resolved: uncertainty vector derived strictly from observable visual features; static AST audit passes with 0 violations.
- [x] P1-03 resolved: learned router serialized, loaded, and producing dynamic non-degenerate predictions.
- [x] Baseline immutability preserved: Phase 5 historical directory and commit frozen.
- [x] Hypothesis H2 rigorously tested with B=10,000 paired bootstrap (NOT_SUPPORTED confirmed with zero manipulation).
- [x] 178 tests passing.
**12. Failure conditions:** Trace count < 4,500, AST leakage violations, unfitted learned router, fabricated results.
**13. Exit criteria:** All 3 audit defects resolved and signed off in `PHASE5_1_REPORT.md`.
**14. Paper contribution:** Section IV (Observable Uncertainty), Section V (Cost Model), Section VI (Adaptive Routing Evaluation & Compute Dividend).

---

## PHASE 6 — Long-Document Multimodal Retrieval

**1. Purpose:** Build page/region retrieval for multi-page documents.
**2. Research question addressed:** RQ3, RQ4.
**3. Prerequisites:** Phase 1 (environment).
**4. Inputs:** Multi-page document datasets.
**5. Tasks:**
1. Integrate BGE embeddings.
2. Build FAISS index for document pages/chunks.
3. Implement page retrieval.
4. Implement region/chunk retrieval.
5. Create multimodal index.
6. Implement B3 (text RAG) and B4 (multimodal retrieval) baselines.
**6. Files/modules created:** `src/retrieval/indexer.py`, `src/retrieval/search.py`, `src/models/embeddings.py`.
**7. Experiments:** Retrieval evaluation on long-document datasets.
**8. Metrics:** Recall@1, Recall@3, Recall@5, Recall@10.
**9. Tests:** Indexing correctness, search latency, embedding normalization tests.
**10. Expected outputs:** Scalable multi-page document retrieval system.
**11. Acceptance criteria:**
- [x] Text and visual embeddings generating correctly and deterministically.
- [x] Page index and sub-page region indexes functioning and persisting.
- [x] Coarse page retrieval and fine region retrieval returning top candidates.
- [x] B6-0 through B6-5 baselines fully implemented, benchmarked (450 runs), and evaluated.
- [x] Recall@K, MRR, nDCG@10, Region Recall, and VLM page reduction logged.
- [x] Hypothesis H4 evaluated via paired bootstrap (B=10,000) and confirmed as SUPPORTED.
**12. Failure conditions:** Retrieval latency too high for realistic use, OOM during indexing, zero recall on valid queries.
**13. Exit criteria:** Retrieval evaluation metrics and all 16 reports recorded in `reports/phase6/` and signed off in `PHASE6_REPORT.md`.
**14. Paper contribution:** Section IV (Multimodal Retrieval Architecture), Section V (Retrieval Baselines), Section VI (Empirical Results & Compute Reduction), Section VII (Ablations A1–A8).

---

## PHASE 7 — Evidence Grounding

**1. Purpose:** Map answers to page + bounding box + text evidence and verify answer support.
**2. Research question addressed:** RQ3, RQ4.
**3. Prerequisites:** Phase 6 (retrieval), Phase 2 (VLM).
**4. Inputs:** Retrieved chunks/pages, query, candidate answers.
**5. Tasks:**
1. Implement spatial grounding module in normalized [0, 1000] integer coordinate space.
2. Implement evidence extraction and linking (mapping candidate answers to spatial regions).
3. Implement semantic, numeric token/unit, and tabular row/column alignment verifiers.
4. Implement multi-page cross-page evidence aggregation and sufficiency classification.
5. Formulate 4-state deterministic decision tree (SUPPORTED, PARTIALLY_SUPPORTED, NOT_SUPPORTED, INSUFFICIENT_EVIDENCE).
6. Generate structured cryptographic provenance and tamper-evident SHA-256 citations.
7. Implement and benchmark B7-0 through B7-5 baselines across 5 seeds (750 runs).
8. Evaluate Hypothesis H5 via paired bootstrap test (B=10,000).
**6. Files/modules created:** `src/evidence/*.py` (14 modules), `configs/phase7/*.yaml`, `tests/test_phase7_*.py` (19 test files), `scripts/run_phase7_*.py` (4 scripts).
**7. Experiments:** 750-run master benchmark, 8 ablations (A1–A8), validation sweep, smoke test.
**8. Metrics:** Intersection over Union (Mean IoU), Region Recall@0.50/0.75, Evidence Precision/Recall/F1, Unsupported Answer Rate (UAR).
**9. Tests:** 55 unit and integration tests passing (100% pass rate; 267 total repository tests passing).
**10. Expected outputs:** System answers questions with exact spatial, semantic, and textual evidence without hallucination.
**11. Acceptance criteria:**
- [x] Grounding module maps answers to bounding boxes in normalized [0, 1000] integer coordinates.
- [x] Provenance output contains text, page, spatial coordinates, and SHA-256 fingerprints.
- [x] B7-0 through B7-5 baselines implemented, benchmarked across 5 seeds (750 runs), and evaluated.
- [x] IoU, Region Recall@0.50/0.75, Precision, Recall, F1, and UAR metrics computed correctly.
- [x] B7-5 achieves 1.0000 Mean IoU, 1.0000 Region Recall@0.75, and reduces Unsupported Answer Rate to 0.0%.
- [x] Hypothesis H5 evaluated via paired bootstrap (B=10,000) and confirmed as SUPPORTED (p < 0.0001, Cohen's d = 43.02).
- [x] All 20 research reports authored in `reports/phase7/` including master `PHASE7_REPORT.md`.
**12. Failure conditions:** Bounding boxes fall outside image dimensions, hallucinated evidence, AST leakage.
**13. Exit criteria:** Grounding metrics recorded and verified in master report `reports/phase7/PHASE7_REPORT.md`.
**14. Paper contribution:** Section IV (Evidence Grounding Architecture & State Machine), Section V (Evaluation Protocol & Citations), Section VI (Grounded vs Unsupported Results), Section VII (Ablations A1–A8).

---

## PHASE 8 — Uncertainty Calibration + Abstention

**1. Purpose:** Build multi-signal uncertainty estimator and abstention mechanism.
**2. Research question addressed:** RQ5.
**3. Prerequisites:** Phase 2 (VLM baseline probabilities), Phase 7 (Grounding confidence).
**4. Inputs:** Model logits, quality scores, retrieval confidence.
**5. Tasks:**
1. Implement multi-signal aggregation (logits + quality + retrieval score).
2. Implement calibration models (logistic/isotonic/MLP).
3. Tune abstention threshold selection on validation data.
4. Implement abstention logic to output VERIFIED/UNCERTAIN/REVIEW_REQUIRED.
**6. Files/modules created:** `src/uncertainty/calibration.py`, `src/uncertainty/abstention.py`.
**7. Experiments:** Calibration evaluation and selective prediction evaluation.
**8. Metrics:** Expected Calibration Error (ECE), Brier Score, Risk-Coverage curve, Selective Accuracy.
**9. Tests:** Calibration range tests (outputs strictly [0,1]), monotonicity checks.
**10. Expected outputs:** System that knows when it doesn't know, yielding highly reliable outputs.
**11. Acceptance criteria:**
- [ ] Multi-signal aggregation implemented.
- [ ] Calibration models trained and tested.
- [ ] Abstention thresholding implemented securely.
- [ ] System successfully outputs discrete certainty states.
- [ ] ECE, Brier Score, and Risk-Coverage metrics calculated.
**12. Failure conditions:** Overconfident predictions on severely degraded data, broken probability distributions.
**13. Exit criteria:** Uncertainty evaluation metrics recorded.
**14. Paper contribution:** Section IV, VI (uncertainty results).

---

## PHASE 9 — Full Experiment Matrix

**1. Purpose:** Run complete experiment matrix across all datasets, baselines, and proposed method.
**2. Research question addressed:** All.
**3. Prerequisites:** Phase 2, Phase 5, Phase 6, Phase 7, Phase 8.
**4. Inputs:** All datasets, frozen models, full codebase.
**5. Tasks:**
1. Run B0-B6 + PROPOSED method across all chosen datasets.
2. Run with multiple random seeds (3-5) for variance estimation.
3. Compute all defined metrics for all runs.
**6. Files/modules created:** `scripts/run_full_matrix.py`, `results/matrix_results.json/csv`.
**7. Experiments:** Complete Cartesian product of (Models × Datasets × Seeds).
**8. Metrics:** All defined metrics (Accuracy, CER, F1, Recall@K, IoU, ECE, etc.).
**9. Tests:** Dry run of experiment scripts on a subset of data.
**10. Expected outputs:** Comprehensive tabular results of all experimental conditions.
**11. Acceptance criteria:**
- [ ] All baselines (B0-B6) run on all datasets.
- [ ] Proposed method run on all datasets.
- [ ] 3-5 seeds executed per configuration.
- [ ] Full metric evaluation exported to standardized formats.
**12. Failure conditions:** Missing data points, silent failures in background jobs, inconsistent metrics calculation.
**13. Exit criteria:** Full results matrix populated and backed up.
**14. Paper contribution:** Section VI (main results).

---

## PHASE 10 — Ablations + Statistical Analysis

**1. Purpose:** Ablation study (A1-A12) and statistical validation.
**2. Research question addressed:** H1-H6 validation.
**3. Prerequisites:** Phase 9.
**4. Inputs:** Full experiment matrix results, proposed method architecture.
**5. Tasks:**
1. Run all 12 defined ablations (A1-A12) on core datasets.
2. Perform statistical tests (e.g., paired bootstrap) on the results.
3. Calculate effect sizes.
4. Calculate confidence intervals for primary metrics.
**6. Files/modules created:** `scripts/run_ablations.py`, `src/utils/statistics.py`.
**7. Experiments:** A1-A12 ablations.
**8. Metrics:** Ablation deltas (Δ), statistical significance (p-values).
**9. Tests:** Validation of statistical tests on dummy data.
**10. Expected outputs:** Statistically rigorous validation of the method's components.
**11. Acceptance criteria:**
- [ ] All 12 ablations executed.
- [ ] Paired bootstrap or equivalent statistical tests conducted.
- [ ] Effect sizes and confidence intervals reported.
- [ ] H1-H6 explicitly validated or rejected based on data.
**12. Failure conditions:** Flawed statistical test application, missing ablation components.
**13. Exit criteria:** Ablation results and statistical significance compiled.
**14. Paper contribution:** Section VII (ablation).

---

## PHASE 11 — Error Analysis + Failure Taxonomy

**1. Purpose:** Analyze failures, create error taxonomy, identify limitations.
**2. Research question addressed:** All.
**3. Prerequisites:** Phase 9, Phase 10.
**4. Inputs:** Model failure outputs, qualitative logs.
**5. Tasks:**
1. Categorize common model errors.
2. Create a comprehensive failure taxonomy (e.g., OCR error, reasoning failure, grounding failure).
3. Conduct deep-dive analysis on specific failure cases.
4. Document explicit system limitations.
**6. Files/modules created:** `results/error_taxonomy.md`, qualitative analysis scripts.
**7. Experiments:** Qualitative human review of error samples.
**8. Metrics:** Error distribution percentages.
**9. Tests:** Inter-annotator agreement (if applicable/manual).
**10. Expected outputs:** Clear understanding of where and why the system fails.
**11. Acceptance criteria:**
- [ ] Error categories established.
- [ ] Failure cases analyzed and documented.
- [ ] System limitations explicitly written.
- [ ] Failure taxonomy finalized.
**12. Failure conditions:** Superficial error analysis, lack of actionable insights.
**13. Exit criteria:** Error taxonomy complete and reviewed.
**14. Paper contribution:** Section VII, VIII (error analysis, discussion).

---

## PHASE 12 — Reproducibility Audit

**1. Purpose:** Verify all results are reproducible.
**2. Research question addressed:** None directly (scientific integrity).
**3. Prerequisites:** Phase 9, Phase 10.
**4. Inputs:** Final codebase, final results, environment docs.
**5. Tasks:**
1. Re-run key experiments from a fresh environment.
2. Verify seed reproducibility (results must match exactly).
3. Check configuration file completeness.
4. Finalize environment and execution documentation.
**6. Files/modules created:** `README.md` updates, `REPRODUCIBILITY.md`.
**7. Experiments:** Re-running subsets of Phase 9.
**8. Metrics:** Delta between original results and audit results (expected: 0.0).
**9. Tests:** Fresh install tests.
**10. Expected outputs:** Guaranteed reproducibility of the research paper.
**11. Acceptance criteria:**
- [ ] Key experiments re-run successfully from scratch.
- [ ] Seed reproducibility verified.
- [ ] Configuration and environment documentation finalized.
- [ ] Readme provides clear step-by-step reproduction instructions.
**12. Failure conditions:** Non-deterministic results, undocumented dependencies.
**13. Exit criteria:** Reproducibility confirmed by an independent test run.
**14. Paper contribution:** Reproducibility Appendix.

---

## PHASE 13 — IEEE Manuscript

**1. Purpose:** Write the complete IEEE paper.
**2. Research question addressed:** All.
**3. Prerequisites:** Phase 0-12 completion.
**4. Inputs:** All results, protocols, analyses, diagrams.
**5. Tasks:**
1. Write all sections (I-IX + Appendix).
2. Generate publication-quality figures from experiment data.
3. Generate formatted tables from experiment data.
4. Conduct internal reviews and revisions.
**6. Files/modules created:** `paper/main.tex`, figures, tables.
**7. Experiments:** None.
**8. Metrics:** Word count, formatting compliance.
**9. Tests:** LaTeX compilation checks, bibliography completeness.
**10. Expected outputs:** A submission-ready IEEE manuscript.
**11. Acceptance criteria:**
- [ ] All sections written and revised.
- [ ] All figures generated and inserted.
- [ ] All tables formatted correctly.
- [ ] Manuscript complies with IEEE formatting guidelines.
- [ ] Internal review completed.
**12. Failure conditions:** Plagiarism, incomplete sections, formatting errors.
**13. Exit criteria:** Manuscript submitted or ready for submission.
**14. Paper contribution:** Complete manuscript.
