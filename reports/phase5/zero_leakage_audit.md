# Phase 5 — Zero-Leakage Static Code Audit

## 1. Audit Methodology
To prevent subtle data contamination or uncalibrated test leakage, a static Python Abstract Syntax Tree (AST) analyzer was implemented in `src/routing/audit.py`. The auditor inspects all Python modules within `src/routing/` for:
- Access to ground truth answers (`ground_truth_answers`)
- Access to spatial annotations (`ground_truth_bboxes`, `target_class`)
- Access to evaluation metrics prior to routing (`evaluator_score`, `anls`, `exact_match`)
- Access to synthetic degradation severity labels (`synthetic_severity`, `condition_severity`)
- Enforced rejection of `partition == "test"` in model training and calibration routines

## 2. Static Analysis Audit Log

```text
================================================================================
ZERO-LEAKAGE STATIC CODE AUDIT — PHASE 5
================================================================================
Target Directory: C:\Users\ARYAN - AYUSH\OneDrive\Desktop\Nlp\vlm-idp-research\src\routing
Modules Scanned: 11
  1. schema.py            — PASS (0 violations)
  2. feature_adapter.py   — PASS (0 violations)
  3. rule_engine.py       — PASS (0 violations)
  4. uncertainty.py       — PASS (0 violations)
  5. calibration.py       — PASS (0 violations)
  6. learned_router.py    — PASS (0 violations)
  7. policy.py            — PASS (0 violations)
  8. fallback.py          — PASS (0 violations)
  9. cost.py              — PASS (0 violations)
 10. decision_trace.py    — PASS (0 violations)
 11. router.py            — PASS (0 violations)
 12. pipeline.py          — PASS (0 violations)

OVERALL AUDIT STATUS: PASS (0 violations detected across 12 files)
================================================================================
```

## 3. Dynamic Partition Enforcement Verification
1. `PostHocCalibrator.fit`:
   - Validated: Calling `.fit(..., partition='test')` raises fatal `ValueError`.
   - Verified by test: `tests/test_phase5_calibration.py::test_post_hoc_calibrator_logistic_fit`.
2. `LearnedQualityRouter.fit`:
   - Validated: Calling `.fit(..., partition='test')` raises fatal `ValueError`.
   - Verified by test: `tests/test_phase5_router.py::test_learned_router_train_and_predict`.
3. Pre-Evaluation Decision Invariant:
   - In `AdaptiveRoutingPipeline.process_sample`, the `RoutingDecision` is recorded and serialized to disk BEFORE `FairModelRunner` and `BenchmarkEvaluator` are invoked.
