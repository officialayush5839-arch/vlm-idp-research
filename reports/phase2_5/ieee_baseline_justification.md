# IEEE BASELINE JUSTIFICATION — UNLIMITED-OCR (B0-U)

**Project**: Vision-Language Models for Intelligent Document Processing under Real-World Visual Degradation  
**Phase**: Phase 2.5 — Unlimited-OCR Integration & Scientific Validation  
**Execution Date**: 2026-10-04  
**Audit Status**: CONFIRMED

---

## 1. IEEE Scientific Value & Context

In document intelligence research submitted to IEEE transactions and conferences, reviewers expect rigorous comparisons not only against classical two-stage OCR pipelines (e.g. PaddleOCR, Tesseract) and general-purpose Vision-Language Models (e.g. Qwen2.5-VL), but also against state-of-the-art **end-to-end multimodal OCR architectures**.

Released by Baidu in June 2026, **Unlimited-OCR** represents the state-of-the-art in long-horizon multimodal document parsing:
- **Reference Sliding Window Attention (R-SWA)**: Resolves the linear KV-cache bottleneck that limits general VLMs.
- **Visual Grounding Capability**: Directly generates bounding box coordinates in a normalized $[0, 1000]$ format when prompted with `<|grounding|>`.
- **Open Reproducibility**: Released under an open MIT license with public weights on Hugging Face (`baidu/Unlimited-OCR`).

Including Unlimited-OCR directly strengthens our IEEE manuscript by ensuring that our proposed adaptive framework is benchmarked against the latest paradigm in multimodal document understanding.

---

## 2. Formal Baseline Inclusion Decision (Section 44 & 45)

$$\textbf{Baseline Classification: FORMAL\_BASELINE}$$
$$\textbf{Assigned Identifier: B0-U}$$
$$\textbf{Formal Title: Unlimited-OCR End-to-End Multimodal OCR Baseline}$$

### Rationale:
1. **Model Execution Validated**: Successfully integrated into the research codebase with dedicated loader, processor, parser, and adapter under `src/baselines/unlimited_ocr/`.
2. **Output Standardization Validated**: Emitted spatial layout tags and text are transformed cleanly into our canonical `[0, 1000]` coordinate schema.
3. **Reproducibility Validated**: 100% exact match repeatability confirmed in `E2_5-REPRO-B0_U`.
4. **Hardware Feasibility Confirmed**: Validated under Category B (4-bit quantization on 6GB VRAM) and Category D (CPU execution).

---

## 3. Clear Demarcation from Proposed Novelty

Including B0-U as an external baseline highlights our paper's core contributions:
- **What B0-U Provides**: Coarse layout parsing, multi-page constant-memory text extraction, element bounding boxes.
- **What B0-U Lacks**:
  1. *Degradation Adaptability*: Does not detect visual degradation or dynamically adjust processing routes.
  2. *Calibrated Uncertainty*: Does not estimate token or document-level confidence.
  3. *Selective Prediction / Abstention*: Cannot abstain or flag `REVIEW_REQUIRED` when visual evidence is corrupted or ambiguous.
  4. *Fine-Grained Evidence Grounding*: Lacks verified word/token-level grounding and multi-signal evidence verification.

Thus, B0-U serves as an ideal external baseline to demonstrate that **high-capacity multimodal OCR alone cannot solve reliable, uncertainty-aware document processing under visual degradation**.
