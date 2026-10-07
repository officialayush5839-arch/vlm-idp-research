# Phase 14 Evidence Grounding Report

## 1. Grounding Methodology

Evidence grounding is evaluated via spatial Intersection-over-Union (IoU) between the predicted evidence bounding box and the annotator-verified ground truth visual region in the source document image.

---

## 2. Grounding Precision by Condition (`table_09_grounding.csv`)

| Condition ID | Pipeline Configuration | Mean Bounding-Box IoU | Standard Deviation |
| :--- | :--- | :---: | :---: |
| **B14-A** | Full-Document VLM (Unpruned) | 0.4527 | 0.0581 |
| **B14-B** | Retrieval-Pruned VLM (Top-2 Pages) | 0.6477 | 0.0573 |
| **B14-C** | Retrieval + Grounded VLM | 0.7553 | 0.0401 |
| **B14-D** | Full Proposed Architecture | 0.7994 | 0.0457 |

---

## 3. Key Observations

1. **Unpruned Grounding Failure (B14-A)**: When presented with full 5-page context, spatial resolution is diluted over hundreds of patch tokens, yielding a poor average IoU of 0.4527.
2. **Retrieval-Induced Localization Gain (B14-B)**: Narrowing candidate visual space to top-2 pages improves localization IoU to 0.6477 (+0.1950 IoU).
3. **Explicit Grounding Enforcement (B14-C & B14-D)**: Explicit coordinate regression and patch cross-attention achieve high spatial fidelity (0.7553 in B14-C and 0.7994 in B14-D), enabling verified human auditability for automated document processing.
