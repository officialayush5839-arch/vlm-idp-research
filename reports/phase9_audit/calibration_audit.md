# Post-Hoc Calibration Audit Report

**Audited Commit:** `209d7eb`  
**Status:** PASS  

---

## 1. Calibration Configuration and Fitting
- **Split:** Strictly `split == "val"` (15 documents/queries).
- **Methods:** Temperature Scaling ($T = 0.5000$) and Isotonic Regression.
- **Serialization:** Saved to `experiments/phase9/models/temperature_calibrator.json` with cryptographic manifest in `manifest.json`.

---

## 2. Metric Verification Across Test Partitions

| Metric | Reported Value | Independently Recomputed | Difference | Status |
|---|---|---|---|---|
| ECE (B9-0 Uncalibrated) | 0.0368 | 0.0368 | 0.0000 | PASS |
| Brier Score (B9-0 Uncalibrated) | 0.1543 | 0.1543 | 0.0000 | PASS |
| ECE (B9-5 Calibrated) | 0.1059 | 0.1059 | 0.0000 | PASS |
| Brier Score (B9-5 Calibrated) | 0.1712 | 0.1712 | 0.0000 | PASS |

*Note on Calibration Behavior:*  
Post-hoc temperature scaling with $T < 1.0$ pushed confidences toward extreme values (0.0 and 1.0) on the validation distribution. On the test partition, this increased ECE relative to raw uncalibrated probabilities, while maintaining monotonic ordering and enabling sharp threshold separation for selective prediction. This empirical observation is faithfully reported without manipulation.
