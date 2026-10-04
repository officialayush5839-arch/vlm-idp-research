# PHASE 2.5 — UNLIMITED-OCR SPATIAL GROUNDING & COORDINATE VALIDATION

**Project**: Vision-Language Models for Intelligent Document Processing under Real-World Visual Degradation  
**Phase**: Phase 2.5 — Unlimited-OCR Integration & Scientific Validation  
**Execution Date**: 2026-10-04  
**Audit Status**: CONFIRMED  
**Grounding Status**: SUPPORTED (Layout Element Level)

---

## 1. Coordinate Space Alignment

Unlimited-OCR natively generates spatial coordinates in the standard integer range:
$$x_1, y_1, x_2, y_2 \in [0, 1000] \subset \mathbb{Z}^4$$
where $(x_1, y_1)$ represents the top-left coordinate and $(x_2, y_2)$ represents the bottom-right coordinate.

This aligns directly with the canonical coordinate normalization space frozen in Phase 0 (`protocol/grounding_protocol.md`) and implemented in Phase 1 (`src/ingestion/coordinates.py`).

---

## 2. Reversibility & Denormalization to Pixel Space

Using `denormalize_coordinates(norm_bbox, page_width, page_height)`, predicted bounding boxes map cleanly back to original raster pixel coordinates:
$$x_{\text{pixel}} = \frac{x_{\text{norm}}}{1000} \times W, \quad y_{\text{pixel}} = \frac{y_{\text{norm}}}{1000} \times H$$

As demonstrated in `tests/test_unlimited_ocr_grounding.py`, the spatial conversion produces zero unbounded rounding drift and maintains geometric consistency.

---

## 3. Anti-Fabrication & No Fake Grounding Verification (Section 26)

In strict adherence to the project constitution:
1. When Unlimited-OCR runs with standard document transcription prompts that omit `<|grounding|>`, it outputs clean text/markdown without bounding boxes.
2. The system **DOES NOT** invent, interpolate, or guess bounding box positions.
3. Instead, the adapter assigns:
   $$\text{spatial\_evidence\_status} = \textbf{NOT\_AVAILABLE}$$
   $$\text{has\_spatial\_grounding} = \textbf{False}$$
4. Bounding boxes are only populated when the model explicitly outputs verified spatial tags.

---

## 4. Grounding Status & Research Value Finding (Section 28)

$$\textbf{Overall Grounding Compatibility: SUPPORTED (Coarse Element-Level)}$$

### Comparison with Proposed Architecture:
- **Unlimited-OCR Capability**: Successfully extracts block-level bounding boxes for titles, paragraphs, tables, and figures.
- **Scientific Limitation**: Unlike classical OCR (PaddleOCR/Tesseract), Unlimited-OCR does not provide dense word-level or token-level bounding boxes, nor does it provide confidence scores or uncertainty metrics for its spatial boundaries.
- **Research Significance**: This empirical limitation directly supports the necessity of our proposed system's contribution (multi-signal evidence grounding and uncertainty-calibrated IDP).
