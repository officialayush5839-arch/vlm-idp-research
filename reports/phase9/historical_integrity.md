# Historical Integrity Verification Record — Pre-Phase 9

**Date:** 2026-10-06  
**Auditor:** Research Engineer / CI System  
**Parent Phase:** Phase 8 (Frozen at `8eabd1f`)  
**Scope:** Verification of all frozen model artifacts and baseline manifests prior to Phase 9 execution.

---

## 1. Frozen Phase 8 Calibrator Artifacts

The following models and decision thresholds were trained/selected strictly on validation split (`split == "val"`) during Phase 8 and are immutable:

| Artifact Path | SHA-256 Digest | Status |
|---|---|---|
| `experiments/phase8/models/abstention_thresholds.json` | `2c2c0d470c96b6108c15c43191e3a5aad17a071067f40c23c5bcabe6bb0753aa` | FROZEN / VERIFIED |
| `experiments/phase8/models/evidence_aware_calibrator.json` | `dfefca7fe32e352d449c699ec14e846d070fc17ae165b2690b8ec5f2e15887c2` | FROZEN / VERIFIED |
| `experiments/phase8/models/isotonic_calibrator.json` | `82e56eb515b3a4d68ab2e1838ba3fdec480c7c437136022f132daaba8e491e64` | FROZEN / VERIFIED |
| `experiments/phase8/models/manifest.json` | `a9a6067121c6a557a6bb799cf488621bbf5ccf36e848eae75e531c281e6997c8` | FROZEN / VERIFIED |
| `experiments/phase8/models/temperature_scaling_calibrator.json` | `54ad8d01c1cbc1dd2ff515f83d0134fb890f1d17e0f5790a964a37351441a22f` | FROZEN / VERIFIED |

---

## 2. Test Suite Baseline
- **Execution Date:** 2026-10-06
- **Test Count:** 302 passed in full test suite (100% pass rate).
- **Environment:** Windows, Python 3.14.6, PyTorch 2.14.1+cpu.
- **Git Commit:** `8eabd1f feat(phase8): implement uncertainty calibration and abstention` (clean working tree).

---

## 3. Protocol Invariants Enforced
1. All Phase 0–8 code, models, and traces are strictly read-only.
2. Phase 9 calibrators and thresholds must be fit exclusively on `split == "val"`.
3. The test set (`split == "test"`) is reserved strictly for unbiased evaluation.
4. Any synthetic evaluation data must be labeled `SYNTHETIC_VALIDATION`.
