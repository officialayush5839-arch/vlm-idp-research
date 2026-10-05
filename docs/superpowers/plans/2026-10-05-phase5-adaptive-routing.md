# Phase 5 — Adaptive Quality-Aware Routing Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement, validate, and benchmark an inference-time adaptive quality-aware and uncertainty-aware model router that selects among B0, B1, B2, and B0-U under real-world visual degradation without test-set leakage or result fabrication.

**Architecture:** An independent modular routing system in `src/routing/` containing schemas, feature adapters, a deterministic rule engine, a calibrated uncertainty estimator, lightweight learned routers, cost models, structural fallback handlers, decision tracers, and anti-leakage audit validators, coordinated by `AdaptiveRoutingPipeline`.

**Tech Stack:** Python 3.14, Pydantic v2, scikit-learn, NumPy, SciPy, PyYAML, Pytest.

**Spec:** Phase 5 Master Implementation Prompt; `protocol/uncertainty_protocol.md`; `protocol/evaluation_protocol.md`; `protocol/statistical_protocol.md`.

## Global Constraints
- Zero data leakage: No ground-truth answers, benchmark annotations, test partition scores, or synthetic degradation severity labels ($S_0$–$S_4$) may ever be passed to the router.
- Configuration-driven parameters: All routing thresholds, weights, and calibration boundaries must live in `configs/phase5/*.yaml`, never hardcoded in Python.
- Anti-fabrication integrity: Honest hardware reporting (`CUDA=NOT_AVAILABLE`, `GPU_VRAM=NOT_AVAILABLE`). No synthetic results claimed as real measurements.
- Immutability of prior phases: Do not modify Phase 0–4 protocols, baseline definitions, or historical artifacts.
- Partition strictness: Router training, threshold selection, and post-hoc calibration MUST occur only on Train/Validation splits; Test split evaluated strictly once.

## Review Focus
1. Test leakage: Router reading ground truth or test partition performance before routing decisions.
2. Synthetic label leakage: Router branching on `condition.severity` or `condition.family` instead of measured visual features.
3. Missing or zero-variance feature handling: Graceful handling of missing features, NaN, or constant vectors in the quality vector.
4. Structural fallback: Robust fallback only when candidate outputs fail structural schema validation (never based on semantic evaluation metrics).
5. Post-hoc calibration isolation: Logistic/Isotonic calibration fitted strictly on validation split data.

---

### Task 1: Phase 5 Configurations & Schemas
**Files:**
- Create: `configs/phase5/routing_config.yaml`
- Create: `configs/phase5/router_rules.yaml`
- Create: `configs/phase5/uncertainty_config.yaml`
- Create: `configs/phase5/calibration_config.yaml`
- Create: `configs/phase5/cost_config.yaml`
- Create: `configs/phase5/experiment_matrix.yaml`
- Create: `configs/phase5/evaluation_config.yaml`
- Create: `src/routing/schema.py`
- Test: `tests/test_phase5_schema.py`

**Interfaces:**
- Produces: `RoutingPolicyType`, `RoutingDecision`, `RoutingTrace`, `UncertaintyVector`, `RoutingCost`, `RoutingRunArtifact`.

- [ ] **Step 1: Write failing test in `tests/test_phase5_schema.py`**
  Verify instantiation and validation of `RoutingDecision`, `UncertaintyVector`, and `RoutingRunArtifact`.
- [ ] **Step 2: Run test to verify it fails**
  Run: `pytest tests/test_phase5_schema.py -v` (Expected: FAIL).
- [ ] **Step 3: Create YAML configs in `configs/phase5/`**
  Define explicit thresholds, cost weights ($\lambda_{\text{latency}}, \lambda_{\text{compute}}$), calibration parameters, and experiment matrices.
- [ ] **Step 4: Implement schemas in `src/routing/schema.py`**
  Use Pydantic v2 with strict validation and provenance tracking.
- [ ] **Step 5: Run test to verify it passes**
  Run: `pytest tests/test_phase5_schema.py -v` (Expected: PASS).

---

### Task 2: Quality & Degradation Feature Adapter
**Files:**
- Create: `src/routing/feature_adapter.py`
- Test: `tests/test_phase5_rules.py`

**Interfaces:**
- Consumes: `PageQualityAssessment` from `src/quality/schema.py`.
- Produces: `extract_routing_features(assessment) -> Dict[str, float]`, normalized feature vectors for 10 quality dimensions.

- [ ] **Step 1: Write failing test in `tests/test_phase5_rules.py` for feature adapter**
  Verify that `extract_routing_features` handles full, partial, or missing features and normalizes to $[0.0, 1.0]$.
- [ ] **Step 2: Run test to verify failure**
  Run: `pytest tests/test_phase5_rules.py -k test_feature_adapter -v` (Expected: FAIL).
- [ ] **Step 3: Implement `src/routing/feature_adapter.py`**
  Extract the 10 quality features (blur, noise, skew, glare, contrast, resolution, compression, illumination, occlusion, perspective) without exposing synthetic ground-truth metadata.
- [ ] **Step 4: Run test to verify pass**
  Run: `pytest tests/test_phase5_rules.py -k test_feature_adapter -v` (Expected: PASS).

---

### Task 3: Deterministic Rule-Based Quality Routing Engine
**Files:**
- Create: `src/routing/rule_engine.py`
- Test: `tests/test_phase5_rules.py`

**Interfaces:**
- Consumes: Normalized quality features and `configs/phase5/router_rules.yaml`.
- Produces: `RuleEngine.evaluate(features: Dict[str, float]) -> Tuple[str, str, float]` (selected model, decision rule reason, confidence).

- [ ] **Step 1: Write failing tests in `tests/test_phase5_rules.py` for rule engine**
  Test clean document route (B0/B1), severe geometric route (B2), severe multimodal degradation route (B0-U/B2).
- [ ] **Step 2: Run test to verify failure**
  Run: `pytest tests/test_phase5_rules.py -k test_rule_evaluation -v` (Expected: FAIL).
- [ ] **Step 3: Implement `src/routing/rule_engine.py`**
  Configurable rule evaluation matching Phase 4 empirical findings without hardcoded magic numbers.
- [ ] **Step 4: Run test to verify pass**
  Run: `pytest tests/test_phase5_rules.py -k test_rule_evaluation -v` (Expected: PASS).

---

### Task 4: Multi-Signal Uncertainty Adapter & Post-Hoc Calibrator
**Files:**
- Create: `src/routing/uncertainty.py`
- Create: `src/routing/calibration.py`
- Test: `tests/test_phase5_calibration.py`

**Interfaces:**
- Consumes: Protocol 6-signal uncertainty definition $[u_{\text{vlm}}, u_{\text{ocr}}, u_{\text{ret}}, u_{\text{gnd}}, u_{\text{qual}}, u_{\text{agr}}]$.
- Produces: `UncertaintyAdapter`, `PostHocCalibrator` (Platt/Logistic, Isotonic, Small MLP), calibrated confidence $c \in [0, 1]$.

- [ ] **Step 1: Write failing test in `tests/test_phase5_calibration.py`**
  Test uncertainty vector extraction, logistic calibration fitting on train/val, and prediction of calibrated confidence.
- [ ] **Step 2: Run test to verify failure**
  Run: `pytest tests/test_phase5_calibration.py -v` (Expected: FAIL).
- [ ] **Step 3: Implement `src/routing/uncertainty.py` and `src/routing/calibration.py`**
  Fit calibrator strictly on validation data; calculate ECE, Brier score, and output status (`VERIFIED`, `UNCERTAIN`, `REVIEW_REQUIRED`).
- [ ] **Step 4: Run test to verify pass**
  Run: `pytest tests/test_phase5_calibration.py -v` (Expected: PASS).

---

### Task 5: Lightweight Learned Router & Policy Manager
**Files:**
- Create: `src/routing/learned_router.py`
- Create: `src/routing/policy.py`
- Test: `tests/test_phase5_router.py`

**Interfaces:**
- Consumes: Feature vectors and train partition model rankings.
- Produces: `LearnedRouter` (LogisticRegression / RandomForestClassifier via scikit-learn), `RoutingPolicyManager` supporting policies:
  - R0: Oracle upper bound (non-deployable)
  - R1: Fixed-best baseline (B2)
  - R2: Rule-based quality router
  - R3: Uncertainty-aware router
  - R4: Learned quality router
  - R5: Quality + Uncertainty composite router

- [ ] **Step 1: Write failing test in `tests/test_phase5_router.py`**
  Verify policy manager dispatching for all R0–R5 policies.
- [ ] **Step 2: Run test to verify failure**
  Run: `pytest tests/test_phase5_router.py -v` (Expected: FAIL).
- [ ] **Step 3: Implement `src/routing/learned_router.py` and `src/routing/policy.py`**
  Ensure train/val fitting only, and mark R0 strictly as non-deployable.
- [ ] **Step 4: Run test to verify pass**
  Run: `pytest tests/test_phase5_router.py -v` (Expected: PASS).

---

### Task 6: Structural Fallback & Routing Cost Model
**Files:**
- Create: `src/routing/fallback.py`
- Create: `src/routing/cost.py`
- Test: `tests/test_phase5_fallback.py`, `tests/test_phase5_cost.py`

**Interfaces:**
- Consumes: `ModelExecutionResult` and engineering cost weights.
- Produces: `validate_structural_output(result)`, `FallbackHandler`, `CostModel.calculate_cost(...)`.

- [ ] **Step 1: Write failing tests in `tests/test_phase5_fallback.py` and `tests/test_phase5_cost.py`**
  Verify fallback on malformed/empty outputs and cost function calculation $J = \text{loss} + \lambda_1 \text{latency} + \lambda_2 \text{compute}$.
- [ ] **Step 2: Run tests to verify failure**
  Run: `pytest tests/test_phase5_fallback.py tests/test_phase5_cost.py -v` (Expected: FAIL).
- [ ] **Step 3: Implement `src/routing/fallback.py` and `src/routing/cost.py`**
  Inspect structural validity without peeking at semantic ground truth. Log fallback events.
- [ ] **Step 4: Run tests to verify pass**
  Run: `pytest tests/test_phase5_fallback.py tests/test_phase5_cost.py -v` (Expected: PASS).

---

### Task 7: Decision Trace & Zero-Leakage Static Audit
**Files:**
- Create: `src/routing/decision_trace.py`
- Create: `src/routing/audit.py`
- Test: `tests/test_phase5_no_leakage.py`

**Interfaces:**
- Consumes: Routing execution state.
- Produces: Immutable JSON traces, static AST audit checking for label leakage and test metric peeking.

- [ ] **Step 1: Write failing test in `tests/test_phase5_no_leakage.py`**
  Verify audit flags illegal access to ground-truth answers or synthetic severity labels during routing.
- [ ] **Step 2: Run test to verify failure**
  Run: `pytest tests/test_phase5_no_leakage.py -v` (Expected: FAIL).
- [ ] **Step 3: Implement `src/routing/decision_trace.py` and `src/routing/audit.py`**
  Record structured traces and audit codebase against protocol leaks.
- [ ] **Step 4: Run test to verify pass**
  Run: `pytest tests/test_phase5_no_leakage.py -v` (Expected: PASS).

---

### Task 8: End-to-End Routing Pipeline & CLI Runners
**Files:**
- Create: `src/routing/router.py`
- Create: `src/routing/pipeline.py`
- Create: `src/routing/__init__.py`
- Create: `scripts/run_phase5_smoke.py`
- Create: `scripts/run_phase5_validation.py`
- Create: `scripts/run_phase5_benchmark.py`
- Test: `tests/test_phase5_determinism.py`, `tests/test_phase5_fairness.py`, `tests/test_phase5_statistics.py`

**Interfaces:**
- Produces: `AdaptiveRoutingPipeline.process(...)`, CLI execution entrypoints, paired bootstrap statistical analysis ($B=10,000$).

- [ ] **Step 1: Write failing tests in remaining test files**
  Test determinism, model fairness, and statistical evaluation routines.
- [ ] **Step 2: Run tests to verify failure**
  Run: `pytest tests/test_phase5_*.py -v` (Expected: FAIL).
- [ ] **Step 3: Implement `src/routing/router.py`, `pipeline.py`, and runner scripts**
  Wire feature extraction, routing decision, model execution, fallback, evaluation, trace generation, and statistical aggregation.
- [ ] **Step 4: Run all Phase 5 tests to verify pass**
  Run: `pytest tests/test_phase5_*.py -v` (Expected: ALL PASS).

---

### Task 9: Execution of Smoke & Validation Benchmarks
**Files:**
- Execute: `scripts/run_phase5_smoke.py`
- Execute: `scripts/run_phase5_validation.py`
- Output: `experiments/phase5/` (artifacts, traces, summaries, calibration data)

- [ ] **Step 1: Run smoke test**
  Run: `.venv\Scripts\python scripts/run_phase5_smoke.py`
  Verify end-to-end routing, fallback, and trace generation on fixed fixtures.
- [ ] **Step 2: Run validation evaluation & calibrate router on validation split**
  Run: `.venv\Scripts\python scripts/run_phase5_validation.py`
  Fit calibrator on validation split, determine optimal decision thresholds, freeze configuration.
- [ ] **Step 3: Run benchmark evaluation**
  Run: `.venv\Scripts\python scripts/run_phase5_benchmark.py`
  Evaluate policies across test partition, compute routing regret, confusion matrices, and paired bootstrap statistics for Hypothesis H2.

---

### Task 10: Ablation Studies (A1–A8) & Statistical Hypotheses
**Files:**
- Generate: `experiments/phase5/ablations/`
- Evaluate: A1 (No quality), A2 (Quality only), A3 (Uncertainty only), A4 (Quality + Uncertainty), A5 (Without fallback), A6 (With fallback), A7 (Feature groups: visual, geometric, photometric, compression, occlusion), A8 (All features).
- Evaluate H2 using Paired Bootstrap ($B=10,000$), Cliff's $\delta$, Cohen's $d$, 95% CIs.

---

### Task 11: Phase 5 Comprehensive Documentation & Reports
**Files:**
- Create: `reports/phase5/routing_architecture.md`
- Create: `reports/phase5/routing_policy.md`
- Create: `reports/phase5/uncertainty_calibration.md`
- Create: `reports/phase5/zero_leakage_audit.md`
- Create: `reports/phase5/routing_results.md`
- Create: `reports/phase5/model_selection_analysis.md`
- Create: `reports/phase5/routing_regret.md`
- Create: `reports/phase5/ablation_analysis.md`
- Create: `reports/phase5/cost_analysis.md`
- Create: `reports/phase5/statistical_analysis.md`
- Create: `reports/phase5/reproducibility_validation.md`
- Create: `reports/phase5/PHASE5_REPORT.md` (30 complete sections)

---

### Task 12: Governance Sync & Git Commit
**Files:**
- Modify: `task.md` (Add Phase 5 tasks, mark PASS)
- Modify: `phases.md` (Mark Phase 5 COMPLETED)
- Modify: `memory.md` (Update state, test counts, Phase 5 facts)
- Execute: Full regression test suite (`pytest -v`)
- Stage: `git add -A`
- Commit: `git commit -m "feat(phase5): implement adaptive quality-aware routing"` (DO NOT PUSH)
