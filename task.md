# VLM-IDP Active Execution Queue

CURRENT PHASE: PHASE 0
CURRENT OBJECTIVE: Freeze research protocol and establish reproducible project foundation.
TASK STATUS: IN_PROGRESS

---

### T001: Create repository structure
- **Purpose**: Initialize base directories for the research project.
- **Dependencies**: None
- **Input**: User specifications
- **Expected Output**: Standard directory layout (e.g., configs/, src/, docs/)
- **Files Affected**: Directory structure
- **Acceptance Criteria**: Directories exist according to conventions.
- **Status**: IN_PROGRESS
- **Evidence**: Directories created

### T002: Create environment specification
- **Purpose**: Define Python environment and build backend.
- **Dependencies**: T001
- **Input**: Environment facts (Python 3.14.6, Windows)
- **Expected Output**: pyproject.toml and .venv setup instructions
- **Files Affected**: pyproject.toml
- **Acceptance Criteria**: Valid pyproject.toml using hatchling.
- **Status**: NOT_STARTED
- **Evidence**: None

### T003: Create requirements/dependency files
- **Purpose**: Lock precise versions for reproducibility.
- **Dependencies**: T002
- **Input**: Model and library requirements
- **Expected Output**: requirements.txt or locked dependencies
- **Files Affected**: pyproject.toml / requirements.txt
- **Acceptance Criteria**: Key packages (torch, transformers) listed.
- **Status**: NOT_STARTED
- **Evidence**: None

### T004: Create dataset manifest system
- **Purpose**: Define how datasets are tracked and downloaded.
- **Dependencies**: None
- **Input**: Selected Datasets list
- **Expected Output**: datasets.yaml or similar manifest
- **Files Affected**: configs/datasets.yaml
- **Acceptance Criteria**: Schema for dataset versions and splits defined.
- **Status**: NOT_STARTED
- **Evidence**: None

### T005: Create model registry
- **Purpose**: Track model versions and configurations.
- **Dependencies**: None
- **Input**: Selected Models list
- **Expected Output**: models.yaml manifest
- **Files Affected**: configs/models.yaml
- **Acceptance Criteria**: Primary and secondary models documented with loading configs.
- **Status**: NOT_STARTED
- **Evidence**: None

### T006: Create experiment configuration schema
- **Purpose**: Standardize how experiments are configured.
- **Dependencies**: T004, T005
- **Input**: Research protocol parameters
- **Expected Output**: Base config template
- **Files Affected**: configs/base_experiment.yaml
- **Acceptance Criteria**: Complete schema covering models, data, metrics, and parameters.
- **Status**: NOT_STARTED
- **Evidence**: None

### T007: Create reproducibility utilities
- **Purpose**: Ensure scripts for fixing seeds and logging environments.
- **Dependencies**: T002
- **Input**: Reproducibility requirements
- **Expected Output**: utils/reproducibility.py
- **Files Affected**: src/utils/reproducibility.py
- **Acceptance Criteria**: Function to set all random seeds and log env info.
- **Status**: NOT_STARTED
- **Evidence**: None

### T008: Create test framework
- **Purpose**: Setup unit testing foundation.
- **Dependencies**: T002
- **Input**: pytest conventions
- **Expected Output**: pytest configuration and initial tests
- **Files Affected**: pytest.ini, tests/
- **Acceptance Criteria**: pytest runs successfully.
- **Status**: NOT_STARTED
- **Evidence**: None

### T009: Create baseline experiment specification
- **Purpose**: Define configurations for B0-B6 baselines.
- **Dependencies**: T006
- **Input**: Baseline definitions from protocol
- **Expected Output**: Baseline config files
- **Files Affected**: configs/baselines/
- **Acceptance Criteria**: All 7 baselines have documented configurations.
- **Status**: NOT_STARTED
- **Evidence**: None

### T010: Create research protocol
- **Purpose**: Formalize methodology.
- **Dependencies**: None
- **Input**: Protocol requirements
- **Expected Output**: research_protocol.md
- **Files Affected**: research_protocol.md
- **Acceptance Criteria**: Complete methodology documented.
- **Status**: IN_PROGRESS
- **Evidence**: Markdown file created

### T011: Create literature tracking system
- **Purpose**: Track relevant papers and contributions.
- **Dependencies**: None
- **Input**: Literature Registry Requirements
- **Expected Output**: literature.md or similar database
- **Files Affected**: docs/literature.md
- **Acceptance Criteria**: Schema for literature tracking established.
- **Status**: NOT_STARTED
- **Evidence**: None

### T012: Validate architecture against PRD
- **Purpose**: Ensure architecture design meets project goals.
- **Dependencies**: None
- **Input**: architecture.md and goal.md
- **Expected Output**: Validation report or updated architecture
- **Files Affected**: architecture.md
- **Acceptance Criteria**: Architecture aligns with memory and goals.
- **Status**: NOT_STARTED
- **Evidence**: None
