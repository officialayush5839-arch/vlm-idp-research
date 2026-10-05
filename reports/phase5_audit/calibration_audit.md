# PHASE 5 SCIENTIFIC AUDIT — POST-HOC CALIBRATION AUDIT

**Audit Item**: Uncertainty Calibration, ECE, Brier Score, and Validation Partition Protocol  
**Audit Status**: VERIFIED NUMERICALLY / QUALIFIED METHODOLOGICALLY (P2 — Synthetic Validation Data)  

---

## 1. Audit Target & Stored Artifacts
- **Module Under Test**: `src/routing/calibration.py` (`PostHocCalibrator`)
- **Execution Script**: `scripts/run_phase5_validation.py`
- **Stored Artifact**: `experiments/phase5/calibration/calibration_metrics.json`
- **Method**: Multidimensional Logistic Calibration mapping $\mathbf{u} \in [0, 1]^6 \to c \in [0, 1]$
- **Thresholds**: $\tau_{\text{accept}} = 0.75$, $\tau_{\text{review}} = 0.40$

---

## 2. Numerical Reconciliation

| Metric | Reported in Report | Stored in JSON Artifact | Recomputed Value | Absolute Difference | Audit Status |
|:---|:---:|:---:|:---:|:---:|:---:|
| **Expected Calibration Error (ECE)** | 0.1084 | 0.108438275190209 | 0.108438275190209 | $0.0000$ | **VERIFIED** |
| **Brier Score** | 0.2205 | 0.220544677632881 | 0.220544677632881 | $0.0000$ | **VERIFIED** |
| **Calibration Intercept** | -2.0235 | -2.023473422622867 | -2.023473422622867 | $0.0000$ | **VERIFIED** |
| **Weight Count** | 6 | 6 | 6 | 0 | **VERIFIED** |

Numerical verification is exact within 64-bit floating point precision.

---

## 3. Methodological Audit & Partition Boundaries
- **Partition Verification**: Calibrator `fit()` strictly verifies `partition == "val"`. Attempting to fit on `partition="test"` raises an immediate fatal `ValueError`. This satisfies zero-test-leakage requirements.
- **Validation Data Source Finding**:
  In `scripts/run_phase5_validation.py` (lines 30–43):
  The 100 validation samples were **synthetically generated random beta-distributed vectors** (`np.random.beta(a=2.0, b=2.0, size=(100, 6))`) with success probabilities computed via a synthetic logistic link:
  $$P(\text{success}) = \sigma(10.0 \cdot (L - 0.50))$$
  where $L = \sum_i w_i u_i$.
  They were NOT drawn from real validation-partition document images of DocVQA or FUNSD.

### Methodological Classification:
- **Leakage Status**: ZERO LEAKAGE (no test data touched).
- **Scientific Qualification**: The reported calibration error ($ECE = 0.1084$) demonstrates that the `PostHocCalibrator` algorithm works correctly on a known synthetic validation distribution. However, it must NOT be represented in the IEEE paper as empirical calibration on real benchmark documents.
