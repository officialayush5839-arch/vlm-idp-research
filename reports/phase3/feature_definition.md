# Visual Quality Feature Formulations and Metrics

**Project Title**: Adaptive, Uncertainty-Aware and Evidence-Grounded Vision-Language Document Intelligence under Real-World Visual Degradation  
**Phase**: Phase 3 — Document Quality / Degradation Assessment Module  
**Status**: FROZEN / VERIFIED  

---

## 1. Feature Registry & Mathematical Formulations

The Phase 3 Quality Subsystem implements 10 distinct, deterministic visual quality feature extractors. Each feature corresponds directly to optical, sensor, codec, geometric, or photometric phenomena.

| Feature Identifier | Corresponding Degradation Family | Primary Mathematical Metric | Polarity | Cutoff Thresholds $[T_1, T_2, T_3, T_4]$ |
|:---|:---|:---|:---:|:---:|
| **blur** | Gaussian Blur | Variance of Laplacian $\text{Var}(\Delta I)$ | `lower_is_worse` | $[2500.0, 500.0, 100.0, 25.0]$ |
| **noise** | Gaussian Noise | Immerkaer Fast Noise $\hat{\sigma}_n$ | `higher_is_worse` | $[3.0, 6.0, 11.0, 18.0]$ |
| **skew** | Skew / Rotation | Hough Line Median Angle $|\theta|$ (deg) | `higher_is_worse` | $[0.5^\circ, 2.0^\circ, 4.0^\circ, 7.5^\circ]$ |
| **glare** | Glare / Specular | Saturated Connected Component Ratio $A_{\text{sat}} / A_{\text{tot}}$ | `higher_is_worse` | $[0.02, 0.06, 0.12, 0.22]$ |
| **contrast** | Contrast Loss | Normalized Dynamic Range $(p_{99.5} - p_{0.5}) / 255$ | `lower_is_worse` | $[0.70, 0.50, 0.30, 0.15]$ |
| **resolution** | Resolution Reduction | High-Frequency Sharp Edge Ratio $N_{|\nabla I| > 150} / N_{|\nabla I| > 30}$ | `lower_is_worse` | $[0.80, 0.65, 0.35, 0.05]$ |
| **compression** | JPEG Compression | 8x8 DCT Boundary Discontinuity Ratio $B_{\text{block}}$ | `higher_is_worse` | $[0.095, 0.110, 0.150, 0.200]$ |
| **illumination** | Illumination Attenuation | Global Mean Intensity $\mu_I$ | `lower_is_worse` | $[195.0, 145.0, 95.0, 50.0]$ |
| **occlusion** | Occlusion / Cutout | Low-Variance Mask Coverage Ratio $A_{\text{occ}} / A_{\text{tot}}$ | `higher_is_worse` | $[0.02, 0.075, 0.15, 0.25]$ |
| **perspective** | Perspective Distortion | Trapezoidal Inward Margin Convergence $|\theta_L + \theta_R|$ (deg) | `higher_is_worse` | $[2.5^\circ, 10.0^\circ, 25.0^\circ, 40.0^\circ]$ |

---

## 2. Detailed Algorithmic Specifications

### 1. Blur (Variance of Laplacian)
$$\text{Var}(\Delta I) = \frac{1}{N} \sum_{x,y} \left( \Delta I(x, y) - \overline{\Delta I} \right)^2$$
Where $\Delta I = I * L_3$, and $L_3$ is the discrete $3 \times 3$ Laplacian kernel.
- **Physical Interpretation**: Sharp vector font strokes yield extreme gradient second derivatives ($\text{Var} > 25,000$). Gaussian blur attenuates high spatial frequencies, dropping variance by orders of magnitude.
- **Diagnostics**: Tenengrad gradient energy $\sum (G_x^2 + G_y^2)$ is recorded in metadata.

### 2. Noise (Immerkaer Fast Noise Variance)
$$\hat{\sigma}_n = \sqrt{\frac{\pi}{2}} \frac{1}{6(W - 2)(H - 2)} \sum_{x=2}^{W-1} \sum_{y=2}^{H-1} |I * M_{x,y}|$$
Where Immerkaer's Laplacian mask is:
$$M = \begin{bmatrix} 1 & -2 & 1 \\ -2 & 4 & -2 \\ 1 & -2 & 1 \end{bmatrix}$$
- **Physical Interpretation**: Eliminates structural image content by filtering polynomial surface trends, isolating high-frequency zero-mean sensor noise.

### 3. Skew (Hough Line Transform)
Probabilistic Hough Transform detects line segments in edge-detected text rows.
$$\theta_{\text{skew}} = \text{median} \left( \left\{ \arctan \left( \frac{\Delta y_i}{\Delta x_i} \right) : |\theta_i| \le 45^\circ \right\} \right)$$
- **Physical Interpretation**: Captures angular misalignment during scanner document feed or off-axis handheld capture.

### 4. Glare (Saturated Connected Pixel Clustering)
Binary highlight threshold at intensity $\ge 250$, filtered via $3 \times 3$ morphological opening, followed by 8-connectivity connected component analysis:
$$\text{Glare} = \frac{\sum_{k: \text{Area}_k \ge 50} \text{Area}_k}{W \times H}$$
- **Physical Interpretation**: Separates natural white paper margins from concentrated specular washout hotspots where ink contrast is destroyed.

### 5. Contrast (Normalized Effective Dynamic Range)
$$\text{DR}_{\text{eff}} = \frac{p_{99.5}(I) - p_{0.5}(I)}{255.0}$$
- **Physical Interpretation**: Measures the tonal distance between the paper background substrate ($p_{99.5}$) and the darkest foreground text ink core ($p_{0.5}$). Scale-sensitive to photocopy fading and thermal degradation.

### 6. Resolution / Scale (High-Frequency Sharp Edge Ratio)
$$R_{\text{sharp}} = \frac{\sum \mathbb{I}(|\nabla I| > 150.0)}{\max \left( 1, \sum \mathbb{I}(|\nabla I| > 30.0) \right)}$$
- **Physical Interpretation**: Downsampling and subsequent upsampling replaces single-pixel step transitions with linear interpolation slopes, causing the sharp-to-soft edge ratio to plummet monotonically.

### 7. Compression (8x8 Block Boundary Discontinuity)
$$\text{Blockiness} = \frac{D_{\text{boundary}} - D_{\text{interior}}}{D_{\text{boundary}} + D_{\text{interior}} + \epsilon}$$
Where $D_{\text{boundary}}$ measures pixel absolute jumps across column and row multiples of 8, and $D_{\text{interior}}$ measures adjacent differences inside the 8x8 DCT grid.
- **Physical Interpretation**: Directly measures Discrete Cosine Transform quantization grid step discontinuities.

### 8. Illumination (Mean Intensity Attenuation)
$$\mu_I = \frac{1}{W \times H} \sum_{x,y} I(x, y)$$
Supplemented by spatial grid variance $\sigma_{\text{grid}}^2$ computed across a $4 \times 4$ spatial block partition.
- **Physical Interpretation**: Detects underexposure, vignetting, and low-light sensor capture.

### 9. Occlusion (Low-Variance Block Masking)
Detects contiguous dark/gray cutout regions via morphological block closing ($11 \times 11$) and connected component filtering:
$$\text{Occlusion} = \frac{A_{\text{masked\_patches}}}{W \times H}$$
- **Physical Interpretation**: Detects physical masking, redaction bars, paper cutouts, and corner fold occlusions.

### 10. Perspective (Trapezoidal Inward Margin Convergence)
Analyzes line segments with $|\theta| > 45^\circ$ across the left and right document halves:
$$\theta_{\text{conv}} = |\theta_{L,\text{tilt}} + \theta_{R,\text{tilt}}|$$
- **Physical Interpretation**: Measures vanishing-point convergence of opposing vertical page borders caused by off-axis camera pitch and roll.
