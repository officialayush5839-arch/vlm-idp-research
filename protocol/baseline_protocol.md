# Baseline Protocol — Formal Specification of Comparative Baselines

**Project Title**: Adaptive, Uncertainty-Aware and Evidence-Grounded Vision-Language Document Intelligence under Real-World Visual Degradation  
**Document Stage**: Phase 0 Research Protocol Freeze  
**Last Updated**: 2026-10-04  

---

## 1. Overview of Experimental Baselines

To demonstrate that the proposed integrated system provides a genuine advance over existing paradigms, we benchmark against a rigorous hierarchy of seven distinct baseline architectures (B0–B6), ranging from classical OCR to fixed preprocessing pipelines and ungrounded VLMs.

```text
                                BASELINE HIERARCHY
                                        |
     +----------------------------------+----------------------------------+
     |                                                                     |
CLASSICAL / OCR PIPELINES                                          VLM-CENTRIC PIPELINES
- B0: OCR-Only                                                     - B2: VLM-Only
- B1: OCR + VLM                                                    - B3: VLM + Text RAG
                                                                   - B4: VLM + Multimodal Retrieval
                                                                   - B5: VLM + Spatial Grounding
                                                                   - B6: Fixed Preprocessing + VLM
                                        |
                                        v
                                 PROPOSED SYSTEM
                 (Quality Assessment + Adaptive Routing +
                  Multimodal Retrieval + Evidence Grounding +
                  Calibrated Uncertainty + Abstention)
```

---

## 2. Formal Baseline Specifications

### Baseline B0: OCR-Only (Classical Text Baseline)
*   **Purpose**: Measure information extraction performance achievable via traditional OCR without modern foundation model reasoning.
*   **Input**: Document image (PDF/PNG).
*   **Model**: PaddleOCR (Primary) and Tesseract (Classical comparison).
*   **Processing Pipeline**: Document Normalization $\to$ OCR Text Recognition $\to$ Heuristic Keyword/Regex Extraction.
*   **Parameters**: Standard PaddleOCR recognition model (`ch_PP-OCRv4` / `en_PP-OCRv4`), confidence threshold $\tau = 0.50$.
*   **Output**: Extracted text string and per-word bounding box coordinates.
*   **Metrics**: Character Error Rate (CER), Word Error Rate (WER), Exact Match (EM), F1 score.

---

### Baseline B1: OCR + VLM (Cascaded Text-Fed VLM)
*   **Purpose**: Test standard enterprise IDP architecture where an upstream OCR engine extracts text, and an LLM/VLM reasons strictly over the OCR transcript.
*   **Input**: Document image + OCR extracted text string.
*   **Model**: PaddleOCR + Qwen2.5-VL 7B (conditioned on OCR text prompt).
*   **Processing Pipeline**: Image $\to$ OCR Engine $\to$ Text Prompt Construction: `"Document Text: {ocr_text}\nQuestion: {query}"` $\to$ VLM Generation.
*   **Parameters**: Greedy decoding ($T=0.0$, top-$p=1.0$), max new tokens = 128.
*   **Output**: Generated textual answer.
*   **Metrics**: EM, F1, ANLS, OCR CER/WER correlation.

---

### Baseline B2: VLM-Only (Pure Direct Visual Reasoning)
*   **Purpose**: Evaluate the raw visual reasoning capacity of state-of-the-art VLMs when directly inspecting raw document pixels without external OCR, preprocessing, or retrieval.
*   **Input**: Document image + Query string.
*   **Model**: Qwen2.5-VL 7B (Primary) and InternVL 2.0 (Generalization).
*   **Processing Pipeline**: Raw Image + Prompt $\to$ Vision Transformer $\to$ Autoregressive Text Generation.
*   **Parameters**: Greedy decoding ($T=0.0$), dynamic resolution enabled.
*   **Output**: Generated textual answer (no grounding coordinates, no confidence).
*   **Metrics**: EM, F1, ANLS, Latency, VRAM usage.

---

### Baseline B3: VLM + Text RAG (Standard Text Retrieval)
*   **Purpose**: Evaluate the de-facto standard approach for long documents: chunking text via OCR, storing in a text vector store, and feeding top-$k$ text chunks to the VLM.
*   **Input**: Multi-page document PDF + Query string.
*   **Model**: PaddleOCR + BGE-large-en-v1.5 embeddings + FAISS (IndexFlatIP) + Qwen2.5-VL 7B.
*   **Processing Pipeline**: Multi-page PDF $\to$ Page OCR $\to$ Chunking (500 tokens, 100 token overlap) $\to$ FAISS retrieval ($k=5$) $\to$ VLM prompt with retrieved text chunks.
*   **Parameters**: $k \in \{1, 3, 5, 10\}$, inner product similarity.
*   **Output**: Generated answer based on retrieved text passages.
*   **Metrics**: Retrieval Recall@$k$, QA F1, ANLS, Context Truncation Rate.

---

### Baseline B4: VLM + Multimodal Retrieval (Visual Page Retrieval)
*   **Purpose**: Test whether retrieving full page images based on multimodal embeddings outperforms text-only RAG for complex layouts and tables.
*   **Input**: Multi-page document PDF + Query string.
*   **Model**: ColPali / BGE-Visual page embeddings + FAISS + Qwen2.5-VL 7B.
*   **Processing Pipeline**: PDF pages rendered to images $\to$ Multimodal page embeddings $\to$ FAISS top-$k$ page retrieval $\to$ VLM reasoning over retrieved page images.
*   **Parameters**: $k \in \{1, 3, 5\}$, page image resolution normalized to 1024px.
*   **Output**: Answer generated from retrieved page images.
*   **Metrics**: Page Recall@$k$, EM, F1, ANLS, GPU Memory per query.

---

### Baseline B5: VLM + Spatial Grounding (Visual Bounding Box Prompting)
*   **Purpose**: Measure whether enforcing spatial bounding-box output from the VLM improves answer faithfulness on single-page benchmarks.
*   **Input**: Document image + Query string prompting for explicit bounding box tokens.
*   **Model**: Qwen2.5-VL 7B (using native `<|box_start|>` coordinate tokens).
*   **Processing Pipeline**: Image + Grounding Prompt $\to$ VLM outputs Answer + Coordinate Tuple $(x_1, y_1, x_2, y_2)$.
*   **Parameters**: Coordinate normalization $[0, 1000]$, greedy decoding.
*   **Output**: Answer string + Bounding box coordinates.
*   **Metrics**: Grounding IoU, Region Recall@$K$, Unsupported Answer Rate.

---

### Baseline B6: Fixed Preprocessing + VLM (Heuristic Image Enhancement)
*   **Purpose**: Evaluate standard practice of applying image enhancement blindly to all documents prior to feeding them to a VLM.
*   **Input**: Document image + Query string.
*   **Model**: OpenCV standard enhancement pipeline (Bilateral Denoising + Otsu/Adaptive Thresholding + Deskewing) + Qwen2.5-VL 7B.
*   **Processing Pipeline**: Raw Image $\to$ Static Enhancement Pipeline $\to$ VLM Generation.
*   **Parameters**: Fixed bilateral filter ($\sigma_c=75, \sigma_s=75$), fixed Hough line deskew.
*   **Output**: Generated textual answer.
*   **Metrics**: EM, F1, ANLS, Compute overhead on clean vs degraded documents.

---

### Proposed System: Integrated Adaptive Document Intelligence
*   **Purpose**: Defend the primary thesis: dynamic degradation routing + multimodal retrieval + evidence grounding + multi-signal calibrated uncertainty provides the optimal Pareto frontier across accuracy, robustness, reliability, and efficiency.
*   **Input**: Document PDF / Image + Query string.
*   **Processing Pipeline**:
    1. *Quality Assessment*: Compute 9-factor quality vector $\vec{q}$ and overall score $\mathcal{Q}$.
    2. *Adaptive Routing*:
       - `CLEAN` ($\mathcal{Q} \ge \tau_{\text{clean}}$): Direct VLM inference.
       - `MODERATE` ($\tau_{\text{severe}} \le \mathcal{Q} < \tau_{\text{clean}}$): Targeted Enhancement $\to$ VLM inference.
       - `SEVERE` ($\mathcal{Q} < \tau_{\text{severe}}$): OCR Fallback $\to$ Dual Vision-Text Assisted VLM.
    3. *Multimodal Retrieval*: Hierarchical page and patch vector retrieval over long documents.
    4. *Evidence Grounding*: Trace answers to explicit page numbers, bounding boxes, and supporting text.
    5. *Uncertainty & Abstention*: Calibrated logistic/isotonic estimator maps multimodal signals to `VERIFIED`, `UNCERTAIN`, or `REVIEW_REQUIRED`.
*   **Output**: Complete JSON schema (`answer`, `confidence`, `status`, `evidence: [{page, bbox, text, score}]`).
*   **Metrics**: Comprehensive suite across extraction, calibration, selective prediction, robustness, and latency.
