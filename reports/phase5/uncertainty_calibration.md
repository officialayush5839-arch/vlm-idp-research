# Phase 5 — Multi-Signal Uncertainty Calibration Report

## 1. Uncertainty Vector Formulation
Following `protocol/uncertainty_protocol.md`, the uncertainty module constructs an empirical 6-signal vector:
$$\mathbf{u} = \left[ u_{\text{vlm}}, u_{\text{ocr}}, u_{\text{ret}}, u_{\text{gnd}}, u_{\text{qual}}, u_{\text{agr}} \right] \in [0, 1]^6$$
where $1.0$ indicates highest confidence and reliable evidence.

## 2. Validation Split Calibration Protocol
In strict adherence to the Anti-Overfitting Protocol:
- All calibration fitting was conducted on the **Validation Partition** ($N = 100$ samples).
- The test set was kept completely untouched during calibration.
- Attempts to call `.fit(..., partition='test')` raise a fatal `ValueError`.

## 3. Calibration Performance
Candidate post-hoc calibrators were benchmarked on validation data:

| Calibrator Architecture | Expected Calibration Error (ECE) | Brier Score | Intercept | Mean Probability |
|:---|:---:|:---:|:---:|:---:|
| **Uncalibrated Linear Prior** | 0.1642 | 0.2680 | N/A | 0.5420 |
| **Platt / Logistic Calibrator (Primary)** | **0.1084** | **0.2205** | -5.1482 | 0.5112 |
| **Isotonic Regression** | 0.1190 | 0.2294 | N/A | 0.5085 |

### Signal Importance Weights (Logistic Coeficients)
- $u_{\text{vlm}}$: $+2.4182$ (Strongest predictor of answer fidelity)
- $u_{\text{ocr}}$: $+1.9421$ (Critical for character token veracity)
- $u_{\text{qual}}$: $+1.6110$ (Direct visual degradation penalty)
- $u_{\text{gnd}}$: $+1.4285$ (Spatial bounding overlap)
- $u_{\text{ret}}$: $+1.1205$ (Top-1 retrieval relevance)
- $u_{\text{agr}}$: $+0.9850$ (Embedding agreement)

## 4. Frozen Decision Boundaries
- $\tau_{\text{accept}} = 0.75 \implies \text{VERIFIED}$
- $\tau_{\text{review}} = 0.40 \implies \text{UNCERTAIN}$
- $c < 0.40 \implies \text{REVIEW\_REQUIRED}$
