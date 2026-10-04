# Degradation Severity Classification & Boundary Validation

**Project Title**: Adaptive, Uncertainty-Aware and Evidence-Grounded Vision-Language Document Intelligence under Real-World Visual Degradation  
**Phase**: Phase 3 — Document Quality / Degradation Assessment Module  
**Status**: VALIDATED  

---

## 1. Severity Scale Architecture

The Phase 0 Research Protocol defines five discrete severity tiers:
- **$S_0$ (Clean)**: Baseline pristine document, unaffected by degradation.
- **$S_1$ (Mild)**: Subtle artifacts; legible to human readers with minimal cognitive load.
- **$S_2$ (Moderate)**: Visible distortion; conventional OCR begins exhibiting character errors.
- **$S_3$ (Severe)**: High corruption; standard OCR fails significantly; VLM attention degrades.
- **$S_4$ (Extreme)**: Catastrophic corruption; human reading requires reconstruction.

---

## 2. Empirical Severity Step Curves

### Gaussian Noise ($\sigma \in \{0, 5, 15, 30, 50\}$)
- $s=0$: $\hat{\sigma} = 1.75 \rightarrow S_0$ (Clean)
- $s=1$: $\hat{\sigma} = 4.64 \rightarrow S_1$ (Mild)
- $s=2$: $\hat{\sigma} = 8.50 \rightarrow S_2$ (Moderate)
- $s=3$: $\hat{\sigma} = 14.07 \rightarrow S_3$ (Severe)
- $s=4$: $\hat{\sigma} = 21.55 \rightarrow S_4$ (Extreme)
- **Mean Absolute Severity Error**: **0.00**.

### Skew / Rotation ($\theta \in \{0^\circ, 1^\circ, 3^\circ, 5^\circ, 10^\circ\}$)
- $s=0$: $|\theta| = 0.00^\circ \rightarrow S_0$ (Clean)
- $s=1$: $|\theta| = 1.00^\circ \rightarrow S_1$ (Mild)
- $s=2$: $|\theta| = 3.00^\circ \rightarrow S_2$ (Moderate)
- $s=3$: $|\theta| = 5.00^\circ \rightarrow S_3$ (Severe)
- $s=4$: $|\theta| = 10.00^\circ \rightarrow S_4$ (Extreme)
- **Mean Absolute Severity Error**: **0.00**.

### Illumination Attenuation ($\alpha \in \{1.00, 0.75, 0.50, 0.30, 0.15\}$)
- $s=0$: $\mu = 246.99 \rightarrow S_0$ (Clean)
- $s=1$: $\mu = 185.24 \rightarrow S_1$ (Mild)
- $s=2$: $\mu = 123.49 \rightarrow S_2$ (Moderate)
- $s=3$: $\mu = 74.10 \rightarrow S_3$ (Severe)
- $s=4$: $\mu = 37.05 \rightarrow S_4$ (Extreme)
- **Mean Absolute Severity Error**: **0.00**.

### Occlusion Coverage ($A_{\text{occ}} \in \{0\%, 5\%, 10\%, 20\%, 30\%\}$)
- $s=0$: $A = 0.00\% \rightarrow S_0$ (Clean)
- $s=1$: $A = 4.96\% \rightarrow S_1$ (Mild)
- $s=2$: $A = 9.94\% \rightarrow S_2$ (Moderate)
- $s=3$: $A = 19.98\% \rightarrow S_3$ (Severe)
- $s=4$: $A = 29.98\% \rightarrow S_4$ (Extreme)
- **Mean Absolute Severity Error**: **0.00**.

### Resolution Reduction ($r \in \{1.00, 0.75, 0.50, 0.25, 0.15\}$)
- $s=0$: $R_{\text{sharp}} = 0.9100 \rightarrow S_0$ (Clean)
- $s=1$: $R_{\text{sharp}} = 0.7180 \rightarrow S_1$ (Mild)
- $s=2$: $R_{\text{sharp}} = 0.6127 \rightarrow S_2$ (Moderate)
- $s=3$: $R_{\text{sharp}} = 0.1078 \rightarrow S_3$ (Severe)
- $s=4$: $R_{\text{sharp}} = 0.0000 \rightarrow S_4$ (Extreme)
- **Mean Absolute Severity Error**: **0.00**.

### Perspective Distortion ($\phi \in \{0^\circ, 5^\circ, 15^\circ, 25^\circ, 35^\circ\}$)
- $s=0$: $\theta_{\text{conv}} = 0.00^\circ \rightarrow S_0$ (Clean)
- $s=1$: $\theta_{\text{conv}} = 5.92^\circ \rightarrow S_1$ (Mild)
- $s=2$: $\theta_{\text{conv}} = 19.65^\circ \rightarrow S_2$ (Moderate)
- $s=3$: $\theta_{\text{conv}} = 33.81^\circ \rightarrow S_3$ (Severe)
- $s=4$: $\theta_{\text{conv}} = 47.87^\circ \rightarrow S_4$ (Extreme)
- **Mean Absolute Severity Error**: **0.00**.

---

## 3. Ordered Error Metrics

Across all 8 pure degradation families $\times$ 5 severity levels (40 experimental conditions):
- **Exact Severity Match Accuracy**: **82.5%** (33 / 40 conditions).
- **Within-One-Level Accuracy ($\pm 1$ Severity Tier)**: **100.0%** (40 / 40 conditions).
- **Global Mean Absolute Severity Error (MASE)**: **0.225**.
