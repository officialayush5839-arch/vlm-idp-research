# Document Classification & Adaptive Routing Architecture

This document provides a comprehensive technical guide to how document classification, quality assessment, degradation taxonomy, and adaptive routing operate within the **`vlm-idp-research`** framework.

---

## 1. Conceptual Overview: Quality-Driven Classification

In traditional document processing systems, document classification typically denotes categorizing documents into semantic classes (e.g., *Invoice*, *Receipt*, *Medical Form*, *Legal Agreement*).

While semantic understanding is vital, this research framework introduces a foundational paradigm: **Visual Integrity and Degradation-Aware Route Classification**.

Instead of treating every input image or PDF uniformly, the system inspects the visual and structural condition of the document to classify:
1. **The Nature and Severity of Visual Degradation** (Blur, noise, skew, compression, illumination).
2. **The Optimal Execution Route** (**CLEAN**, **MODERATE**, or **SEVERE**).
3. **The Inference Confidence and Risk of Hallucination** (**VERIFIED** vs. **ABSTAIN / REVIEW_REQUIRED**).

```
                      ┌──────────────────────────────────────┐
                      │            INPUT DOCUMENT            │
                      │       (PDF / Scanned Images)         │
                      └──────────────────┬───────────────────┘
                                         │
                                         ▼
                      ┌──────────────────────────────────────┐
                      │ 1. 10-Feature Quality Extraction     │
                      │    (Blur, Skew, Noise, Contrast,     │
                      │     Glare, Illumination, etc.)       │
                      └──────────────────┬───────────────────┘
                                         │
                                         ▼
                      ┌──────────────────────────────────────┐
                      │ 2. Degradation Severity              │
                      │    Classification Engine             │
                      │    (Laplacian, FFT, RMS Contrast)    │
                      └──────────────────┬───────────────────┘
                                         │
                 ┌───────────────────────┼───────────────────────┐
                 │                       │                       │
                 ▼                       ▼                       ▼
          [ CLEAN ROUTE ]        [ MODERATE ROUTE ]      [ SEVERE ROUTE ]
          Overall Score ≥ 0.70    0.35 ≤ Score < 0.70     Overall Score < 0.35
                 │                       │                       │
                 ▼                       ▼                       ▼
          Fast Direct VLM         Adaptive Restoration   Dual-OCR Fallback
          (Sub-second)            (Unsharp mask /        (PaddleOCR / Tesseract
                                   Wiener filter) + VLM   restoration) + VLM
                 │                       │                       │
                 └───────────────────────┼───────────────────────┘
                                         │
                                         ▼
                      ┌──────────────────────────────────────┐
                      │ 3. Calibrated Uncertainty & Gate     │
                      │    (Grounding Score + Quality Score) │
                      └──────────────────┬───────────────────┘
                                         │
                         ┌───────────────┴───────────────┐
                         ▼                               ▼
                 [ VERIFIED ANSWER ]            [ SAFE ABSTENTION ]
                 Confidence ≥ 0.60              Confidence < 0.60
                 Evidence BBox Locked           (REVIEW_REQUIRED)
```

---

## 2. The 10-Feature Visual Quality Taxonomy

Implemented in [`src/quality/pipeline.py`](src/quality/pipeline.py), every incoming document page is analyzed across 10 deterministic visual dimensions:

| # | Feature Name | Mathematical / Algorithmic Basis | Real-World Degradation Detected |
|---|---|---|---|
| 1 | **Blur** | Laplacian Variance & Modified Laplacian Operator ($\nabla^2 I$) | Out-of-focus capture, motion blur |
| 2 | **Noise** | High-frequency residual variance via Median Filtering | Camera sensor grain, thermal ISO noise |
| 3 | **Contrast** | Root-Mean-Square (RMS) pixel intensity variance | Faded receipts, poor photocopies |
| 4 | **Skew** | Radon transform & Hough Line angular peak detection | Angled mobile camera scans, page rotation |
| 5 | **Perspective**| Quadrilateral boundary contour vanishing points | Slanted mobile camera angles |
| 6 | **Illumination**| Local histogram illumination uniformity | Uneven room lighting, cast shadows |
| 7 | **Glare** | Specular saturation clustering ($>98\%$ luminance) | Flash reflection, glossy paper |
| 8 | **Occlusion** | Margin bounding box integrity & border clipping | Fingers, staples, clips obstructing text |
| 9 | **Resolution**| DPI assessment and effective character stroke width | Low-resolution fax or mobile captures |
| 10| **Compression**| 8x8 DCT boundary discontinuity detection | Heavy JPEG artifacts, re-compression blur |

---

## 3. Empirical Scoring and Degradation Classification

Each feature $f_i$ is mapped to a discrete severity label:
- **`CLEAN`**: No degradation present.
- **`MODERATE`**: Tolerable degradation; legible to humans but prone to token corruption.
- **`SEVERE`**: Critical degradation; standard Vision-Language Models will hallucinate.

An empirical composite quality score ($S \in [0.0, 1.0]$) is computed:
$$S = \max\left(0.10, 0.90 - \sum \text{penalty}(\text{severity}_i)\right)$$

Where:
- $\text{Severe Penalty} = 0.25$
- $\text{Moderate Penalty} = 0.15$
- $\text{Mild Penalty} = 0.08$

---

## 4. Tri-Pathway Adaptive Routing Policy

Managed by [`AdaptiveRouter`](src/routing/router.py) and [`RuleBasedQualityRouter`](src/routing/rule_engine.py), the document is dynamically classified into one of three execution pathways:

### Pathway 1: CLEAN Route ($S \ge 0.70$)
- **Profile**: High contrast, sharp text edges, no significant geometric skew.
- **Action**: Dispatches directly to the primary Vision-Language Model (`SmolVLM-500M INT4`).
- **Advantage**: Lowest latency, zero unnecessary preprocessing overhead.

### Pathway 2: MODERATE Route ($0.35 \le S < 0.70$)
- **Profile**: Moderate blur, low contrast, mild skew.
- **Action**: Preprocesses the document using:
  - Adaptive contrast normalization.
  - Unsharp masking ($r=2$, $130\%$).
  - Wiener deconvolution.
- **Advantage**: Restores token legibility before passing to the multimodal neural backbone.

### Pathway 3: SEVERE Route ($S < 0.35$)
- **Profile**: Extreme degradation, low legibility, or heavy compression.
- **Action**: Activates the Dual-OCR Fallback engine (`PaddleOCR` + `Tesseract` baseline) with morphological binarization.
- **Advantage**: Prevents catastrophic VLM visual hallucination on severely corrupted documents.

---

## 5. Uncertainty & Safe Abstention Classification

Following extraction, the answer and visual grounding undergo a final classification to decide whether the output should be presented as factual or rejected safely:

A calibrated confidence score is generated:
$$\text{Confidence} = 0.35 \times \text{QualityScore} + 0.65 \times \text{GroundingScore}$$

- **`VERIFIED`**: Confidence $\ge 0.60$ and spatial bounding boxes accurately verify the source region.
- **`ABSTAIN / REVIEW_REQUIRED`**: Triggered when visual evidence is absent, degraded below the reliability threshold, or ambiguous. The system refrains from answering and issues an explanation to human operators.
