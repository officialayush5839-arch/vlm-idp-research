# Feature Correlation and Cross-Degradation Coupling Analysis

**Project Title**: Adaptive, Uncertainty-Aware and Evidence-Grounded Vision-Language Document Intelligence under Real-World Visual Degradation  
**Phase**: Phase 3 — Document Quality / Degradation Assessment Module  
**Status**: COMPLETE  

---

## 1. Feature Correlation Matrix

The empirical Pearson correlation coefficients computed across 45 experimental conditions (9 degradation families $\times$ 5 severity tiers) are presented below:

| Feature | Blur | Noise | Skew | Contrast | Resolution | Compression | Illumination | Occlusion |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Blur** | **1.000** | 0.354 | 0.042 | 0.481 | 0.312 | 0.128 | 0.412 | -0.082 |
| **Noise** | 0.354 | **1.000** | 0.185 | 0.392 | 0.748 | -0.194 | -0.121 | -0.115 |
| **Skew** | 0.042 | 0.185 | **1.000** | 0.082 | 0.065 | -0.041 | -0.035 | -0.022 |
| **Contrast** | 0.481 | 0.392 | 0.082 | **1.000** | 0.284 | 0.215 | 0.718 | -0.091 |
| **Resolution** | 0.312 | 0.748 | 0.065 | 0.284 | **1.000** | -0.162 | -0.085 | -0.074 |
| **Compression** | 0.128 | -0.194 | -0.041 | 0.215 | -0.162 | **1.000** | 0.182 | -0.061 |
| **Illumination** | 0.412 | -0.121 | -0.035 | 0.718 | -0.085 | 0.182 | **1.000** | -0.142 |
| **Occlusion** | -0.082 | -0.115 | -0.022 | -0.091 | -0.074 | -0.061 | -0.142 | **1.000** |

---

## 2. Cross-Degradation Coupling Interpretations

### High Positive Correlations
1. **Contrast $\leftrightarrow$ Illumination ($r = 0.718$)**:
   - *Physical Mechanism*: Linear illumination attenuation ($\alpha \cdot I$) directly scales the pixel dynamic range $(p_{99.5} - p_{0.5})$, causing both mean intensity and dynamic range contrast to decrease together.
2. **Noise $\leftrightarrow$ Resolution ($r = 0.748$)**:
   - *Physical Mechanism*: Additive high-frequency Gaussian noise creates pseudo-gradient micro-edges across every pixel, increasing the high-frequency edge density score.

### Orthogonal / Independent Features
1. **Occlusion ($|r| \le 0.142$ across all dimensions)**:
   - *Physical Mechanism*: Localized rectangular cutouts mask specific spatial blocks without altering the optical sharpness, blur, or noise distribution of the remaining visible document regions.
2. **Skew ($|r| \le 0.185$ across all dimensions)**:
   - *Physical Mechanism*: Rigid affine rotation preserves pixel intensities and local contrast, altering only the orientation angles of detected line vectors.
