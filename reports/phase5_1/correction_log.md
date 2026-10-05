# Phase 5.1 Scientific Correction Log

**Project**: Vision-Language Models for Intelligent Document Processing under Real-World Visual Degradation  
**Phase**: 5.1 — Scientific Correction & Revalidation  
**Date**: 2026-10-05  
**Author**: Antigravity Pair-Programming Agent  

---

## 1. Summary of Changes

Phase 5.1 implements precision modifications addressing all findings from the formal scientific audit of Phase 5. Historical artifacts in `experiments/phase5/` remain strictly immutable. All corrected outputs are organized under `experiments/phase5_1/`, `configs/phase5_1/`, and `reports/phase5_1/`.

---

## 2. Itemized Code Modifications

### 2.1 Trace Schema Expansion
- **File**: `src/routing/schema.py`
- **Changes**:
  - Added condition provenance fields to `RoutingTrace`: `phase`, `dataset`, `sample_id`, `degradation_family`, `severity`, `seed`, `policy`, `configuration_hash`, `model_revision`, `input_hash`, `quality_feature_hash`, `uncertainty_vector`, `fallback_status`, `latency_ms`, `compute_cost`, `artifact_hash`.
  - Added optional provenance fields to `RoutingRunArtifact`: `phase`, `sample_id`, `degradation_family`, `severity`.
- **Rationale**: Enables full condition-level auditing without data loss.

### 2.2 Decision Trace Persistence & Collision Protection
- **File**: `src/routing/decision_trace.py`
- **Changes**:
  - Implemented cryptographic hash checking in `RoutingDecisionTracer.save_trace()`.
  - Added explicit `FileExistsError` raising when an existing trace file with differing condition/decision content is targeted.
  - Enabled configurable `trace_dir`.
- **Rationale**: Resolves Defect P1-01 and guarantees that silent trace overwrite is impossible.

### 2.3 Observable Uncertainty Assembly
- **File**: `src/routing/uncertainty.py`
- **Changes**:
  - Implemented `assemble_from_quality_features(quality_features, overall_quality)`.
  - Made constructor configuration optional with verified defaults.
  - Ensured that uncertainty signals depend exclusively on visual image metrics.
- **Rationale**: Resolves Defect P1-02 by purging benchmark metadata (`condition.severity`, `condition.family`) from uncertainty assembly.

### 2.4 Learned Router Serialization & Model Persistence
- **File**: `src/routing/learned_router.py`
- **Changes**:
  - Implemented `save(path)` using `joblib.dump`, saving model, hyperparameters, feature order (`FEATURE_NAMES`), and provenance metadata.
  - Implemented `load(path)` and class factory `from_file(path)`.
  - Added validation check preventing saving of unfitted models.
- **Rationale**: Resolves Defect P1-03 by bridging the offline training script with inference deployment.

### 2.5 Policy Manager Model Loading
- **File**: `src/routing/policy.py`
- **Changes**:
  - Updated `RoutingPolicyManager.from_configs()` to read `learned_router_model_path` and load `LearnedQualityRouter.from_file(path)` if present on disk.
- **Rationale**: Ensures `R4_LEARNED` runs a fitted model rather than defaulting to `B2`.

### 2.6 Router Provenance Forwarding
- **File**: `src/routing/router.py`
- **Changes**:
  - Updated `AdaptiveRouter.route()` to accept condition provenance kwargs (`phase`, `sample_id`, `degradation_family`, `severity`, `seed`, `configuration_hash`) and pass them to `RoutingDecisionTracer.record_trace()`.
  - Made `create_default()` accept config paths and `trace_dir`.
- **Rationale**: Full traceability across the orchestrator boundary.

### 2.7 Pipeline Unique Run Identity & Clean Assembly
- **File**: `src/routing/pipeline.py`
- **Changes**:
  - Updated `process_sample()` to format `run_id` as:
    `run_P5_1_{dataset}_{policy}_{sample_id}_{family}_sev{severity}_s{seed}`.
  - Replaced synthetic uncertainty derivation with `assemble_from_quality_features()`.
  - Populated all provenance parameters into trace and run artifact records.
  - Supported configurable `output_dir` and `phase`.
- **Rationale**: Corrects both P1-01 (overwriting) and P1-02 (metadata leakage).

### 2.8 Enhanced Zero-Leakage AST Auditor
- **File**: `src/routing/audit.py`
- **Changes**:
  - Added attribute checking (`ast.Attribute`) to detect forbidden attribute references (`node.attr in self.forbidden_terms`).
  - Added extended forbidden identifiers: `true_severity`, `true_family`.
- **Rationale**: Enforces static compile-time verification of zero leakage.

---

## 3. Test Suites Created

1. `tests/test_phase5_1_trace_identity.py`: Verified unique run IDs across all degradation conditions.
2. `tests/test_phase5_1_trace_collision.py`: Verified `FileExistsError` on conflicting trace overwrite.
3. `tests/test_phase5_1_uncertainty_clean.py`: Verified pure visual uncertainty assembly without condition metadata.
4. `tests/test_phase5_1_learned_router_serialization.py`: Verified `joblib` save, reload, and prediction parity.
5. `tests/test_phase5_1_learned_router_deployment.py`: Verified R4 loads fitted model and predicts dynamically.
6. `tests/test_phase5_1_no_leakage_audit.py`: Verified static AST audit passes on all routing modules.
7. `tests/test_phase5_1_config_preservation.py`: Verified all 7 Phase 5.1 configuration files.
8. `tests/test_phase5_1_cardinality.py`: Verified trace cardinality preservation without file loss.
9. `tests/test_phase5_1_cost_accounting.py`: Verified Relative Architectural Compute Cost model accounting.
10. `tests/test_phase5_1_regression.py`: Verified mathematical regret calculation and bootstrap testing.

All 178 tests passed.
