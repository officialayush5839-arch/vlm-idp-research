# Phase 5 — Ablation Study Analysis (A1–A8)

## 1. Overview of Ablation Experiments
The ablation matrix evaluates the contribution of quality features, uncertainty signals, fallback handlers, and distinct visual degradation feature groups:

| Ablation ID | Description | Mean Score | Relative Compute | Fallback Rate | Mean Regret |
|:---|:---|:---:|:---:|:---:|:---:|
| **A1** | No Quality Features (Fixed Baseline B2) | 0.7778 | 1.0000 | 0.00% | 0.0178 |
| **A2** | Quality Features Only (R2 Rule-Based) | 0.7671 | 0.9222 | 0.00% | 0.0284 |
| **A3** | Uncertainty Only (R3 Uncertainty-Directed)| 0.6796 | 0.9467 | 35.56% | 0.1160 |
| **A4** | Quality + Uncertainty (R5 Composite) | 0.7724 | 0.9444 | 0.00% | 0.0231 |
| **A5** | Without Structural Fallback | 0.7671 | 0.9222 | 0.00% | 0.0284 |
| **A6** | With Structural Fallback | 0.7671 | 0.9222 | 0.00% | 0.0284 |
| **A8** | All 10 Features Jointly Evaluated | 0.7671 | 0.9222 | 0.00% | 0.0284 |

---

## 2. A7: Feature Group Sensitivity Analysis

Visual degradation feature groups were analyzed for their association with downstream accuracy drops:

1. **Spatial Occlusion Group (`occlusion`)**:
   - Severity $S_4$ Performance Drop: **$-0.8000$**
   - Criticality: **Highest**. Information destruction requires large-context generative priors.
2. **Geometric Distortion Group (`skew`, `perspective`)**:
   - Severity $S_4$ Performance Drop: **$-0.7400$**
   - Criticality: **Critical**. Completely invalidates axis-aligned OCR bounding boxes, requiring rotation-invariant vision backbones.
3. **Visual Sharpness Group (`blur`, `resolution`)**:
   - Severity $S_4$ Performance Drop: **$-0.6500$**
   - Criticality: **High**. Attenuates high-frequency character edge gradients.
4. **Signal & Compression Group (`noise`, `compression`)**:
   - Severity $S_4$ Performance Drop: **$-0.6400$**
   - Criticality: **High**. Perturbs token representations; effectively addressed by B0-U.
5. **Photometric Group (`illumination`, `contrast`, `glare`)**:
   - Severity $S_4$ Performance Drop: **$-0.5200$**
   - Criticality: **Moderate**. Handled well across both native VLMs and normalized OCR preprocessors.
