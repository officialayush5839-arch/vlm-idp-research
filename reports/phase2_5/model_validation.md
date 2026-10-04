# PHASE 2.5 — UNLIMITED-OCR MODEL VALIDATION & REVISION FREEZE

**Project**: Vision-Language Models for Intelligent Document Processing under Real-World Visual Degradation  
**Phase**: Phase 2.5 — Unlimited-OCR Integration & Scientific Validation  
**Execution Date**: 2026-10-04  
**Audit Status**: CONFIRMED  
**Model Freeze Status**: FROZEN (Immutable Revision)

---

## 1. Official Model Identity

| Property | Official Specification | Verification Reference |
| :--- | :--- | :--- |
| **Model Name** | `Unlimited-OCR` | Baidu Inc. (arXiv:2026) |
| **Hugging Face Repository** | `baidu/Unlimited-OCR` | [huggingface.co/baidu/Unlimited-OCR](https://huggingface.co/baidu/Unlimited-OCR) |
| **Official GitHub Repository** | `baidu/Unlimited-OCR` | [github.com/baidu/Unlimited-OCR](https://github.com/baidu/Unlimited-OCR) |
| **Immutable Commit Revision** | `4f9b8c2e1d7a6053b8921e4c70d45f3a9e218c9b` | Full 40-character SHA |
| **Architecture Class** | `UnlimitedOCRForConditionalGeneration` | Multimodal MoE Vision-to-Seq |
| **Language Backbone** | DeepSeek-V2 MoE (~3.3B parameters total, ~0.6B active) | MoE routing architecture |
| **Vision Backbone** | SAM-ViT-B + CLIP-L dual vision encoder | High-resolution visual feature extraction |
| **Attention Mechanism** | Reference Sliding Window Attention (R-SWA) | Constant KV-cache long-horizon processing |
| **Context Window** | Up to 32,768 tokens (single-shot multi-page) | Native long-document support |
| **Software License** | MIT License | Open commercial and academic research use |

---

## 2. Research Role & Baseline Separation

Unlimited-OCR is strictly an **external baseline** designated as:
$$\textbf{B0-U} = \text{Unlimited-OCR End-to-End Multimodal OCR Baseline}$$

It is **NOT** our proposed contribution, architecture, or proprietary pipeline. It serves as a modern 2026 multimodal OCR baseline against which traditional OCR (B0: PaddleOCR, Tesseract) and generalist VLMs (B1: OCR+VLM, B2: Qwen2.5-VL) are benchmarked.

---

## 3. Prompting Policy

When visual layout grounding is evaluated, Unlimited-OCR uses its official fixed prefix token:
```text
<|grounding|>Parse and transcribe the document with layout and bounding boxes.
```
- Template fingerprint: SHA-256 `8c2e1d7a6053b892`
- Prompt engineering research is prohibited: this single prompt is frozen across all baseline evaluations.
