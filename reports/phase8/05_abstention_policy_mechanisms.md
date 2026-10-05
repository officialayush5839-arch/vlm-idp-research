# Report 05: Selective Prediction and Abstention Policy Mechanisms

## 1. Decision Function
A selective classification model consists of a prediction function $f(X)$ and a selection function $g(X) \in \{0, 1\}$.
In Phase 8:
$$g(X) = \mathbb{I}(\hat{P}_{\text{cal}} \ge \tau)$$
where $\hat{P}_{\text{cal}}$ is calibrated confidence and $\tau \in [0, 1]$ is the acceptance threshold calibrated on validation data.
- If $g(X) = 1$: system outputs $(\hat{A}, \text{ANSWER})$ with confidence $\hat{P}_{\text{cal}}$.
- If $g(X) = 0$: system outputs $(\emptyset, \text{ABSTAIN})$ with recorded abstention reason.

## 2. Verification Status Assignment
Each inference decision is mapped into a three-state operational triage status:
- **`VERIFIED`**: Calibrated confidence $\ge 0.80$ and evidence sufficiency is `SUFFICIENT`.
- **`UNCERTAIN`**: Borderline confidence or abstained without critical evidence failure.
- **`REVIEW_REQUIRED`**: Abstained with `INSUFFICIENT_EVIDENCE` or severe degradation ($Q < 0.40$).

## 3. Threshold Calibration Table
Selected on the validation partition (`split == 'val'`) and frozen:

| Target Coverage | A0 Threshold | A1 Threshold | A2 Threshold | A3 Threshold | A4 Threshold | A5 Proposed Threshold |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| 100% | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| 95% | 0.0000 | 0.0500 | 0.4200 | 0.3186 | 0.2500 | 0.0000 |
| 90% | 0.0000 | 0.1000 | 0.4200 | 0.3186 | 0.2500 | 0.0000 |
| **80%** | **0.0000** | **0.2000** | **0.4200** | **0.3186** | **0.2500** | **0.5000** |
| 70% | 0.0000 | 0.3000 | 0.6600 | 0.8267 | 0.7500 | 0.5000 |
| 60% | 0.0000 | 0.4000 | 0.6600 | 0.8267 | 0.7500 | 1.0000 |
| 50% | 0.0000 | 0.5000 | 0.6600 | 0.8267 | 0.7500 | 1.0000 |
