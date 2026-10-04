# VLM-IDP Technical Architecture

## 1. System Overview
**Project Title**: Adaptive, Uncertainty-Aware and Evidence-Grounded Vision-Language Document Intelligence under Real-World Visual Degradation

This document serves as the technical source of truth for the VLM-IDP project. The system is a research-grade Vision-Language Model Intelligent Document Processing (VLM-IDP) architecture designed to handle real-world visual degradation. It uniquely combines degradation assessment, adaptive routing, multimodal retrieval, evidence grounding, and uncertainty estimation to provide robust, traceable, and reliable document intelligence.

## 2. Architecture Principles
*   **Modularity**: Clear separation of concerns with distinct, decoupled modules.
*   **Configuration-driven**: No hard-coded parameters; all settings managed via YAML.
*   **Reproducibility-first**: Every run tracks git hashes, seeds, and configs.
*   **Fail-safe**: Never silently drop errors; graceful degradation and explicit logging.
*   **Provenance-tracked**: Data lineage from original to enhanced to output is strictly maintained.
*   **No hard-coded paths**: All file operations use robust path management based on project root.

## 3. High-Level Architecture

```text
                         INPUT DOCUMENT
                         PDF / IMAGE
                              |
                              v
                 +--------------------------+
                 | Document Normalization   |
                 | PDF rendering / pages    |
                 +------------+-------------+
                              |
                              v
                 +--------------------------+
                 | Quality & Degradation    |
                 | Assessment Module        |
                 +------------+-------------+
                              |
             +----------------+----------------+
             |                |                |
           CLEAN           MODERATE          SEVERE
             |                |                |
             v                v                v
         Direct VLM     Enhancement + VLM   OCR + VLM
             |                |                |
             +----------------+----------------+
                              |
                              v
                 +--------------------------+
                 | Multimodal Document      |
                 | Representation / Index   |
                 +------------+-------------+
                              |
                              v
                 +--------------------------+
                 | Multimodal Retrieval     |
                 | Pages + Regions + Text   |
                 +------------+-------------+
                              |
                              v
                 +--------------------------+
                 | VLM Reasoning Engine     |
                 | Extraction / QA / Math   |
                 +------------+-------------+
                              |
                              v
                 +--------------------------+
                 | Evidence Grounding       |
                 | Page + BBox + Content    |
                 +------------+-------------+
                              |
                              v
                 +--------------------------+
                 | Uncertainty Estimator    |
                 | Calibration + Risk       |
                 +------------+-------------+
                              |
                    +---------+---------+
                    |                   |
                    v                   v
             VERIFIED ANSWER       ABSTAIN / REVIEW
             + Evidence            + Reason
             + Confidence          + Evidence
```

## 4. Detailed Pipeline
1.  **Ingestion**: A PDF or image is ingested and normalized into standardized page images.
2.  **Quality Assessment**: Each page is analyzed for visual quality and specific degradations (blur, noise, etc.).
3.  **Adaptive Routing**: Based on the quality score, the page is routed to:
    *   Clean: Sent directly to the VLM.
    *   Moderate: Visually enhanced, then sent to the VLM.
    *   Severe: Processed with OCR, and the VLM is assisted by the OCR text.
4.  **Representation & Indexing**: Pages, text, and visual regions are embedded and stored in a vector index.
5.  **Retrieval**: For a given query, relevant pages, regions, and text chunks are retrieved.
6.  **Reasoning**: The VLM processes the retrieved multimodal context to generate an answer.
7.  **Grounding**: The answer is traced back to specific pages and bounding boxes in the original document.
8.  **Uncertainty Estimation**: System confidence is calculated combining VLM confidence, retrieval scores, and grounding quality.
9.  **Output Generation**: The final output is categorized as VERIFIED or flagged for ABSTAIN/REVIEW with full evidence provided.

## 5. Module Boundaries
The system is built as a set of decoupled Python packages under the `src/` directory. Each module has a specific responsibility and interacts with others through well-defined interfaces and data schemas.

## 6. Data Flow
`Document Ingestion` -> `Quality Assessment` -> `Adaptive Routing` -> `[Direct VLM | Enhancement+VLM | OCR+VLM]` -> `Multimodal Representation` -> `Retrieval` -> `Reasoning` -> `Evidence Grounding` -> `Uncertainty Estimation` -> `Output`.

## 7. Document Ingestion
*   **Source Directory**: `src/ingestion/`
*   **Purpose**: Standardize input documents into workable image formats.
*   **Input Schema**: File path to PDF or image file.
*   **Output Schema**: List of PIL Images (pages) + Metadata dict (num_pages, original_format).
*   **Responsibility**: PDF rendering, page extraction, image normalization.
*   **Dependencies**: `pdf2image`, `Pillow`.
*   **Failure Modes**: Corrupted PDF, unsupported image format, out-of-memory on massive PDFs.
*   **Evaluation Metrics**: Processing time per page, conversion success rate.

## 8. Quality Assessment
*   **Source Directory**: `src/quality/`
*   **Purpose**: Evaluate the visual quality of document pages.
*   **Input Schema**: PIL Image (page).
*   **Output Schema**: Quality vector `{blur: float, noise: float, glare: float, skew: float, occlusion: float, overall_quality: float}`.
*   **Responsibility**: Image quality scoring, overall quality aggregation.
*   **Dependencies**: `opencv-python`, `scikit-image`.
*   **Failure Modes**: Extreme images causing mathematical errors in variance calculation.
*   **Evaluation Metrics**: Correlation with human quality judgments (if available), processing latency.

## 9. Degradation Detection
*   **Source Directory**: Part of `src/quality/`
*   **Purpose**: Identify specific types and severity of image degradation.
*   **Input Schema**: PIL Image.
*   **Output Schema**: Dict of boolean/float flags and severity metrics for:
    *   `blur`: Gaussian / motion blur ($\sigma \in \{0, 1, 2, 4, 6\}$)
    *   `noise`: Gaussian noise ($\sigma \in \{0, 5, 15, 30, 50\}$)
    *   `illumination` / `brightness`: Attenuation levels ($100\%, 75\%, 50\%, 30\%$)
    *   `skew` / `rotation`: Angular deviation ($0^\circ, 1^\circ, 3^\circ, 5^\circ, 10^\circ$)
    *   `compression`: JPEG quality factor ($100, 80, 50, 25, 10$)
    *   `small_text`: Effective DPI / character size drop
    *   `crop_cutoff` / `occlusion`: Coverage masking ($0\%, 5\%, 10\%, 20\%, 30\%$)
    *   `glare`: Specular reflection and hotspot artifacts
    *   `resolution`: Downsampling scaling ($100\%, 75\%, 50\%, 25\%$)
    *   `perspective_distortion`: Off-axis projective tilt ($0^\circ, 5^\circ, 15^\circ, 25^\circ$)
    *   `mixed_degradation`: Composite corruption profiles
*   **Responsibility**: Classify degradation types and quantify severity accurately.
*   **Dependencies**: `opencv-python`.
*   **Failure Modes**: False positives on natural document features (e.g., classifying a watermark as noise).
*   **Evaluation Metrics**: Precision/Recall for each degradation class against an annotated dataset.

## 10. Enhancement
*   **Source Directory**: `src/enhancement/`
*   **Purpose**: Improve legibility of moderately degraded documents.
*   **Input Schema**: PIL Image + identified degradations.
*   **Output Schema**: Enhanced PIL Image + applied transformation logs.
*   **Responsibility**: Deskew, denoise, contrast normalization, perspective correction, resolution normalization. MUST NOT overwrite originals. Maintain `original/`, `enhanced/`, and `metadata/` separately.
*   **Dependencies**: `opencv-python`, `albumentations`.
*   **Failure Modes**: Over-enhancement leading to artifact generation (hallucinations).
*   **Evaluation Metrics**: Downstream OCR/VLM accuracy improvement on enhanced vs. original images.

## 11. OCR
*   **Source Directory**: `src/ocr/`
*   **Purpose**: Extract text from highly degraded images where VLMs struggle visually.
*   **Input Schema**: PIL Image.
*   **Output Schema**: List of dicts `{text, confidence, page_id, bounding_box, level (line/word)}`.
*   **Responsibility**: Text extraction, bounding box localization.
*   **Dependencies**: `paddleocr` (primary), `pytesseract` (baseline).
*   **Failure Modes**: Gibberish output on abstract images, very slow execution.
*   **Evaluation Metrics**: Character Error Rate (CER), Word Error Rate (WER).

## 12. VLM Engine
*   **Source Directory**: `src/vlm/`
*   **Purpose**: Primary reasoning and extraction engine.
*   **Input Schema**: PIL Image(s) + Text Prompt + (Optional OCR Text).
*   **Output Schema**: Raw text response.
*   **Responsibility**: Vision-language inference, prompt management, parameter control.
*   **Dependencies**: `transformers`, `torch`, `accelerate`.
*   **Failure Modes**: Out of Memory (OOM), empty responses, hallucinations.
*   **Evaluation Metrics**: Accuracy on benchmark QA/Extraction tasks.

## 13. Retrieval
*   **Source Directory**: `src/retrieval/`
*   **Purpose**: Find relevant information within long documents.
*   **Input Schema**: Query string + Document ID.
*   **Output Schema**: List of dicts `{document_id, page_id, region_id, bounding_box, chunk_id, text, embedding_id, retrieval_score}`.
*   **Responsibility**: Vector embeddings, FAISS indexing, similarity search (k=3,5,10).
*   **Dependencies**: `sentence-transformers` (BGE embeddings), `faiss-cpu`.
*   **Failure Modes**: Index corruption, out of memory for huge vector spaces.
*   **Evaluation Metrics**: Mean Reciprocal Rank (MRR), Recall@K.

## 14. Long-Document Processing
*   **Source Directory**: `src/retrieval/` (indexing and multi-page chunking) & `src/routing/` (orchestration flow)
*   **Purpose**: Handle documents exceeding VLM context limits.
*   **Pipeline**: Page extraction → page-level representation → text/OCR → visual representation → embedding/index → query → top-k page retrieval → region/chunk retrieval → VLM reasoning → evidence verification.
*   **Failure Modes**: Missing crucial context across chunk boundaries.
*   **Evaluation Metrics**: End-to-end accuracy on multi-page QA datasets.

## 15. Evidence Grounding
*   **Source Directory**: `src/grounding/`
*   **Purpose**: Link VLM answers back to source document pixels.
*   **Input Schema**: VLM Answer + Original Document.
*   **Output Schema**: JSON `{answer, confidence, status, evidence: [{page, bbox, text, score}]}`. Status is `REVIEW_REQUIRED` if grounding fails.
*   **Responsibility**: Bounding box alignment, text matching.
*   **Dependencies**: `difflib`, fuzzy matching libraries.
*   **Failure Modes**: Inability to locate paraphrased answers in source text.
*   **Evaluation Metrics**: Grounding precision/recall.

## 16. Uncertainty Estimation
*   **Source Directory**: `src/uncertainty/`
*   **Purpose**: Quantify system confidence in the generated answer.
*   **Input Schema**: Signals: VLM consistency, OCR confidence, retrieval score, grounding score, visual quality score.
*   **Output Schema**: Classification: `VERIFIED`, `UNCERTAIN`, or `REVIEW_REQUIRED`.
*   **Responsibility**: Calibration (Logistic/Isotonic Regression or Small MLP) using thresholds derived strictly from validation data.
*   **Dependencies**: `scikit-learn`.
*   **Failure Modes**: Overconfidence on incorrect answers.
*   **Evaluation Metrics**: Expected Calibration Error (ECE), Area Under the Risk-Coverage Curve (AURC).

## 17. Abstention
*   **Source Directory**: `src/uncertainty/` (specifically `src/uncertainty/abstention.py` review & routing trigger)
*   **Purpose**: Prevent confident failures.
*   **Input Schema**: Uncertainty status.
*   **Output Schema**: Abstention signal + reason + available partial evidence.
*   **Responsibility**: Halt the pipeline and flag for human review when uncertainty is too high.
*   **Input Schema**: Uncertainty status.
*   **Output Schema**: Abstention signal + reason + available partial evidence.
*   **Responsibility**: Halt the pipeline and flag for human review when uncertainty is too high.

## 18. Adaptive Routing
*   **Source Directory**: `src/routing/`
*   **Purpose**: Dynamically select the optimal processing path.
*   **Input Schema**: Quality score vector.
*   **Output Schema**: Routing decision (CLEAN, MODERATE, SEVERE).
*   **Responsibility**: Execute routing logic based on frozen thresholds learned from train/val data.
*   **Failure Modes**: Misrouting (e.g., sending a severely degraded image to Direct VLM).
*   **Evaluation Metrics**: Routing accuracy vs. oracle routing; downstream performance vs fixed pipelines.

## 19. Output Schema
Complete JSON output format:
```json
{
  "document_id": "doc_123",
  "query": "What is the total invoice amount?",
  "answer": "$1,250.00",
  "confidence": 0.92,
  "status": "VERIFIED",
  "evidence": [
    {
      "page": 1,
      "bbox": [100, 200, 300, 250],
      "text": "Total Due: $1,250.00",
      "score": 0.95
    }
  ],
  "routing_decision": "MODERATE",
  "quality_assessment": {
    "overall_quality": 0.6,
    "blur": 0.8
  },
  "metadata": {
    "processing_time_ms": 1500,
    "model_used": "Qwen2.5-VL-7B"
  }
}
```

## 20. Experiment Tracking
*   **Records Tracked**: experiment_id, timestamp, git_commit, model, model_version, dataset, dataset_version, dataset_split, seed, prompt_version, temperature, top_p, max_tokens, batch_size, hardware, software_environment, configuration, metrics, outputs, status.
*   **Format**: Machine-readable JSON/CSV/Parquet.

## 21. Storage Architecture
*   `data/raw/`: Original, unmodified datasets.
*   `data/degraded/`: Synthetically degraded datasets.
*   `data/splits/`: Train/val/test splits.
*   `data/manifests/`: Metadata and index files.
*   `experiments/`: Logs, outputs, and tracking data per run.
*   Strict separation between original and enhanced images.

## 22. API Architecture
Research demonstration API providing endpoints for:
1.  Document Upload
2.  Quality Assessment Status
3.  Route Selection Notification
4.  Extraction execution
5.  Evidence formulation
6.  Confidence scoring.

## 23. UI Architecture
Research demo layer presenting:
*   Document upload interface.
*   Display of original image.
*   Quality assessment scores.
*   Routing decision visualization.
*   Final answer and confidence score.
*   Evidence page highlight.
*   Evidence region highlight (bounding boxes).
*   Supporting text extraction.
*   Explicit `REVIEW_REQUIRED` visual state.

## 24. Model Interfaces
Unified, Abstract Base Classes (ABCs) for interchangeable components:
*   `BaseVLM`: Unified interface for Qwen, InternVL, etc.
*   `BaseOCR`: Unified interface for PaddleOCR, Tesseract.
*   `BaseEmbedding`: Unified interface for vector embeddings.

## 25. Configuration System
YAML configurations stored in `configs/`:
*   `models.yaml`
*   `datasets.yaml`
*   `degradation.yaml`
*   `routing.yaml`
*   `retrieval.yaml`
*   `uncertainty.yaml`
*   `experiments.yaml`
No parameters are hard-coded in the Python source.

## 26. Failure Handling
*   No silent failures; all exceptions caught and logged.
*   Graceful degradation mechanisms.
*   If VLM fails -> OCR fallback attempted.
*   If OCR fails -> Report explicit processing failure.
*   If retrieval returns empty -> Flag low-evidence / Abstain.

## 27. Reproducibility Architecture
*   Git commit hash logged in every experiment.
*   Centralized seed management for `numpy`, `torch`, `random`.
*   Configuration freezing (saving a copy of the exact YAML used with the output).
*   Environment capture (`requirements.txt` or `poetry.lock` hash).
*   Deterministic algorithms enforced where PyTorch/CUDA allows.

## 28. Security/Privacy
*   Local model inference only.
*   No cloud API calls (e.g., OpenAI, Anthropic) for the primary system.
*   Document data never leaves the local machine.

## 29. Scalability
*   Batch processing support in VLM and Embedding modules.
*   Memory-efficient page-by-page processing for long documents.
*   Support for model quantization (e.g., 4-bit/8-bit) for VRAM constraints (6GB RTX 3050).

## 30. Architecture Decision Records (ADRs)
A template is maintained in `docs/adr_template.md` to track major technical decisions, including:
*   Model selection rationale.
*   Calibration method choices.
*   Routing threshold decisions.
Each ADR requires context, alternatives considered, decision, and consequences.
