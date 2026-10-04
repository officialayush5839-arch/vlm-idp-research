# Quality Subsystem Architecture Specification

**Project Title**: Adaptive, Uncertainty-Aware and Evidence-Grounded Vision-Language Document Intelligence under Real-World Visual Degradation  
**Phase**: Phase 3 — Document Quality / Degradation Assessment Module  
**Status**: COMPLETE / VALIDATED  
**Authoritative Scope**: Measurement layer strictly decoupled from downstream model selection or routing decisions.

---

## 1. Architectural Overview

The Phase 3 Quality Subsystem provides an independent, non-destructive, and deterministic measurement layer for document images. It quantifies intrinsic visual quality, extracts multi-dimensional low-level feature vectors, and detects visual degradations across the 9 protocol-defined corruption families.

```text
                           INPUT DOCUMENT
                           (PDF / Image)
                                 │
                                 ▼
                     ┌───────────────────────┐
                     │   Phase 1 Ingestion   │
                     │  (Render / Normalize) │
                     └───────────┬───────────┘
                                 │
                                 ▼
                         Page Image (PIL)
                                 │
                                 ▼
                     ┌───────────────────────┐
                     │ Quality Preprocessor  │
                     │  (Format, Color, L)   │
                     └───────────┬───────────┘
                                 │
                                 ▼
                     ┌───────────────────────┐
                     │ Multi-Feature Engine  │
                     │  (10 Pure Extractors) │
                     └───────────┬───────────┘
                                 │
        ┌──────────────┬─────────┼─────────┬──────────────┐
        ▼              ▼         ▼         ▼              ▼
      Blur           Noise     Skew    Contrast       Occlusion
   (Laplacian)    (Immerkaer) (Hough) (DynamicRange) (CutoutMask)
        ▼              ▼         ▼         ▼              ▼
   Compression    Illum/Attn   Scale     Glare        Perspective
   (Blockiness)   (SpatialVar)(Sobel)   (Saturate)   (Trapezoid)
        └──────────────┴─────────┼─────────┴──────────────┘
                                 │
                                 ▼
                     ┌───────────────────────┐
                     │ Quality Feature Vector│
                     │   (10 Typed Results)  │
                     └───────────┬───────────┘
                                 │
                                 ▼
                     ┌───────────────────────┐
                     │ Degradation Detector  │
                     │ (Threshold & Severity)│
                     └───────────┬───────────┘
                                 │
                                 ▼
                     ┌───────────────────────┐
                     │  Page Quality Report  │
                     │ (S0-S4 Detections)    │
                     └───────────┬───────────┘
                                 │
                                 ▼
                     ┌───────────────────────┐
                     │ Multi-Page Aggregator │
                     │ (Descriptive Stats)   │
                     └───────────┬───────────┘
                                 │
                                 ▼
                      Document Quality Report
```

---

## 2. Component Design & Modularity

The subsystem is implemented under `src/quality/` with strict modular isolation:

1. **`schema.py`**:
   - `FeatureStatus`: `MEASURED`, `NOT_AVAILABLE`, `INVALID_INPUT`, `FAILED`, `NOT_APPLICABLE`.
   - `SeverityLevel`: Discrete scale $S_0$ (Clean), $S_1$ (Mild), $S_2$ (Moderate), $S_3$ (Severe), $S_4$ (Extreme).
   - `FeatureResult`: Typed record capturing raw metric, normalized $[0, 1]$ value, assigned severity, polarity direction, and diagnostic metadata.
   - `DegradationDetection`: Identifies active degradation family, mapped severity level, supporting evidence feature, and threshold delta.
   - `PageQualityAssessment`: Single-page report with runtime breakdown, algorithm version, configuration hash, and ISO-8601 UTC timestamp.
   - `DocumentQualityAssessment`: Preserves complete page-level fidelity while computing multi-page descriptive statistics (mean, median, min, max, std) and identifying the worst page.

2. **`preprocessing.py`**:
   - Accepts PIL Image, numpy array, or file path.
   - Composites alpha channels onto neutral paper white `(255, 255, 255)` rather than dropping transparency or producing black backgrounds.
   - Generates standardized RGB and Grayscale representations.
   - Non-destructive: source image arrays are never modified in-place.

3. **Feature Extractors** (`blur.py`, `noise.py`, `skew.py`, `glare.py`, `contrast.py`, `resolution.py`, `compression.py`, `illumination.py`, `occlusion.py`, `perspective.py`):
   - Pure functions taking 2D Grayscale array and configuration parameters.
   - Encapsulated error handling: internal mathematical errors return `FeatureStatus.FAILED` without halting remaining extractors.

4. **`detector.py`**:
   - Compares measured feature metrics against frozen severity cutoffs in `configs/phase3/severity_config.yaml`.
   - Emits detections only for severity $\ge 1$ ($S_1$ to $S_4$).
   - Flags composite multi-family degradation (`mixed_degradation`) when $\ge 3$ independent corruptions co-occur.

5. **`pipeline.py` (`DocumentQualityPipeline`)**:
   - Master facade coordinating preprocessor, extractors, detector, and aggregator.
   - Tracks sub-millisecond execution times (`RuntimeBreakdown`).
   - Injects cryptographic configuration SHA-256 hash.

---

## 3. Strict Boundary Invariants

- **No Downstream Feedback Loop**: Zero calls to OCR (`PaddleOCR`, `Tesseract`) or VLMs (`Qwen2.5-VL`, `Unlimited-OCR`).
- **No Model Selection or Routing**: The subsystem outputs only visual measurement features and degradation severities. Model routing logic belongs exclusively to Phase 5.
- **No Calibration or Abstention Logic**: Abstention, selective classification, and confidence calibration belong exclusively to Phase 8.
- **No Ground-Truth Label Inspection**: Operates blindly on input image pixels without access to synthetic degradation labels, split identifiers, or task annotations.
