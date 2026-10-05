# Report 11: Ablation Study on Calibration Engines (A5–A6)

## 1. Experimental Design
We evaluated the relative efficacy of different calibration algorithms applied to the multi-signal features:
1. **Uncalibrated Raw**: Pass-through raw model confidence without post-hoc transformation.
2. **Temperature Scaling (A3)**: Parametric logit rescaling optimized via NLL minimization.
3. **Isotonic Regression (A4)**: Non-parametric piecewise constant regression fitted on raw confidence.
4. **Evidence-Aware Isotonic Regression (A5 / Proposed)**: Non-parametric isotonic regression applied to multi-signal composite confidence.

## 2. Quantitative Results

| Engine | ECE | Brier Score | AURC | Excess AURC | AUROC |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Uncalibrated Raw** | 0.1520 | 0.1453 | 0.1578 | 0.1143 | 0.7807 |
| **Temperature Scaling** | **0.1192** | 0.1375 | 0.1578 | 0.1143 | 0.7807 |
| **Isotonic Regression** | 0.1600 | 0.1500 | 0.1578 | 0.1143 | 0.7281 |
| **Evidence-Aware Isotonic** | 0.1359 | **0.1016** | **0.0923** | **0.0488** | **0.8158** |

## 3. Key Insights
1. **Temperature Scaling** yields the lowest pure ECE on raw scores (0.1192) due to smooth global stretching of logits, but leaves AUROC and AURC unchanged because rank ordering is strictly preserved.
2. **Evidence-Aware Isotonic Regression** achieves the best overall risk-coverage profile (AURC = 0.0923 vs 0.1578) and lowest probability error (Brier = 0.1016 vs 0.1453), proving that post-hoc calibration combined with multi-signal feature fusion provides the strongest selective prediction performance.
