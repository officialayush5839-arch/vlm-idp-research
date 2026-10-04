# VLM-IDP Active Execution Queue

CURRENT PHASE: PHASE 1 — Repository + Environment + Infrastructure & Ingestion (COMPLETED)
CURRENT OBJECTIVE: Phase 1 complete. Awaiting user authorization to begin Phase 2.
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
