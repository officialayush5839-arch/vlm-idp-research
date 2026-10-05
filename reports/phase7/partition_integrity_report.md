# Phase 7 Partition Integrity and Isolation Report

## 1. Partition Hygiene
Phase 7 preserves strict split boundaries established in Phase 1:
- `train`: Used for baseline development and representation calibration.
- `val`: Used for threshold exploration in `scripts/run_phase7_validation.py`.
- `test`: Evaluated solely under frozen configurations in `scripts/run_phase7_benchmark.py`.

## 2. Invariants
- Zero test document leakage into validation or tuning routines.
- Derived degradation variants inherit source document partition splits.
- Provenance records explicitly track partition origin (`split: test`).
- Test split integrity confirmed across all 25 test documents and 25 test queries.
