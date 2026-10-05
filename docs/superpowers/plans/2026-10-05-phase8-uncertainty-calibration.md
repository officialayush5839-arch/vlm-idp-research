# Phase 8: Uncertainty Calibration + Abstention Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement and scientifically validate an uncertainty-calibration and selective-prediction abstention subsystem residing in `src/uncertainty/` that reliably identifies low-confidence document intelligence outputs and enables safe abstention under visual degradation and long-document retrieval conditions without data leakage.

**Architecture:** A multi-signal uncertainty pipeline that ingests inference-observable features from Phase 3 (quality), Phase 5.1 (routing/model confidence), Phase 6 (retrieval margin/entropy), and Phase 7 (evidence support/grounding status), fits temperature scaling and isotonic regression models on the validation partition, freezes calibration parameters, evaluates risk-coverage dynamics across multiple coverage thresholds, and computes paired bootstrap hypothesis testing ($B=10,000$) for Hypothesis H6.

**Tech Stack:** Python 3.14.6, PyTorch (CPU-only), scikit-learn, numpy, pydantic v2, PyYAML, pytest.

**Spec:** PRD (`prd.md`), Architecture (`architecture.md`), Rules (`rules.md`), Phases (`phases.md`), Research Protocol (`research_protocol.md`), and Master Implementation Prompt for Phase 8.

## Global Constraints
- Preserve Phase 0 through Phase 7 scientific immutability (Phase 7 commit `9ea3b89`).
- DO NOT modify `src/evidence/`, `src/retrieval/`, `src/routing/`, or earlier phase code.
- Strict anti-fabrication: Never invent confidence, ECE, Brier score, coverage, or risk metrics.
- Zero runtime label leakage: Runtime code must NEVER access gold answers, gold evidence, or degradation family/severity labels.
- Calibration partition isolation: Fit calibration models and select abstention thresholds EXCLUSIVELY on the validation partition.
- Frozen test evaluation: Test partition must be evaluated with frozen calibration artifacts.
- Local commit only: `feat(phase8): implement uncertainty calibration and abstention`. DO NOT push to remote. DO NOT start Phase 9.

## Review Focus
1. Information boundary compliance: Explicitly tag all features as `OBSERVABLE_AT_INFERENCE`, `CALIBRATION_ONLY`, or `GROUND_TRUTH_ONLY`.
2. Calibration parameter freeze: Verify SHA-256 hash of serialized calibrators before and after test evaluation.
3. Monotonicity of selective risk: Validate that selective risk monotonically decreases or stays bounded as coverage decreases.
4. Degradation robustness: Evaluate uncertainty calibration across clean, mild, moderate, and severe degradation without leaking severity labels.
5. Trace identity uniqueness: Ensure run IDs (`run_P8_...`) are collision-free across all baselines, seeds, and conditions.

---

### Task 1: Configuration System (`configs/phase8/`)
- [ ] Create `configs/phase8/uncertainty_config.yaml`
- [ ] Create `configs/phase8/calibration_config.yaml`
- [ ] Create `configs/phase8/abstention_config.yaml`
- [ ] Create `configs/phase8/evaluation_config.yaml`
- [ ] Create `configs/phase8/experiment_matrix.yaml`
- [ ] Test configuration loading with `tests/test_phase8_config.py`

### Task 2: Information Boundary & Schemas (`src/uncertainty/schema.py`)
- [ ] Define Pydantic models: `UncertaintyFeatures`, `CalibrationArtifact`, `AbstentionDecision`, `UncertaintyPackage`, `CalibrationMetricsResult`, `SelectivePredictionMetricsResult`.
- [ ] Write `reports/phase8/uncertainty_information_boundary.md` documenting all features and their accessibility.
- [ ] Test schemas with `tests/test_phase8_schema.py`.

### Task 3: Signal Extraction & Feature Engineering (`src/uncertainty/signals.py`, `features.py`)
- [ ] Implement inference-observable feature extraction: model confidence, retrieval score margin, retrieval entropy, semantic support score, entity coverage, spatial valid flag, sufficiency enum, visual quality scores.
- [ ] Test feature extraction with `tests/test_phase8_features.py`.

### Task 4: Calibration Engines (`src/uncertainty/temperature.py`, `isotonic.py`, `calibration.py`)
- [ ] Implement `TemperatureScalingCalibrator` with negative log-likelihood optimization.
- [ ] Implement `IsotonicRegressionCalibrator` using isotonic piecewise constant regression.
- [ ] Implement `CalibrationManager` for fitting, serialization, cryptographic hashing, and prediction.
- [ ] Test calibration models with `tests/test_phase8_temperature.py`, `test_phase8_isotonic.py`, `test_phase8_calibration.py`.

### Task 5: Selective Prediction & Abstention (`src/uncertainty/abstention.py`, `selective.py`)
- [ ] Implement threshold-based abstention logic (`ANSWER` vs `ABSTAIN`).
- [ ] Implement threshold selection on the calibration partition for target coverage levels (100%, 95%, 90%, 80%, 70%, 60%, 50%).
- [ ] Test abstention with `tests/test_phase8_abstention.py`, `test_phase8_selective.py`.

### Task 6: Metrics & Statistical Rigor (`src/uncertainty/metrics.py`)
- [ ] Implement ECE (Expected Calibration Error), MCE, Brier Score, reliability diagram bins.
- [ ] Implement selective risk, coverage, AURC (Area Under Risk-Coverage Curve), selective accuracy.
- [ ] Implement paired bootstrap test ($B=10,000$, seed=42) for Hypothesis H6.
- [ ] Test metrics with `tests/test_phase8_metrics.py`.

### Task 7: Provenance, Collision Prevention & Static AST Audit (`src/uncertainty/provenance.py`, `audit.py`)
- [ ] Implement run ID generation: `run_P8_{dataset}_{baseline}_{doc}_{query}_{condition}_s{seed}`.
- [ ] Implement collision-free trace serializer with SHA-256 fingerprinting.
- [ ] Implement static AST zero-leakage auditor.
- [ ] Test provenance and audit with `tests/test_phase8_provenance.py`, `test_phase8_trace_identity.py`, `test_phase8_trace_collision.py`, `test_phase8_no_leakage.py`.

### Task 8: Master Pipeline & Baseline Registry (`src/uncertainty/pipeline.py`, `baselines.py`)
- [ ] Implement `UncertaintyPipeline` integrating extraction, calibration, and abstention.
- [ ] Register baselines A0 (No Abstention), A1 (Random Abstention), A2 (Uncalibrated Confidence), A3 (Temperature Scaled), A4 (Isotonic Calibrated), A5 (Evidence-Aware Calibrated).
- [ ] Test pipeline with `tests/test_phase8_determinism.py`, `test_phase8_partition_integrity.py`, `test_phase8_calibration_freeze.py`, `test_phase8_regression.py`.

### Task 9: Experiment Execution (`scripts/run_phase8_*.py`)
- [ ] Create and run `scripts/run_phase8_smoke.py`: smoke test across all baselines.
- [ ] Create and run `scripts/run_phase8_calibrate.py`: fit calibrators on validation partition and freeze artifacts.
- [ ] Create and run `scripts/run_phase8_benchmark.py`: evaluate on test partition across 5 seeds, compute metrics and H6 hypothesis test.
- [ ] Create and run `scripts/run_phase8_ablations.py`: evaluate ablations A1–A8.
- [ ] Create and run `scripts/generate_phase8_figures.py`: generate publication-grade figures in `experiments/phase8/figures/`.

### Task 10: Research Documentation & Governance Sign-Off
- [ ] Authored 16 detailed scientific reports in `reports/phase8/` and master 30-section `PHASE8_REPORT.md`.
- [ ] Verify historical Phase 0–7 integrity.
- [ ] Update `task.md`, `phases.md`, `memory.md`.
- [ ] Execute full repository regression test suite (all 267 prior tests + all Phase 8 tests).
- [ ] Create clean local commit: `feat(phase8): implement uncertainty calibration and abstention`.
- [ ] Mandatory stop at Phase 8 boundary.
