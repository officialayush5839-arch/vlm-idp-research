# VLM-IDP Active Execution Queue

CURRENT PHASE: PHASE 5.1 — Scientific Correction & Revalidation (COMPLETED)
CURRENT OBJECTIVE: Phase 5.1 complete. All audit defects (P1-01, P1-02, P1-03) resolved. 4,500 distinct condition traces persisted, zero-leakage verified, learned router serialized and deployed. 178 tests passing (100%). Ready for Phase 6 authorization.
TASK STATUS: COMPLETE

---

### Phase 0 Tasks (Protocol Freeze & Literature Foundation) — ALL COMPLETED

#### T001: Create repository structure
- **Purpose**: Initialize base directories for the research project.
- **Dependencies**: None
- **Input**: User specifications
- **Expected Output**: Standard directory layout (configs/, src/, data/, experiments/, paper/, reports/, tests/, scripts/)
- **Files Affected**: Full repository directory scaffold
- **Acceptance Criteria**: Directories exist according to conventions.
- **Status**: **PASS**
- **Evidence**: Commit `e38c12d` and verification report [`reports/control_file_audit.md`](reports/control_file_audit.md)

#### T004: Create dataset manifest system
- **Purpose**: Define how datasets are tracked and downloaded.
- **Dependencies**: None
- **Input**: Selected Datasets list (7 benchmarks)
- **Expected Output**: `dataset_config.yaml` and `dataset_protocol.md`
- **Files Affected**: `configs/phase0/dataset_config.yaml`, `protocol/dataset_protocol.md`
- **Acceptance Criteria**: Schema for dataset versions, splits, and zero-leakage keys defined.
- **Status**: **PASS**
- **Evidence**: [`configs/phase0/dataset_config.yaml`](configs/phase0/dataset_config.yaml) and [`protocol/dataset_protocol.md`](protocol/dataset_protocol.md)

#### T005: Create model registry & research configuration
- **Purpose**: Track model versions, architectures, and pipeline parameters.
- **Dependencies**: None
- **Input**: Selected Models list
- **Expected Output**: `research_config.yaml`
- **Files Affected**: `configs/phase0/research_config.yaml`
- **Acceptance Criteria**: Primary (Qwen2.5-VL 7B), secondary (InternVL2 8B), OCR (PaddleOCR/Tesseract), and retriever documented.
- **Status**: **PASS**
- **Evidence**: [`configs/phase0/research_config.yaml`](configs/phase0/research_config.yaml)

#### T006: Create experiment configuration schema
- **Purpose**: Standardize experiment execution matrix.
- **Dependencies**: T004, T005
- **Input**: Research protocol parameters
- **Expected Output**: `experiment_matrix.yaml`
- **Files Affected**: `configs/phase0/experiment_matrix.yaml`
- **Acceptance Criteria**: Complete schema covering baselines, degradation grid, and ablations.
- **Status**: **PASS**
- **Evidence**: [`configs/phase0/experiment_matrix.yaml`](configs/phase0/experiment_matrix.yaml)

#### T009: Create baseline experiment specification
- **Purpose**: Define formal configurations for B0–B6 baselines and proposed system.
- **Dependencies**: T006
- **Input**: Baseline definitions from protocol
- **Expected Output**: `protocol/baseline_protocol.md`
- **Files Affected**: `protocol/baseline_protocol.md`
- **Acceptance Criteria**: All 7 baselines and proposed system have complete formal specifications.
- **Status**: **PASS**
- **Evidence**: [`protocol/baseline_protocol.md`](protocol/baseline_protocol.md)

#### T010: Create research protocol
- **Purpose**: Formalize complete scientific methodology.
- **Dependencies**: None
- **Input**: Protocol requirements
- **Expected Output**: `research_protocol.md` and 9 operational sub-protocols
- **Files Affected**: `research_protocol.md`, `protocol/*.md`
- **Acceptance Criteria**: Complete methodology documented with statistical significance and zero-leakage rules.
- **Status**: **PASS**
- **Evidence**: [`research_protocol.md`](research_protocol.md) and [`reports/phase0/protocol_audit.md`](reports/phase0/protocol_audit.md)

#### T011: Create literature tracking system
- **Purpose**: Track relevant papers, contributions, and novelty.
- **Dependencies**: None
- **Input**: Literature Registry Requirements across 3 gaps
- **Expected Output**: `literature_registry.csv`, `literature_matrix.md`, `gap_analysis.md`, `novelty_matrix.md`
- **Files Affected**: `literature/*`
- **Acceptance Criteria**: 20 primary academic papers cataloged; gap analysis and novelty matrix completed.
- **Status**: **PASS**
- **Evidence**: [`literature/literature_registry.csv`](literature/literature_registry.csv) and [`reports/phase0/literature_audit.md`](reports/phase0/literature_audit.md)

#### T012: Validate architecture against PRD
- **Purpose**: Ensure technical architecture design aligns with PRD and goal specifications.
- **Dependencies**: None
- **Input**: `architecture.md`, `prd.md`, `goal.md`
- **Expected Output**: Consistency audit report
- **Files Affected**: `reports/control_file_audit.md`
- **Acceptance Criteria**: Architecture satisfies all PRD and Goal requirements without contradictions.
- **Status**: **PASS**
- **Evidence**: [`reports/control_file_audit.md`](reports/control_file_audit.md) (100% PASS)

---

### Phase 1 Tasks (Repository + Environment + Infrastructure & Ingestion) — ALL COMPLETED

#### T002: Create environment specification
- **Purpose**: Define Python environment, build backend (`pyproject.toml`), and `.env.example`.
- **Dependencies**: Phase 0 Complete
- **Input**: Environment facts (Python 3.14.6, Windows, RTX 3050 6GB, hatchling conventions)
- **Expected Output**: `pyproject.toml`, `.venv`, `.env.example`
- **Files Affected**: `pyproject.toml`, `.env.example`, `.venv/`
- **Acceptance Criteria**: Valid `pyproject.toml` using hatchling build backend.
- **Status**: **PASS**
- **Evidence**: [`pyproject.toml`](pyproject.toml), [`reports/phase1/environment_report.md`](reports/phase1/environment_report.md)

#### T003: Create requirements/dependency files
- **Purpose**: Lock precise versions for reproducibility.
- **Dependencies**: T002
- **Input**: PyTorch, Transformers, PaddleOCR, FAISS, Scikit-learn
- **Expected Output**: Installed packages in `.venv` matching frozen specifications
- **Files Affected**: `pyproject.toml`, `.venv/`
- **Acceptance Criteria**: Pinned dependency environment for Windows x86_64.
- **Status**: **PASS**
- **Evidence**: [`reports/phase1/environment_report.md`](reports/phase1/environment_report.md)

#### T007: Create reproducibility utilities
- **Purpose**: Seed locking and runtime environment metadata capture.
- **Dependencies**: T002
- **Input**: `protocol/reproducibility_protocol.md`
- **Expected Output**: `src/evaluation/reproducibility.py`
- **Files Affected**: `src/evaluation/reproducibility.py`
- **Acceptance Criteria**: `seed_everything()` and environment logging implemented.
- **Status**: **PASS**
- **Evidence**: [`src/evaluation/reproducibility.py`](src/evaluation/reproducibility.py), [`tests/test_reproducibility.py`](tests/test_reproducibility.py) (6/6 tests pass)

#### T008: Create test framework
- **Purpose**: Setup unit testing foundation, pytest markers, and test suites.
- **Dependencies**: T002
- **Input**: pytest conventions
- **Expected Output**: `pytest` configuration in `pyproject.toml` and 6 test suites under `tests/`
- **Files Affected**: `pyproject.toml`, `tests/`
- **Acceptance Criteria**: `pytest` executes successfully across all test suites.
- **Status**: **PASS**
- **Evidence**: 39/39 passing tests in `tests/`, [`reports/phase1/PHASE1_REPORT.md`](reports/phase1/PHASE1_REPORT.md)

#### T013: Implement Document Ingestion module
- **Purpose**: Implement standardized PDF rendering, page extraction, image normalization, and metadata tracking.
- **Dependencies**: T002, T008
- **Input**: `src/ingestion/`
- **Expected Output**: Ingestion pipeline code under `src/ingestion/`
- **Files Affected**: `src/ingestion/coordinates.py`, `src/ingestion/schema.py`, `src/ingestion/metadata.py`, `src/ingestion/pdf.py`, `src/ingestion/adapter.py`
- **Acceptance Criteria**: Successfully parses multi-page PDFs to normalized images with coordinate metadata.
- **Status**: **PASS**
- **Evidence**: [`src/ingestion/`](src/ingestion/), [`reports/phase1/ingestion_validation.md`](reports/phase1/ingestion_validation.md) (19/19 ingestion & coordinate tests pass)

---

### Phase 2 Tasks (Baseline OCR and VLM Pipelines) — ALL COMPLETED

#### T014: Configure Phase 2 baseline models and inference parameters
- **Purpose**: Freeze configuration schemas for models, OCR engines, baselines, and prompts.
- **Dependencies**: Phase 1 Complete
- **Input**: Protocol baseline definitions
- **Expected Output**: `configs/phase2/model_config.yaml`, `ocr_config.yaml`, `baseline_config.yaml`, `inference_config.yaml`
- **Files Affected**: `configs/phase2/*.yaml`, `configs/phase2/prompts/*.txt`
- **Acceptance Criteria**: All models and prompt templates frozen with commit SHAs and hashes.
- **Status**: **PASS**
- **Evidence**: [`configs/phase2/`](configs/phase2/), [`reports/phase2/model_validation.md`](reports/phase2/model_validation.md)

#### T015: Implement OCR module and coordinate normalization bindings
- **Purpose**: Integrate PaddleOCR and Tesseract backends with normalized $[0, 1000]$ coordinate output.
- **Dependencies**: T014
- **Input**: `src/ocr/`
- **Expected Output**: `src/ocr/schema.py`, `base.py`, `paddle.py`, `tesseract.py`
- **Files Affected**: `src/ocr/`
- **Acceptance Criteria**: Normalized bounding boxes and word/line level tokens extracted.
- **Status**: **PASS**
- **Evidence**: [`src/ocr/`](src/ocr/), [`tests/test_ocr.py`](tests/test_ocr.py) (3/3 tests pass)

#### T016: Implement VLM pipeline with prompt hash versioning and image processor
- **Purpose**: Provide traceable VLM inference engine, image transformation recorder, and model loader.
- **Dependencies**: T014
- **Input**: `src/vlm/`
- **Expected Output**: `src/vlm/schema.py`, `loader.py`, `processor.py`, `prompts.py`, `inference.py`
- **Files Affected**: `src/vlm/`
- **Acceptance Criteria**: Traceable image transformations, deterministic prompt hash tracking, timing breakdown.
- **Status**: **PASS**
- **Evidence**: [`src/vlm/`](src/vlm/), [`tests/test_vlm_pipeline.py`](tests/test_vlm_pipeline.py), [`tests/test_latency.py`](tests/test_latency.py)

#### T017: Implement B0, B1, and B2 baseline pipelines
- **Purpose**: Build B0 (OCR-only), B1 (OCR + VLM), and B2 (VLM-only) standard execution pipelines.
- **Dependencies**: T015, T016
- **Input**: `src/baselines/`
- **Expected Output**: `src/baselines/base.py`, `b0_ocr.py`, `b1_ocr_vlm.py`, `b2_vlm.py`
- **Files Affected**: `src/baselines/`
- **Acceptance Criteria**: Common baseline interface produces Section 29 run artifacts.
- **Status**: **PASS**
- **Evidence**: [`src/baselines/`](src/baselines/), [`tests/test_baselines.py`](tests/test_baselines.py) (3/3 tests pass)

#### T018: Implement evaluation metrics and run artifact serializers
- **Purpose**: Exact Match, Token F1, ANLS, CER, WER, and JSON artifact serialization.
- **Dependencies**: T017
- **Input**: `protocol/evaluation_protocol.md`
- **Expected Output**: `src/evaluation/metrics.py`, `src/evaluation/artifacts.py`
- **Files Affected**: `src/evaluation/metrics.py`, `src/evaluation/artifacts.py`
- **Acceptance Criteria**: Metric algorithms and JSON artifact schema match Phase 0 specifications.
- **Status**: **PASS**
- **Evidence**: [`src/evaluation/metrics.py`](src/evaluation/metrics.py), [`tests/test_metrics.py`](tests/test_metrics.py), [`tests/test_inference_artifacts.py`](tests/test_inference_artifacts.py)

#### T019: Execute controlled baseline smoke test and repeatability verification
- **Purpose**: Verify pipeline plumbing, timing, error handling, and 100% repeatability.
- **Dependencies**: T017, T018
- **Input**: Controlled synthetic validation samples
- **Expected Output**: Artifacts under `experiments/phase2/artifacts/` and summary JSONs
- **Files Affected**: `experiments/phase2/`
- **Acceptance Criteria**: E2-SMOKE-B0/B1/B2 pass; E2-REPRO-B0 achieves 100% exact match repeatability.
- **Status**: **PASS**
- **Evidence**: [`scripts/run_phase2_smoke.py`](scripts/run_phase2_smoke.py), [`reports/phase2/smoke_test_report.md`](reports/phase2/smoke_test_report.md)

#### T020: Compile Phase 2 validation and final audit reports
- **Purpose**: Complete documentation suite and Section 58 final audit table.
- **Dependencies**: T014-T019
- **Input**: Test suite execution and smoke experiment results
- **Expected Output**: 6 Phase 2 reports in `reports/phase2/`
- **Files Affected**: `reports/phase2/*.md`
- **Acceptance Criteria**: 100% PASS on all Section 58 audit items.
- **Status**: **PASS**
- **Evidence**: [`reports/phase2/PHASE2_REPORT.md`](reports/phase2/PHASE2_REPORT.md)

---

### Phase 2.5 Tasks (Unlimited-OCR Integration & Scientific Validation) — ALL COMPLETED

#### T021: Investigate and freeze Unlimited-OCR official model specification
- **Purpose**: Identify official repository, architecture, and freeze commit SHA.
- **Dependencies**: Phase 2 Complete
- **Input**: Baidu Unlimited-OCR official releases
- **Expected Output**: `configs/phase2_5/unlimited_ocr_config.yaml`, `reports/phase2_5/model_validation.md`
- **Files Affected**: `configs/phase2_5/unlimited_ocr_config.yaml`, `reports/phase2_5/model_validation.md`
- **Acceptance Criteria**: 40-char SHA commit frozen; architecture details documented.
- **Status**: **PASS**
- **Evidence**: [`configs/phase2_5/unlimited_ocr_config.yaml`](configs/phase2_5/unlimited_ocr_config.yaml), [`reports/phase2_5/model_validation.md`](reports/phase2_5/model_validation.md)

#### T022: Conduct RTX 3050 6GB VRAM feasibility and environment audit
- **Purpose**: Determine memory footprint for 3.3B MoE architecture and verify runtime constraints.
- **Dependencies**: T021
- **Input**: Hardware specs (RTX 3050 6GB, Python 3.14.6)
- **Expected Output**: `reports/phase2_5/environment_validation.md`, `reports/phase2_5/vram_feasibility.md`
- **Files Affected**: `reports/phase2_5/environment_validation.md`, `reports/phase2_5/vram_feasibility.md`
- **Acceptance Criteria**: Feasibility classified per Section 16 (Category B: 4-bit; Category D: CPU).
- **Status**: **PASS**
- **Evidence**: [`reports/phase2_5/vram_feasibility.md`](reports/phase2_5/vram_feasibility.md)

#### T023: Implement Unlimited-OCR architecture, parser, and adapter (B0-U)
- **Purpose**: Build modular integration in `src/baselines/unlimited_ocr/` with standardized `[0, 1000]` schema.
- **Dependencies**: T021, T022
- **Input**: `src/baselines/unlimited_ocr/`
- **Expected Output**: Python modules for schemas, loader, processor, parser, backend, and adapter
- **Files Affected**: `src/baselines/unlimited_ocr/*.py`
- **Acceptance Criteria**: Fully implements common `Baseline` interface; produces `B0-U` results.
- **Status**: **PASS**
- **Evidence**: [`src/baselines/unlimited_ocr/`](src/baselines/unlimited_ocr/), [`tests/test_unlimited_ocr_adapter.py`](tests/test_unlimited_ocr_adapter.py)

#### T024: Validate spatial grounding and coordinate reversibility
- **Purpose**: Verify `<|grounding|>` layout tag parsing, $[0, 1000]$ normalization, and denormalization.
- **Dependencies**: T023
- **Input**: Parser test cases
- **Expected Output**: Grounding validation test suite and report
- **Files Affected**: `tests/test_unlimited_ocr_grounding.py`, `reports/phase2_5/grounding_validation.md`
- **Acceptance Criteria**: Boundary checks pass; no fake bounding box synthesis.
- **Status**: **PASS**
- **Evidence**: [`tests/test_unlimited_ocr_grounding.py`](tests/test_unlimited_ocr_grounding.py), [`reports/phase2_5/grounding_validation.md`](reports/phase2_5/grounding_validation.md)

#### T025: Execute single-page, multi-page, and degradation smoke experiments
- **Purpose**: Verify pipeline stability on multi-page and corrupted document images.
- **Dependencies**: T023, T024
- **Input**: Controlled synthetic document images
- **Expected Output**: Artifacts under `experiments/phase2_5/artifacts/` and summary JSONs
- **Files Affected**: `scripts/run_phase2_5_smoke.py`, `experiments/phase2_5/`
- **Acceptance Criteria**: 100% SUCCESS across all degradation levels; 100% repeatability in `E2_5-REPRO-B0_U`.
- **Status**: **PASS**
- **Evidence**: [`scripts/run_phase2_5_smoke.py`](scripts/run_phase2_smoke.py), [`reports/phase2_5/smoke_test_report.md`](reports/phase2/smoke_test_report.md)

#### T026: Compile baseline comparison matrix and IEEE justification
- **Purpose**: Provide side-by-side comparison across PaddleOCR, Tesseract, Unlimited-OCR, Qwen2.5-VL.
- **Dependencies**: T021-T025
- **Input**: Measured parameters and architectural analysis
- **Expected Output**: `reports/phase2_5/unlimited_ocr_comparison.md`, `reports/phase2_5/ieee_baseline_justification.md`
- **Files Affected**: `reports/phase2_5/unlimited_ocr_comparison.md`, `reports/phase2_5/ieee_baseline_justification.md`
- **Acceptance Criteria**: Complete comparison table; justification grounded in published literature.
- **Status**: **PASS**
- **Evidence**: [`reports/phase2_5/unlimited_ocr_comparison.md`](reports/phase2_5/unlimited_ocr_comparison.md), [`reports/phase2_5/ieee_baseline_justification.md`](reports/phase2_5/ieee_baseline_justification.md)

#### T027: Execute test suite and compile Phase 2.5 final report
- **Purpose**: Run all 69 unit tests and generate Section 59 final audit report.
- **Dependencies**: T021-T026
- **Input**: Full test suite and experiment records
- **Expected Output**: `reports/phase2_5/PHASE2_5_REPORT.md`
- **Files Affected**: `reports/phase2_5/PHASE2_5_REPORT.md`
- **Acceptance Criteria**: 100% PASS on Section 58 Acceptance Audit; all 69 tests pass.
- **Status**: **PASS**
- **Evidence**: [`reports/phase2_5/PHASE2_5_REPORT.md`](reports/phase2_5/PHASE2_5_REPORT.md)

---

### Phase 3 Tasks (Document Quality / Degradation Assessment Module) — ALL COMPLETED

#### T030: Quality Architecture & Pydantic Schemas
- **Purpose**: Define formal data structures and typed schemas for quality features, degradations, and multi-page reports.
- **Dependencies**: Phase 2.5 Complete
- **Input**: Requirements from PRD and Architecture Modules 8 & 9
- **Expected Output**: `src/quality/schema.py`, `src/quality/config.py`
- **Files Affected**: `src/quality/schema.py`, `src/quality/config.py`
- **Acceptance Criteria**: Typed Pydantic models for `FeatureResult`, `DegradationDetection`, `PageQualityAssessment`, `DocumentQualityAssessment`; failure status isolation.
- **Status**: **PASS**
- **Evidence**: [`src/quality/schema.py`](src/quality/schema.py), [`tests/test_quality_schema.py`](tests/test_quality_schema.py)

#### T031: Image Preprocessing & Multi-Color Space Pipeline
- **Purpose**: Build non-destructive image loading, dimension validation, and alpha channel compositing.
- **Dependencies**: T030
- **Input**: `src/quality/preprocessing.py`
- **Expected Output**: Preprocessing pipeline producing RGB and Grayscale representations.
- **Files Affected**: `src/quality/preprocessing.py`
- **Acceptance Criteria**: Alpha channel composited onto white; source images immutable.
- **Status**: **PASS**
- **Evidence**: [`src/quality/preprocessing.py`](src/quality/preprocessing.py), [`tests/test_quality_preprocessing.py`](tests/test_quality_preprocessing.py)

#### T032: Visual Feature Extraction Engine (10 Extractors)
- **Purpose**: Implement pure extractor functions for blur, noise, skew, glare, contrast, resolution, compression, illumination, occlusion, perspective.
- **Dependencies**: T031
- **Input**: `src/quality/*.py`
- **Expected Output**: 10 modular feature extractors with failure isolation
- **Files Affected**: `src/quality/blur.py`, `src/quality/noise.py`, `src/quality/skew.py`, `src/quality/glare.py`, `src/quality/contrast.py`, `src/quality/resolution.py`, `src/quality/compression.py`, `src/quality/illumination.py`, `src/quality/occlusion.py`, `src/quality/perspective.py`, `src/quality/features.py`
- **Acceptance Criteria**: All 10 extractors produce typed `FeatureResult`; errors do not halt independent features.
- **Status**: **PASS**
- **Evidence**: [`src/quality/features.py`](src/quality/features.py), [`tests/test_quality_features.py`](tests/test_quality_features.py)

#### T033: Degradation Classifier & Discrete Severity Mapping
- **Purpose**: Map continuous feature metrics to discrete S0–S4 severity tiers based on frozen thresholds.
- **Dependencies**: T032
- **Input**: `configs/phase3/severity_config.yaml`
- **Expected Output**: `src/quality/detector.py`
- **Files Affected**: `src/quality/detector.py`, `configs/phase3/severity_config.yaml`
- **Acceptance Criteria**: Severity levels match Phase 0 protocol; composite mixed degradation handled.
- **Status**: **PASS**
- **Evidence**: [`src/quality/detector.py`](src/quality/detector.py), [`tests/test_quality_detector.py`](tests/test_quality_detector.py)

#### T034: Multi-Page Document Quality Aggregator
- **Purpose**: Compute descriptive summary statistics across document pages without losing page-level fidelity.
- **Dependencies**: T030, T033
- **Input**: `src/quality/aggregator.py`
- **Expected Output**: Aggregation function identifying worst page and distribution parameters
- **Files Affected**: `src/quality/aggregator.py`, `src/quality/pipeline.py`
- **Acceptance Criteria**: Preserves every page assessment; overall score marked `NOT_DEFINED` per protocol.
- **Status**: **PASS**
- **Evidence**: [`src/quality/aggregator.py`](src/quality/aggregator.py), [`tests/test_quality_pipeline.py`](tests/test_quality_pipeline.py)

#### T035: Synthetic Degradation Validation Framework
- **Purpose**: Implement deterministic synthetic corruptor matching 9 protocol families and validate detector.
- **Dependencies**: T032, T033
- **Input**: `protocol/degradation_protocol.md`
- **Expected Output**: `src/quality/synthetic.py`, `scripts/run_phase3_validation.py`
- **Files Affected**: `src/quality/synthetic.py`, `scripts/run_phase3_validation.py`, `experiments/phase3/`
- **Acceptance Criteria**: 9 families x 5 severities evaluated; monotonic curves analyzed; artifacts saved.
- **Status**: **PASS**
- **Evidence**: [`scripts/run_phase3_validation.py`](scripts/run_phase3_validation.py), [`experiments/phase3/E3-VAL-QUALITY_summary.json`](experiments/phase3/E3-VAL-QUALITY_summary.json)

#### T036: Zero-Leakage & Anti-Fabrication Audit
- **Purpose**: Verify that quality assessment is completely blind to downstream models, ground-truth labels, and metadata.
- **Dependencies**: T035
- **Input**: Interface audit and spoof tests
- **Expected Output**: Dedicated test suite in `tests/test_quality_no_leakage.py`
- **Files Affected**: `tests/test_quality_no_leakage.py`
- **Acceptance Criteria**: 0 forbidden parameters; identical feature outputs under metadata spoofing.
- **Status**: **PASS**
- **Evidence**: [`tests/test_quality_no_leakage.py`](tests/test_quality_no_leakage.py)

#### T037: Determinism & Runtime Benchmarking
- **Purpose**: Benchmark sub-millisecond execution times and verify 100% repeatability.
- **Dependencies**: T035
- **Input**: Repeated run logs and timing records
- **Expected Output**: `reports/phase3/runtime_validation.md`, `reports/phase3/reproducibility_validation.md`
- **Files Affected**: `reports/phase3/runtime_validation.md`, `reports/phase3/reproducibility_validation.md`, `tests/test_quality_determinism.py`
- **Acceptance Criteria**: 100% exact match; mean latency 70.11 ms (< 500 ms limit).
- **Status**: **PASS**
- **Evidence**: [`reports/phase3/runtime_validation.md`](reports/phase3/runtime_validation.md), [`tests/test_quality_determinism.py`](tests/test_quality_determinism.py)

#### T038: Phase 3 Verification & Final Report Generation
- **Purpose**: Run complete pytest suite and generate authoritative 27-section report.
- **Dependencies**: T030-T037
- **Input**: All experimental artifacts and validation logs
- **Expected Output**: `reports/phase3/PHASE3_REPORT.md` and 8 companion reports
- **Files Affected**: `reports/phase3/*.md`
- **Acceptance Criteria**: 106 passed tests (100% pass rate); all 27 report sections complete.
- **Status**: **PASS**
- **Evidence**: [`reports/phase3/PHASE3_REPORT.md`](reports/phase3/PHASE3_REPORT.md)

---

### Phase 4 Tasks (Controlled Degradation Benchmark) — ALL COMPLETED

#### T040: Controlled Degradation Benchmark Architecture & Schemas
- **Purpose**: Define formal data structures and typed schemas for benchmark samples, execution results, and artifacts.
- **Dependencies**: Phase 3 Complete
- **Input**: PRD, Architecture, and Phase 4 Master Prompt
- **Expected Output**: `src/benchmark/schema.py`, `configs/phase4/*.yaml`
- **Files Affected**: `src/benchmark/schema.py`, `configs/phase4/experiment_matrix.yaml`, `benchmark_config.yaml`, `execution_config.yaml`, `evaluation_config.yaml`, `statistics_config.yaml`
- **Acceptance Criteria**: Typed Pydantic models for `BenchmarkSample`, `BenchmarkRunArtifact`, `DegradationCondition`, `ReconciliationRecord`.
- **Status**: **PASS**
- **Evidence**: [`src/benchmark/schema.py`](src/benchmark/schema.py), [`tests/test_phase4_schema.py`](tests/test_phase4_schema.py)

#### T041: Dataset Manifest & Zero-Leakage Split Enforcement
- **Purpose**: Manage standard evaluation corpus, document cryptographic hashing, and enforce partition inheritance.
- **Dependencies**: T040
- **Input**: Standard evaluation documents
- **Expected Output**: `src/benchmark/manifest.py`, `data/manifests/evaluation_manifest.json`, `data/splits/dataset_splits.json`
- **Files Affected**: `src/benchmark/manifest.py`, `data/raw/`, `data/manifests/`, `data/splits/`
- **Acceptance Criteria**: All derived degraded variants strictly inherit `test` split; SHA-256 verified.
- **Status**: **PASS**
- **Evidence**: [`src/benchmark/manifest.py`](src/benchmark/manifest.py), [`tests/test_phase4_split_integrity.py`](tests/test_phase4_split_integrity.py)

#### T042: Deterministic Degradation Runner & Coordinate Mapping
- **Purpose**: Wrap synthetic corruption suite with caching and inverse bounding-box coordinate transformations.
- **Dependencies**: T040, T041
- **Input**: `src/quality/synthetic.py`
- **Expected Output**: `src/benchmark/degradation_runner.py`
- **Files Affected**: `src/benchmark/degradation_runner.py`
- **Acceptance Criteria**: All 9 families x 5 severities supported; bounding boxes preserved in $[0, 1000]$.
- **Status**: **PASS**
- **Evidence**: [`src/benchmark/degradation_runner.py`](src/benchmark/degradation_runner.py), [`tests/test_phase4_degradation.py`](tests/test_phase4_degradation.py)

#### T043: Multi-Baseline Model Runner with Fairness Safeguards
- **Purpose**: Orchestrate B0, B1, B2, B0-U under identical image inputs with zero label leakage or prompt drift.
- **Dependencies**: T040
- **Input**: `src/baselines/`
- **Expected Output**: `src/benchmark/model_runner.py`
- **Files Affected**: `src/benchmark/model_runner.py`
- **Acceptance Criteria**: Prompt versions and hashes frozen; zero degradation metadata passed to prompts.
- **Status**: **PASS**
- **Evidence**: [`src/benchmark/model_runner.py`](src/benchmark/model_runner.py), [`tests/test_phase4_model_fairness.py`](tests/test_phase4_model_fairness.py)

#### T044: Task Metrics & Spatial Grounding Evaluator
- **Purpose**: Compute EM, Token F1, ANLS, CER, WER, and Grounding IoU.
- **Dependencies**: T040
- **Input**: `src/evaluation/metrics.py`, `src/ingestion/coordinates.py`
- **Expected Output**: `src/benchmark/evaluator.py`
- **Files Affected**: `src/benchmark/evaluator.py`
- **Acceptance Criteria**: Correct task-metric binding; IoU $\ge 0.50$ validation.
- **Status**: **PASS**
- **Evidence**: [`src/benchmark/evaluator.py`](src/benchmark/evaluator.py)

#### T045: Observational Quality Feature Capture Integration
- **Purpose**: Capture 10-feature quality vector from Phase 3 on every degraded document without downstream feedback.
- **Dependencies**: T040, Phase 3
- **Input**: `src/quality/pipeline.py`
- **Expected Output**: `src/benchmark/quality_capture.py`
- **Files Affected**: `src/benchmark/quality_capture.py`
- **Acceptance Criteria**: 100% of artifacts contain independent quality vectors; zero model feedback.
- **Status**: **PASS**
- **Evidence**: [`src/benchmark/quality_capture.py`](src/benchmark/quality_capture.py)

#### T046: Clean Baseline Reconciliation with Phase 2/2.5
- **Purpose**: Compare Phase 4 clean baseline ($S_0$) against Phase 2/2.5 reference metrics.
- **Dependencies**: T043, T044
- **Input**: S0 clean evaluation runs
- **Expected Output**: `src/benchmark/reconciliation.py`, `reports/phase4/baseline_reconciliation.md`
- **Files Affected**: `src/benchmark/reconciliation.py`, `reports/phase4/baseline_reconciliation.md`
- **Acceptance Criteria**: Difference $\le \pm 0.05$; 100% PASS across B0, B1, B2, B0-U.
- **Status**: **PASS**
- **Evidence**: [`reports/phase4/baseline_reconciliation.md`](reports/phase4/baseline_reconciliation.md), [`tests/test_phase4_reconciliation.py`](tests/test_phase4_reconciliation.py)

#### T047: Paired Bootstrap Statistical Framework & Effect Sizes
- **Purpose**: Implement paired bootstrap ($B=10,000$), Cliff's delta, Cohen's d, and Hypothesis H1 trend testing.
- **Dependencies**: T040
- **Input**: Protocol statistical requirements
- **Expected Output**: `src/benchmark/statistics.py`
- **Files Affected**: `src/benchmark/statistics.py`
- **Acceptance Criteria**: $B=10,000$ iterations; empirical 95% CIs; Cliff's delta thresholds.
- **Status**: **PASS**
- **Evidence**: [`src/benchmark/statistics.py`](src/benchmark/statistics.py), [`tests/test_phase4_statistics.py`](tests/test_phase4_statistics.py)

#### T048: Benchmark Matrix Execution & Master Phase 4 Reporting
- **Purpose**: Execute all 3,600 conditions, tabulate Tables A-E, and generate comprehensive reports.
- **Dependencies**: T040-T047
- **Input**: Execution pipeline
- **Expected Output**: `scripts/run_phase4_benchmark.py`, `experiments/phase4/`, `reports/phase4/*.md`
- **Files Affected**: `scripts/run_phase4_benchmark.py`, `reports/phase4/PHASE4_REPORT.md` and 7 companion reports
- **Acceptance Criteria**: 3,600 run artifacts saved; all 32 report sections complete; 126 tests passing.
- **Status**: **PASS**
- **Evidence**: [`reports/phase4/PHASE4_REPORT.md`](reports/phase4/PHASE4_REPORT.md), [`experiments/phase4/index.json`](experiments/phase4/index.json)

---

### Phase 5 Tasks (Adaptive Routing & Uncertainty-Aware Model Selection) — ALL COMPLETED

#### T050: Adaptive Routing Schemas, Pydantic Models & YAML Configurations
- **Purpose**: Define formal data structures and typed schemas for routing decisions, traces, costs, and configs.
- **Dependencies**: Phase 4 Complete
- **Input**: `protocol/uncertainty_protocol.md`, Phase 5 prompt
- **Expected Output**: `src/routing/schema.py`, `configs/phase5/*.yaml`
- **Files Affected**: `src/routing/schema.py`, `configs/phase5/` (7 YAML config files)
- **Acceptance Criteria**: Typed Pydantic models with strict validation; 6 passed schema tests.
- **Status**: **PASS**
- **Evidence**: [`src/routing/schema.py`](src/routing/schema.py), [`tests/test_phase5_schema.py`](tests/test_phase5_schema.py)

#### T051: Quality Feature Adapter & Deterministic Rule Engine
- **Purpose**: Map Phase 3 visual quality features to model selections via configuration-driven rules.
- **Dependencies**: T050
- **Input**: `src/quality/schema.py`, `configs/phase5/router_rules.yaml`
- **Expected Output**: `src/routing/feature_adapter.py`, `src/routing/rule_engine.py`
- **Files Affected**: `src/routing/feature_adapter.py`, `src/routing/rule_engine.py`
- **Acceptance Criteria**: 10-feature extraction normalized in $[0, 1]$; zero label leakage; 7 passed rule tests.
- **Status**: **PASS**
- **Evidence**: [`src/routing/rule_engine.py`](src/routing/rule_engine.py), [`tests/test_phase5_rules.py`](tests/test_phase5_rules.py)

#### T052: Multi-Signal Uncertainty Adapter & Post-Hoc Calibrator
- **Purpose**: Assemble 6-signal uncertainty vector and fit calibrators strictly on validation partition.
- **Dependencies**: T050
- **Input**: `protocol/uncertainty_protocol.md`
- **Expected Output**: `src/routing/uncertainty.py`, `src/routing/calibration.py`
- **Files Affected**: `src/routing/uncertainty.py`, `src/routing/calibration.py`
- **Acceptance Criteria**: Platt/logistic calibration; ECE and Brier score evaluation; validation split enforcement.
- **Status**: **PASS**
- **Evidence**: [`src/routing/calibration.py`](src/routing/calibration.py), [`tests/test_phase5_calibration.py`](tests/test_phase5_calibration.py)

#### T053: Lightweight Learned Router & Policy Manager (R0–R5)
- **Purpose**: Implement policy dispatcher for Oracle (R0), Fixed (R1), Rule-based (R2), Uncertainty (R3), Learned (R4), and Composite (R5).
- **Dependencies**: T051, T052
- **Input**: Model execution outcomes
- **Expected Output**: `src/routing/learned_router.py`, `src/routing/policy.py`
- **Files Affected**: `src/routing/learned_router.py`, `src/routing/policy.py`
- **Acceptance Criteria**: Dispatch across all policies; oracle strictly marked non-deployable; 7 passed router tests.
- **Status**: **PASS**
- **Evidence**: [`src/routing/policy.py`](src/routing/policy.py), [`tests/test_phase5_router.py`](tests/test_phase5_router.py)

#### T054: Structural Fallback & Engineering Cost Model
- **Purpose**: Inspect model output structure and account for latency and relative compute expenditures.
- **Dependencies**: T050
- **Input**: `configs/phase5/cost_config.yaml`
- **Expected Output**: `src/routing/fallback.py`, `src/routing/cost.py`
- **Files Affected**: `src/routing/fallback.py`, `src/routing/cost.py`
- **Acceptance Criteria**: Fallback on malformed/empty outputs; cost function $J$ evaluation; 7 passed fallback/cost tests.
- **Status**: **PASS**
- **Evidence**: [`src/routing/fallback.py`](src/routing/fallback.py), [`tests/test_phase5_fallback.py`](tests/test_phase5_fallback.py)

#### T055: Decision Tracing & Zero-Leakage Static Code Audit
- **Purpose**: Log immutable decision traces and audit routing source files for forbidden ground-truth identifiers.
- **Dependencies**: T050
- **Input**: Routing codebase
- **Expected Output**: `src/routing/decision_trace.py`, `src/routing/audit.py`
- **Files Affected**: `src/routing/decision_trace.py`, `src/routing/audit.py`
- **Acceptance Criteria**: Static AST audit passes with 0 violations across 12 routing modules.
- **Status**: **PASS**
- **Evidence**: [`reports/phase5/zero_leakage_audit.md`](reports/phase5/zero_leakage_audit.md), [`tests/test_phase5_no_leakage.py`](tests/test_phase5_no_leakage.py)

#### T056: End-to-End Routing Pipeline & CLI Runners
- **Purpose**: Orchestrate feature extraction, policy selection, model invocation, and artifact serialization.
- **Dependencies**: T050-T055
- **Input**: Complete routing package
- **Expected Output**: `src/routing/router.py`, `src/routing/pipeline.py`, `scripts/run_phase5_*.py`
- **Files Affected**: `src/routing/router.py`, `src/routing/pipeline.py`, `scripts/run_phase5_smoke.py`, `scripts/run_phase5_validation.py`, `scripts/run_phase5_benchmark.py`
- **Acceptance Criteria**: 163 pytest tests pass; smoke test and validation test pass.
- **Status**: **PASS**
- **Evidence**: [`scripts/run_phase5_smoke.py`](scripts/run_phase5_smoke.py), [`scripts/run_phase5_validation.py`](scripts/run_phase5_validation.py)

#### T057: Controlled Routing Benchmark Execution & Statistical Hypotheses
- **Purpose**: Execute 4,500 evaluations across 900 benchmark conditions and test Hypothesis H2 via paired bootstrap.
- **Dependencies**: T056
- **Input**: Evaluation corpus and degradation runner
- **Expected Output**: `experiments/phase5/summaries/E5_ROUTING_summary.json`, `experiments/phase5/index.json`
- **Files Affected**: `experiments/phase5/`
- **Acceptance Criteria**: $B=10,000$ paired bootstrap computed; empirical 95% CIs; Cliff's $\delta$ computed; honest H2 evaluation.
- **Status**: **PASS**
- **Evidence**: [`experiments/phase5/summaries/E5_ROUTING_summary.json`](experiments/phase5/summaries/E5_ROUTING_summary.json), [`reports/phase5/statistical_analysis.md`](reports/phase5/statistical_analysis.md)

#### T058: Master Phase 5 Research Documentation
- **Purpose**: Author all 12 comprehensive Phase 5 research reports.
- **Dependencies**: T050-T057
- **Input**: Experimental results and audit evidence
- **Expected Output**: `reports/phase5/PHASE5_REPORT.md` (30 complete sections) and 11 companion reports
- **Files Affected**: `reports/phase5/*.md`
- **Acceptance Criteria**: All 12 reports written; anti-fabrication verified; governance synchronized.
- **Status**: **PASS**
- **Evidence**: [`reports/phase5/PHASE5_REPORT.md`](reports/phase5/PHASE5_REPORT.md)

---

### Phase 5.1 Tasks (Scientific Correction & Revalidation) — ALL COMPLETED

#### T059: Trace Schema Expansion & Cryptographic Collision Protection
- **Purpose**: Resolve Audit Defect P1-01 by supporting condition provenance fields and preventing silent trace overwrites.
- **Dependencies**: Phase 5 Scientific Audit
- **Input**: Audit findings on trace loss
- **Expected Output**: Updated `src/routing/schema.py` and `src/routing/decision_trace.py` with hash comparison.
- **Files Affected**: `src/routing/schema.py`, `src/routing/decision_trace.py`
- **Acceptance Criteria**: Unique run ID generation; FileExistsError on conflicting overwrite; 100% collision tests pass.
- **Status**: **PASS**
- **Evidence**: [`tests/test_phase5_1_trace_collision.py`](tests/test_phase5_1_trace_collision.py), [`reports/phase5_1/trace_cardinality.md`](reports/phase5_1/trace_cardinality.md)

#### T060: Zero-Leakage Observable Uncertainty Assembly
- **Purpose**: Resolve Audit Defect P1-02 by eliminating condition metadata from inference-time uncertainty vectors.
- **Dependencies**: T059
- **Input**: Observable visual quality features from Phase 3
- **Expected Output**: `assemble_from_quality_features()` in `src/routing/uncertainty.py`
- **Files Affected**: `src/routing/uncertainty.py`, `src/routing/pipeline.py`
- **Acceptance Criteria**: Derives purely from visual features; zero access to condition metadata; static AST audit passes.
- **Status**: **PASS**
- **Evidence**: [`tests/test_phase5_1_uncertainty_clean.py`](tests/test_phase5_1_uncertainty_clean.py), [`reports/phase5_1/uncertainty_information_boundary.md`](reports/phase5_1/uncertainty_information_boundary.md)

#### T061: Learned Router Model Serialization & Runtime Deployment
- **Purpose**: Resolve Audit Defect P1-03 by serializing fitted scikit-learn models and deploying them at benchmark runtime.
- **Dependencies**: T059
- **Input**: Training on validation partition
- **Expected Output**: `save()` / `load()` methods in `src/routing/learned_router.py`, `learned_router.joblib` artifact.
- **Files Affected**: `src/routing/learned_router.py`, `src/routing/policy.py`, `scripts/run_phase5_1_validation.py`
- **Acceptance Criteria**: Model serialized to disk; loaded during policy dispatch; dynamic non-degenerate prediction distribution.
- **Status**: **PASS**
- **Evidence**: [`experiments/phase5_1/models/learned_router.joblib`](experiments/phase5_1/models/learned_router.joblib), [`reports/phase5_1/learned_router_serialization.md`](reports/phase5_1/learned_router_serialization.md)

#### T062: Phase 5.1 Configuration Master & Preservation
- **Purpose**: Create isolated Phase 5.1 configurations preserving Phase 5 baseline immutability.
- **Dependencies**: T059-T061
- **Input**: Phase 5 configurations
- **Expected Output**: 7 configuration files under `configs/phase5_1/`
- **Files Affected**: `configs/phase5_1/*.yaml`
- **Acceptance Criteria**: Candidate models match B0, B1, B2, B0-U; relative cost weights calibrated; tests pass.
- **Status**: **PASS**
- **Evidence**: [`tests/test_phase5_1_config_preservation.py`](tests/test_phase5_1_config_preservation.py)

#### T063: Phase 5.1 Test Suite Implementation & Verification
- **Purpose**: Develop 10 new rigorous test suites verifying trace identity, collision detection, clean uncertainty, serialization, and regression.
- **Dependencies**: T059-T062
- **Input**: Test specifications
- **Expected Output**: 10 new test files under `tests/test_phase5_1_*.py`
- **Files Affected**: `tests/test_phase5_1_*.py`
- **Acceptance Criteria**: All 178 tests pass (100% pass rate, 0 failures, 0 regressions).
- **Status**: **PASS**
- **Evidence**: Pytest test run output (178 passed in 19.71s)

#### T064: Phase 5.1 Controlled Routing Benchmark Execution
- **Purpose**: Execute full 900-condition benchmark across 5 policies, generating 4,500 distinct traces and evaluating H2.
- **Dependencies**: T063
- **Input**: Benchmark runner and evaluation corpus
- **Expected Output**: 4,500 trace artifacts, `experiments/phase5_1/summaries/E5_1_ROUTING_summary.json`
- **Files Affected**: `experiments/phase5_1/`
- **Acceptance Criteria**: 4,500 unique on-disk traces; B=10,000 paired bootstrap; honest evaluation of H2 (NOT_SUPPORTED).
- **Status**: **PASS**
- **Evidence**: [`experiments/phase5_1/summaries/E5_1_ROUTING_summary.json`](experiments/phase5_1/summaries/E5_1_ROUTING_summary.json)

#### T065: Phase 5.1 Ablation Study Execution
- **Purpose**: Generate comprehensive ablation analysis covering feature groups, fallbacks, and learned routing.
- **Dependencies**: T064
- **Input**: Master benchmark summary
- **Expected Output**: `experiments/phase5_1/ablations/ablation_summary.json`
- **Files Affected**: `experiments/phase5_1/ablations/ablation_summary.json`
- **Acceptance Criteria**: Covers A1 through A8; documents 16.6% compute reduction under R4.
- **Status**: **PASS**
- **Evidence**: [`experiments/phase5_1/ablations/ablation_summary.json`](experiments/phase5_1/ablations/ablation_summary.json)

#### T066: Master Phase 5.1 Research Documentation
- **Purpose**: Author all comprehensive Phase 5.1 scientific reports.
- **Dependencies**: T059-T065
- **Input**: Benchmark data, ablation outputs, audit logs
- **Expected Output**: `reports/phase5_1/PHASE5_1_REPORT.md` (34 sections) and 7 companion reports
- **Files Affected**: `reports/phase5_1/*.md`
- **Acceptance Criteria**: Complete 34-section report; before/after comparisons; zero result fabrication.
- **Status**: **PASS**
- **Evidence**: [`reports/phase5_1/PHASE5_1_REPORT.md`](reports/phase5_1/PHASE5_1_REPORT.md)

