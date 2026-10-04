# VLM-IDP Active Execution Queue

CURRENT PHASE: PHASE 2 — Baseline OCR and VLM Pipelines (COMPLETED)
CURRENT OBJECTIVE: Phase 2 baselines established and validated. Awaiting user authorization to begin Phase 3.
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
