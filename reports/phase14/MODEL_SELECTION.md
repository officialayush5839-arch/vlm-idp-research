# PHASE 14 MODEL SELECTION PROTOCOL

**Target Publication Standard:** IEEE Transactions on Pattern Analysis and Machine Intelligence (TPAMI) / IEEE Access  
**Investigation:** Physical CUDA VLM Enablement, Real INT4 Inference & Quantization Benchmark  

---

## 1. Selection Criteria & Governance

The primary multimodal architecture candidate for Phase 14 physical GPU benchmarking must satisfy:
1. **Open-Weight Availability:** Transparent public architecture with open weights.
2. **Vision-Language Modality:** Native visual encoder with autoregressive decoder for document understanding.
3. **High-Resolution Document Understanding:** Dynamic resolution or patch-level tokenization suitable for OCR and page-level layout reasoning.
4. **Reproducible Model Revision:** Cryptographically pinnable Hugging Face revision identifier.
5. **Practical Quantization Support:** Support for 4-bit and 8-bit weight compression via BitsAndBytes or AWQ backends.
6. **Permissive Research License:** Apache 2.0 or compatible research license.

---

## 2. Model Feasibility Ladder

To guarantee scientific rigor while preventing false claims:

### Tier 1: Target Primary Model (7B Class)
- **Model Identifier:** `Qwen/Qwen2.5-VL-7B-Instruct`
- **Architecture:** Qwen2.5-VL (7.6B total parameters; Vision Transformer + 28-layer Transformer Decoder)
- **Precision Modes:**
  - **Q0 (FP16/BF16):** ~15.2 GB weight footprint (Theoretical VRAM required: >16 GB).
    - *Expected behavior on 6GB RTX 3050:* Immediate Out-Of-Memory (OOM). Recorded as a legitimate physical negative control.
  - **Q1 (INT8):** ~7.9 GB weight footprint.
    - *Expected behavior on 6GB RTX 3050:* OOM during model load or activation allocation.
  - **Q2 (INT4 / NF4 / AWQ):** ~4.2 GB weight footprint.
    - *Physical Headroom:* 1.9 GB remaining on 6GB card for KV cache, patch embeddings, and CUDA driver context.

### Tier 2: Fallback Engineering Model (2B/3B Class)
- **Model Identifier:** `Qwen/Qwen2.5-VL-3B-Instruct` / `SmolVLM-500M-Instruct`
- **Role:** Explicitly documented as a **Fallback Engineering Experiment** if the 7B model exhausts physical allocator headroom or encounters Windows CUDA memory fragmentation.
- **Rule of Separation:** A successful Tier 2 run **never** proves Tier 1 (7B) feasibility. Results must be reported under separate explicit labels.

---

## 3. Quantization Backend Configuration

- **Backend:** `bitsandbytes` (4-bit NF4 / FP4 quantization with double quantization enabled).
- **Compute Dtype:** `torch.float16`.
- **Device Map:** `auto` with explicit GPU device targeting (`cuda:0`).
- **Fail-Closed Rule:** If GPU device mapping fails, fallback to CPU is **strictly blocked** from entering physical benchmark tables.
