# Dataset Protocol — Benchmark Selection and Curation Specification

**Project Title**: Adaptive, Uncertainty-Aware and Evidence-Grounded Vision-Language Document Intelligence under Real-World Visual Degradation  
**Document Stage**: Phase 0 Research Protocol Freeze  
**Last Updated**: 2026-10-04  

---

## 1. Overview & Dataset Taxonomy

To rigorously test our hypotheses (H1–H6) without benchmark bias or cherry-picking, the experimental protocol incorporates seven public benchmark datasets structured into distinct scientific roles:

```text
                               DATASET SUITE
                                     |
         +---------------------------+---------------------------+
         |                                                       |
   SHORT / SINGLE-PAGE                                   MULTI-PAGE / LONG-DOC
   (Forms, Receipts, Scans)                              (Reports, Books, Contracts)
         |                                                       |
   +-----+-----+                                           +-----+-----+
   |           |                                           |           |
DocVQA       FUNSD / SROIE / CORD                     MMLongBench-Doc  LongDocURL / XL-DocBench
(QA & BBox)  (Noisy Scans & Parsing)                  (Cross-Page QA)  (Evidence Grounding)
```

| Functional Role | Selected Datasets | Primary Research Justification |
|:---|:---|:---|
| **Primary QA & Extraction** | `DocVQA` | De-facto international standard for document visual question answering with spatial evidence ground truth. |
| **Noisy Scan Robustness** | `FUNSD`, `SROIE`, `CORD` | Native real-world scans containing historical paper noise, wrinkles, skew, and thermal print fading. |
| **Long-Document Multimodal** | `MMLongBench-Doc` | 135 long PDFs (avg 47.5 pages) testing cross-page multimodal reasoning and unanswerable hallucination checks. |
| **Spatial Grounding & Locating** | `LongDocURL`, `XL-DocBench` | Explicit human-verified evidence-grounded page and region coordinates for multi-page complex documents. |
| **External Generalization** | Held-out subsets across domains | Testing cross-domain transferability (H6) from commercial forms to technical and legal documents. |

---

## 2. Detailed Dataset Specifications

### A. DocVQA (Document Visual Question Answering)
*   **Document Domain**: Industry documents, letters, reports, tables from the UCSF Industry Documents Library.
*   **Scale**: 12,767 document images, 50,000 question-answer pairs.
*   **Page Structure**: Single-page documents (high visual complexity, varied layouts, stamps, handwritten signatures).
*   **Annotations**: Question strings, list of valid answer strings, ground-truth bounding box coordinates for answer locations.
*   **License & Availability**: Non-commercial academic research license (freely downloadable via RRC Portal).
*   **Role in Project**: Primary single-page extraction and spatial grounding benchmark (B0–B6, PROPOSED).
*   **Relevance to Gaps**:
    *   *Gap 1 (Uncertainty)*: Grounding-DocVQA subset provides ground truth for evaluating unsupported answers and calibration.
    *   *Gap 2 (Grounding)*: Bounding box annotations enable strict IoU and Region Recall@$K$ evaluation.
    *   *Gap 3 (Degradation)*: Source clean images will be injected with controlled degradation to measure accuracy drop curves.

---

### B. FUNSD (Form Understanding in Noisy Scanned Documents)
*   **Document Domain**: Historical, degraded scanned business and government forms (1980s–1990s).
*   **Scale**: 199 fully annotated scanned forms (31,485 words, 9,707 semantic entities, 5,304 relations).
*   **Page Structure**: Single-page noisy scans with real-world artifacts (skew, optical noise, low resolution, bleed-through).
*   **Annotations**: Word-level bounding boxes, transcribed text, semantic labels (header, question, answer, other), entity links.
*   **License & Availability**: Permissive open-access research license.
*   **Role in Project**: Baseline for real-world document noise without synthetic corruption.
*   **Relevance to Gaps**:
    *   *Gap 3 (Degradation)*: Serves as the primary real-world degraded anchor to validate the domain gap against synthetic noise (A12).
    *   *Gap 1 (Uncertainty)*: Real scanning noise induces natural OCR errors, testing selective abstention.

---

### C. SROIE & CORD (Receipts and Point-of-Sale Documents)
*   **Document Domain**: Retail receipts and point-of-sale invoices.
*   **Scale**:
    *   *SROIE*: 1,000 scanned receipts with 4 key entities (company, date, address, total).
    *   *CORD*: 1,000 Indonesian retail receipts with 30 fine-grained semantic categories.
*   **Page Structure**: Single-page narrow aspect-ratio images, thermal paper fading, folds, severe skew, and wrinkles.
*   **Annotations**: Word-level bounding boxes and key-value field extractions.
*   **License & Availability**: Open academic research benchmarks.
*   **Role in Project**: Robustness and field extraction under complex low-resolution layouts.

---

### D. MMLongBench-Doc
*   **Document Domain**: Multi-domain complex documents (academic papers, corporate annual reports, technical whitepapers, financial statements).
*   **Scale**: 135 long PDF documents averaging 47.5 pages (ranging from 12 to 105 pages), 1,091 expert-curated QA pairs.
*   **Page Structure**: Multi-page structured documents with dense tables, flowcharts, vector graphics, and multi-column text.
*   **Annotations**: Question, answer, source page index, and binary flag for unanswerable questions (21% of test questions).
*   **License & Availability**: MIT License (GitHub / Hugging Face).
*   **Role in Project**: Primary multi-page long-document reasoning and hallucination-detection benchmark (B3, B4, PROPOSED).
*   **Relevance to Gaps**:
    *   *Gap 2 (Long-Doc)*: Directly evaluates cross-page reasoning across 50+ page contexts.
    *   *Gap 1 (Uncertainty)*: Built-in unanswerable questions provide clean evaluation for safe abstention (`REVIEW_REQUIRED`).

---

### E. LongDocURL & XL-DocBench
*   **Document Domain**: Government filings, legal proceedings, financial prospectuses.
*   **Scale**:
    *   *LongDocURL*: 2,325 QA pairs spanning 33,000+ pages with explicit element locating tasks.
    *   *XL-DocBench*: 1,519 questions across extra-long documents (up to 2,303 pages, 72.6% multi-page dependencies).
*   **Page Structure**: Extra-long multimodal documents requiring dense retrieval.
*   **Annotations**: Ground-truth evidence page numbers and localized element coordinates.
*   **License & Availability**: Open research licenses on arXiv / Hugging Face.
*   **Role in Project**: Large-scale evidence retrieval and locating evaluation (Recall@$k$, Locating mAP).

---

## 3. Dataset Allocation Across Experimental Matrix

| Experiment Module | Selected Dataset(s) | Sample Split (Train / Val / Test) | Target Metrics |
|:---|:---|:---|:---|
| **Baseline Extraction (B0, B1, B2)** | DocVQA, FUNSD, SROIE | Official splits (or 70/15/15) | EM, F1, ANLS, CER, WER |
| **Degradation Robustness (Gap 3)** | DocVQA (Synthetic 9-grid) + FUNSD (Real) | Source test split only | Accuracy vs. Severity, Slope |
| **Adaptive Routing (Gap 3)** | DocVQA Degraded + FUNSD | Val (tune thresholds) / Test (frozen) | Route accuracy, Latency, F1 |
| **Multimodal Retrieval (Gap 2)** | MMLongBench-Doc, LongDocURL | Full document corpora | Page Recall@$k$ ($k=1,3,5,10$) |
| **Evidence Grounding (Gap 2)** | Grounding-DocVQA, LongDocURL | Val / Test splits | IoU, Region Recall@$K$, Provenance |
| **Uncertainty & Abstention (Gap 1)**| MMLongBench-Doc (unanswerable) + DocVQA | Val (calibrate) / Test (evaluate) | ECE, Brier, AURC, Selective F1 |
| **Cross-Dataset Generalization (H6)** | CORD, XL-DocBench | Zero-shot evaluation | EM, F1, Selective Accuracy |
