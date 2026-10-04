# Degradation Protocol — Controlled Visual Corruption Grid

**Project Title**: Adaptive, Uncertainty-Aware and Evidence-Grounded Vision-Language Document Intelligence under Real-World Visual Degradation  
**Document Stage**: Phase 0 Research Protocol Freeze  
**Last Updated**: 2026-10-04  

---

## 1. Controlled Degradation Taxonomy

The degradation generator creates deterministic, parameterized visual corruptions spanning 9 distinct physical degradation families. Corruptions are modeled after real-world scanning, camera capture, and optical transmission artifacts.

```text
                                DEGRADATION SUITE
                                        |
     +-----------------+----------------+-----------------+-----------------+
     |                 |                |                 |                 |
  OPTICAL          SENSOR/NOISE    COMPRESSION/RES    GEOMETRIC        OCCLUSION
  - Blur           - Gaussian       - JPEG Artifacts  - Skew/Rotation  - Patch Masking
  - Illumination     Noise          - Downsampling    - Perspective    - Crop/Cutoff
```

---

## 2. Parameter Grid & Severity Levels

Every degradation family is parameterized across five severity levels ($s \in \{0, 1, 2, 3, 4\}$), where $s=0$ represents clean baseline input:

| Degradation Family | Mathematical / Algorithmic Formulation | Severity 0 (Clean) | Severity 1 (Mild) | Severity 2 (Moderate) | Severity 3 (Severe) | Severity 4 (Extreme) |
|:---|:---|:---:|:---:|:---:|:---:|:---:|
| **1. Gaussian Blur** | Convolution with 2D Gaussian kernel $G_\sigma(x, y)$; kernel size $k = 2\lceil 3\sigma \rceil + 1$ | $\sigma = 0.0$ | $\sigma = 1.0$ | $\sigma = 2.0$ | $\sigma = 4.0$ | $\sigma = 6.0$ |
| **2. JPEG Compression** | Discrete Cosine Transform quantization with standard libjpeg quality factor $Q$ | $Q = 100$ | $Q = 80$ | $Q = 50$ | $Q = 25$ | $Q = 10$ |
| **3. Gaussian Noise** | Additive Gaussian noise $I'(x, y) = \text{clip}(I(x, y) + \mathcal{N}(0, \sigma^2), 0, 255)$ | $\sigma = 0$ | $\sigma = 5$ | $\sigma = 15$ | $\sigma = 30$ | $\sigma = 50$ |
| **4. Skew / Rotation** | Affine rotation matrix $R(\theta)$ around image center with bilinear interpolation | $\theta = 0^\circ$ | $\theta = 1^\circ$ | $\theta = 3^\circ$ | $\theta = 5^\circ$ | $\theta = 10^\circ$ |
| **5. Illumination / Brightness** | Linear intensity attenuation $I'(x, y) = \alpha \cdot I(x, y)$ | $\alpha = 1.00$ | $\alpha = 0.75$ | $\alpha = 0.50$ | $\alpha = 0.30$ | $\alpha = 0.15$ |
| **6. Occlusion / Cutoff** | Random rectangular cutout masking with uniform gray/black mask ($A_{\text{occ}} / A_{\text{total}}$) | $0\%$ | $5\%$ | $10\%$ | $20\%$ | $30\%$ |
| **7. Resolution Reduction** | Downsample with area interpolation by factor $r$, then upsample back to original dimensions | $r = 1.00$ | $r = 0.75$ | $r = 0.50$ | $r = 0.25$ | $r = 0.15$ |
| **8. Perspective Distortion** | Projective 4-point homography matrix tilting image around vertical axis by angle $\phi$ | $\phi = 0^\circ$ | $\phi = 5^\circ$ | $\phi = 15^\circ$ | $\phi = 25^\circ$ | $\phi = 35^\circ$ |
| **9. Mixed Degradation** | Composite pipeline applying (Blur + Noise + JPEG + Skew) simultaneously | Clean | $s=1$ all | $s=2$ all | $s=3$ all | $s=4$ all |

---

## 3. Real vs. Synthetic Degradation Protocol

A crucial scientific rule is that **synthetic degradation must never be claimed as identical to real-world degradation**. 

To maintain scientific integrity:
1. **Synthetic Benchmark (DocVQA-Degraded)**: Measures controlled mathematical response curves across individual corruption dimensions ($x$-axis: severity $\sigma$, $y$-axis: accuracy $F_1$).
2. **Real-World Benchmark (FUNSD & Real Scans)**: Evaluates whether adaptive routing and uncertainty mechanisms calibrated on synthetic/clean validation data generalize to natural, unmodeled scan artifacts (thermal fading, paper folds, coffee stains, historical bleed-through).
3. **Domain Gap Ablation (A12)**: Explicitly reports performance deltas between clean, synthetically corrupted, and naturally degraded document variants.

---

## 4. Implementation Invariants

1. **Deterministic Seeding**: The degradation generator accepts an integer seed. Given the same image, degradation type, severity, and seed, the resulting image must produce an identical SHA-256 hash.
2. **Storage Separation**:
   - `data/raw/`: Original uncorrupted images (strictly read-only / immutable).
   - `data/degraded/`: Generated degraded variants stored with naming convention `{doc_id}_deg_{type}_sev{s}_seed{seed}.png`.
   - `data/manifests/`: JSON metadata recording exact parameters, bounding-box coordinate transformations, and checksums.
3. **Coordinate Preservation**: Transformations involving geometric changes (rotation $\theta$, perspective $\phi$, downsampling $r$) MUST compute the inverse coordinate transform matrix $T^{-1}$ and map ground-truth bounding boxes so that spatial grounding evaluations remain mathematically valid.
