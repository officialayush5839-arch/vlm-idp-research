# Partition Integrity & Leakage Audit Report

**Audited Commit:** `209d7eb`  
**Status:** PASS (Strict Validation/Test Isolation Verified)  

---

## 1. Partition Definitions in Corpus Manifest
- **Source:** `experiments/phase6/indexes/corpus_manifest.json`
- **Validation Documents:** 15 (`split == "val"`)
- **Test Documents:** 25 (`split == "test"`)
- **Intersection:** $\emptyset$ (Disjoint sets verified by unit test `test_partition_split_manifest`).

---

## 2. Partition Usage Across Subsystems

| Module | Operation | Partition Consumed | Test Contamination? | Status |
|---|---|---|---|---|
| `scripts/run_phase9_calibrate.py` | Temperature & Isotonic Fitting | Validation (`split == "val"`, 15 docs) | NO | PASS |
| `scripts/run_phase9_calibrate.py` | Threshold Derivation ($\tau$) | Validation (`split == "val"`, 15 docs) | NO | PASS |
| `scripts/run_phase9_benchmark.py` | Baseline Evaluation | Test (`split == "test"`, 25 docs $\times$ 5 seeds) | N/A (Eval only) | PASS |
| `scripts/run_phase9_ablations.py` | Ablation Evaluation (A9-1..8) | Test (`split == "test"`, 25 docs) | N/A (Eval only) | PASS |

---

## 3. Findings
1. Neither test labels nor test performance metrics were accessed during the execution of `run_phase9_calibrate.py`.
2. All thresholds stored in `experiments/phase9/models/reliability_thresholds.json` are computed strictly from validation scores.
3. Zero leakage invariant is strictly satisfied.
