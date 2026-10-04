# PHASE 2.5 — UNLIMITED-OCR OUTPUT CHARACTERIZATION & SCHEMA ANALYSIS

**Project**: Vision-Language Models for Intelligent Document Processing under Real-World Visual Degradation  
**Phase**: Phase 2.5 — Unlimited-OCR Integration & Scientific Validation  
**Execution Date**: 2026-10-04  
**Audit Status**: CONFIRMED

---

## 1. Output Type Taxonomy (Section 21)

An empirical characterization was performed to identify what data modalities Unlimited-OCR natively emits:

| Data Type | Native Output Status | Description / Syntax in Unlimited-OCR |
| :--- | :--- | :--- |
| **Plain Text** | **PRESENT** | Full text body recovered sequentially. |
| **Markdown** | **PRESENT** | Emits `#`, `##`, `*`, list markers, and standard markdown headers. |
| **HTML** | **PARTIAL** | Emits HTML tags primarily for complex tables (`<table>`, `<tr>`, `<td>`). |
| **JSON** | **ABSENT** | Does not output structured JSON schema unless explicitly post-processed. |
| **Structured Elements**| **PRESENT** | Explicit layout tokens: `title`, `text`, `table`, `figure`, `header`, `footer`. |
| **Bounding Boxes** | **PRESENT** | When prompted with `<|grounding|>`, emits `[x1, y1, x2, y2]`. |
| **Layout Labels** | **PRESENT** | Prefixes every bounding box with category (e.g. `title [x1, y1, x2, y2]`). |
| **Tables** | **PRESENT** | Extracts Markdown and HTML table matrices. |
| **Form Fields** | **PARTIAL** | Extracts field key-value pairs as adjacent text layout elements. |
| **Reading Order** | **PRESENT** | Tokens are emitted sequentially according to document reading flow. |
| **Coordinates** | **PRESENT** | Integer coordinates natively normalized to `[0, 1000]` interval. |
| **Confidence Score** | **ABSENT** | Does not provide per-box or per-word calibrated confidence metrics. |
| **Page References** | **PRESENT** | Preserves page demarcations during multi-page processing. |

---

## 2. Raw vs Normalized Output Immutability (Section 24)

In accordance with strict provenance safeguards:
1. **Raw Output (`raw_output`)**:
   - Preserves the verbatim generation emitted by the model without alteration.
   - Example:
     ```text
     title [40, 40, 500, 90]INVOICE #INV-2024-001
     text [40, 100, 350, 140]Vendor: Acme Corporation
     text [40, 160, 250, 190]Date: 2024-05-12
     text [40, 220, 320, 260]Total Amount: $1,450.00
     ```
2. **Normalized Text (`normalized_text`)**:
   - Strips spatial tag prefixes to provide clean downstream reading text:
     ```text
     INVOICE #INV-2024-001
     Vendor: Acme Corporation
     Date: 2024-05-12
     Total Amount: $1,450.00
     ```
3. **Structured Elements Array (`structured_elements`)**:
   - Decomposes each tagged line into an individual dictionary capturing `element_id`, `element_type`, `normalized_bbox`, `raw_bbox`, and `text`.
