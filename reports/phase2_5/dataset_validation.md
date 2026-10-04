# PHASE 2.5 — DATASET INTEGRATION & ZERO-LEAKAGE VALIDATION

**Project**: Vision-Language Models for Intelligent Document Processing under Real-World Visual Degradation  
**Phase**: Phase 2.5 — Unlimited-OCR Integration & Scientific Validation  
**Execution Date**: 2026-10-04  
**Audit Status**: CONFIRMED  
**Zero-Leakage Compliance**: PASS (100%)

---

## 1. Target Datasets & Architecture Roles

Unlimited-OCR (B0-U) was evaluated for architectural compatibility across all 7 frozen benchmark datasets:

| Dataset Name | Domain / Modality | Context Horizon | Baseline Compatibility | Planned Evaluation Role |
| :--- | :--- | :--- | :--- | :--- |
| **DocVQA** | Diverse scanned industry documents | Single-page | **COMPATIBLE** | Primary Document VQA Benchmark |
| **FUNSD** | Scanned noisy bureaucratic forms | Single-page | **COMPATIBLE** | Form & Key-Value Extraction |
| **SROIE** | Scanned retail cash receipts | Single-page | **COMPATIBLE** | Dense Key Information Extraction |
| **CORD** | High-variance multi-receipt scans | Single-page | **COMPATIBLE** | Fine-Grained Entity Hierarchy |
| **MMLongBench-Doc** | Complex multi-page research reports | Long-document | **NATIVELY COMPATIBLE (R-SWA)** | Multi-Page Multimodal Reasoning |
| **LongDocURL** | Extreme-length multi-page documents | Long-document | **NATIVELY COMPATIBLE (R-SWA)** | Long-Horizon Document Parsing |
| **XL-DocBench** | Cross-domain multi-layout PDFs | Long-document | **NATIVELY COMPATIBLE (R-SWA)** | Cross-Domain Scaling Benchmark |

---

## 2. Long-Document Architectural Advantage

Unlimited-OCR's Reference Sliding Window Attention (R-SWA) mechanism is specifically designed to eliminate the linear KV-cache growth that prevents standard VLMs (like Qwen2.5-VL or InternVL) from processing 30+ page documents in a single forward pass.
This makes B0-U a particularly strong and relevant baseline for the long-document benchmarks (`MMLongBench-Doc`, `LongDocURL`, `XL-DocBench`).

---

## 3. Zero-Leakage & Split Integrity Enforcement (Section 37 & 42)

In strict accordance with the Zero-Leakage Invariant:
1. Unlimited-OCR was validated solely on validation (`val`) partition samples.
2. The split validation suite (`tests/test_splits.py`) confirms:
   - Zero overlap of document source IDs between partitions.
   - Zero cryptographic hash overlap between partitions.
   - All degraded variants strictly inherit the partition of their clean source document.
3. No prompt engineering, threshold tuning, or model adjustment was performed on test partitions.
