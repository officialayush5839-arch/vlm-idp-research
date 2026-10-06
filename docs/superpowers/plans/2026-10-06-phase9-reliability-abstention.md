# Phase 9: Uncertainty-Aware Reliability, Abstention & Failure-Safety Evaluation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

## Overview
Implement the Phase 9 Reliability and Failure-Safety decision layer for the VLM-IDP project. The system aggregates signals from Phase 3 (Quality), Phase 6 (Retrieval), Phase 7 (Grounding), and Phase 8 (Calibration) into an 8-dimensional observable uncertainty vector, produces calibrated confidence estimates, enforces selective prediction and abstention policies (`ACCEPT`, `ACCEPT_WITH_WARNING`, `ESCALATE`, `ABSTAIN`), and evaluates failure modes using an 8-class taxonomy across a multi-seed benchmark.

## Task Decomposition

### Task 1: Configuration System (`configs/phase9/`)
- [ ] Create YAML configuration files: `reliability_config.yaml`, `uncertainty_config.yaml`, `calibration_config.yaml`, `abstention_config.yaml`, `threshold_config.yaml`, `experiment_matrix.yaml`, `evaluation_config.yaml`.
- [ ] Create `tests/test_phase9_config.py` to validate schema, loading, defaults, and immutability.
- [ ] Run test suite and verify passing.

### Task 2: Core Schemas, Signals & Uncertainty Vector Modeling (`src/reliability/`)
- [ ] Implement `src/reliability/schema.py`: Enums (`ReliabilityAction`, `FailureMode`), Dataclasses (`UncertaintyVector`, `ReliabilityDecision`, `ReliabilityPackage`, `FailureModeResult`).
- [ ] Implement `src/reliability/signals.py`: Observable signal extraction from prior phases without ground truth leakage.
- [ ] Implement `src/reliability/uncertainty.py`: 8D Uncertainty vector math and normalization:
  $$U = [u_{\text{retrieval}}, u_{\text{semantic}}, u_{\text{spatial}}, u_{\text{numeric}}, u_{\text{table}}, u_{\text{sufficiency}}, u_{\text{quality}}, u_{\text{agreement}}] \in [0, 1]^8$$
- [ ] Implement `src/reliability/confidence.py`: Confidence models C0 (Raw), C1 (Weighted composite), C2 (Calibrated composite).
- [ ] Write and verify tests: `tests/test_phase9_schema.py`, `tests/test_phase9_signals.py`, `tests/test_phase9_uncertainty.py`, `tests/test_phase9_confidence.py`.

### Task 3: Calibration, Abstention Policies, Risk & Metrics
- [ ] Implement `src/reliability/calibration.py`: Validation-only calibration wrappers.
- [ ] Implement `src/reliability/abstention.py`: Multi-threshold decision rules mapping confidence and uncertainty to actions (`ACCEPT`, `ACCEPT_WITH_WARNING`, `ESCALATE`, `ABSTAIN`).
- [ ] Implement `src/reliability/selective_prediction.py`: Risk-coverage curve calculation, optimal coverage selection.
- [ ] Implement `src/reliability/failure_modes.py`: Structured 8-class failure classifier ($F_1$ to $F_8$).
- [ ] Implement `src/reliability/risk.py` & `src/reliability/metrics.py`: AURC, E-AURC, Selective Accuracy, Selective Risk, Abstention Precision/Recall, ECE, Brier score.
- [ ] Write and verify tests: `tests/test_phase9_calibration.py`, `tests/test_phase9_abstention.py`, `tests/test_phase9_selective_prediction.py`, `tests/test_phase9_failure_modes.py`, `tests/test_phase9_metrics.py`.

### Task 4: Pipeline, Baselines & Provenance System
- [ ] Implement `src/reliability/provenance.py`: Trace ID generator `run_P9_{dataset}_{baseline}_{doc}_{query}_{condition}_s{seed}` and collision detector.
- [ ] Implement `src/reliability/audit.py`: AST static analysis to prove zero test leakage.
- [ ] Implement `src/reliability/baselines.py`: B9-0 (No Abstention), B9-1 (Grounding-Only), B9-2 (Fixed Confidence), B9-3 (Quality-Only), B9-4 (Evidence-Only), B9-5 (Proposed Multi-Signal).
- [ ] Implement `src/reliability/pipeline.py`: Master `ReliabilityPipeline`.
- [ ] Write and verify tests: `tests/test_phase9_determinism.py`, `tests/test_phase9_no_leakage.py`, `tests/test_phase9_partition_integrity.py`, `tests/test_phase9_trace_identity.py`, `tests/test_phase9_provenance.py`, `tests/test_phase9_regression.py`, `tests/test_phase9_validation.py`.

### Task 5: Experiment Execution & Statistical Evaluation
- [ ] Create `scripts/run_phase9_smoke.py`: Quick end-to-end pipeline verification.
- [ ] Create `scripts/run_phase9_calibrate.py`: Calibration & threshold fitting strictly on validation split (`split == "val"`).
- [ ] Create `scripts/run_phase9_benchmark.py`: Execute B9-0 through B9-5 across 5 seeds on test partition (125 evaluations, 750 traces), compute metrics, and run paired bootstrap ($B=10,000$, seed=42) to test Hypothesis H9.
- [ ] Create `scripts/run_phase9_ablations.py`: Run ablations A1–A8.
- [ ] Create `scripts/generate_phase9_figures.py`: Generate publication-grade PNG diagrams via Pillow.

### Task 6: Comprehensive Documentation, Verification & Git Commit
- [ ] Author all 18 reports in `reports/phase9/` and master `PHASE9_REPORT.md` (34 sections).
- [ ] Verify historical Phase 0–8 immutability.
- [ ] Update `task.md`, `memory.md`, `phases.md`.
- [ ] Run entire pytest test suite (Phases 0–9).
- [ ] Commit locally: `feat(phase9): implement uncertainty-aware reliability and abstention`.
- [ ] Stop at Phase 9 boundary.
