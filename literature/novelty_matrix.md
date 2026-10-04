# Novelty Matrix — Systematic Comparison with Prior Art

**Project Title**: Adaptive, Uncertainty-Aware and Evidence-Grounded Vision-Language Document Intelligence under Real-World Visual Degradation  
**Document Stage**: Phase 0 Research Protocol Freeze  
**Last Updated**: 2026-10-04  

---

## Comparison Matrix

The table below contrasts our proposed architecture against major published systems, recent research benchmarks, and baseline methodologies across all ten system dimensions.

| System / Method | VLM | OCR | Long Doc (>20p) | Multimodal Retrieval | Evidence Grounding | Uncertainty Est. | Calibrated Abstention | Degradation Robustness | Adaptive Routing | Cross-Dataset Eval |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **LayoutLMv3** (Huang et al., 2022) | NO | YES | NO | NO | PARTIAL | NO | NO | PARTIAL | NO | YES |
| **DocVQA Baseline** (Mathew et al., 2021) | NO | YES | NO | NO | NO | NO | NO | PARTIAL | NO | NO |
| **ColPali** (Faysse et al., 2024) | YES | NO | YES | YES | PARTIAL | NO | NO | PARTIAL | NO | YES |
| **MMLongBench-Doc** (Wang et al., 2024) | YES | PARTIAL | YES | PARTIAL | NO | PARTIAL | PARTIAL | NO | NO | YES |
| **LongDocURL** (Deng et al., 2025) | YES | PARTIAL | YES | PARTIAL | YES | NO | NO | NO | NO | YES |
| **XL-DocBench** (2026) | YES | NO | YES | PARTIAL | YES | NO | NO | NO | NO | YES |
| **ReCoVERR** (Gao et al., 2024) | YES | NO | NO | NO | NO | YES | YES | NO | NO | NO |
| **Variational VQA** (Bain et al., 2025) | YES | NO | NO | NO | NO | YES | YES | NO | NO | NO |
| **Consensus Entropy** (Chen et al., 2024) | YES | YES | NO | NO | NO | YES | NO | YES | NO | YES |
| **DocTr** (Zhao et al., 2022) | NO | PARTIAL | NO | NO | NO | NO | NO | YES | NO | PARTIAL |
| **Qwen2.5-VL 7B Native** (Bai et al., 2025) | YES | PARTIAL | PARTIAL | NO | YES | PARTIAL | NO | PARTIAL | NO | YES |
| ─────────────────────────────── | ─── | ─── | ─── | ─── | ─── | ─── | ─── | ─── | ─── | ─── |
| **B0: OCR-Only** | NO | YES | NO | NO | NO | NO | NO | PARTIAL | NO | YES |
| **B1: OCR + VLM** | YES | YES | NO | NO | NO | NO | NO | PARTIAL | NO | YES |
| **B2: VLM-Only** | YES | NO | NO | NO | NO | NO | NO | NO | NO | YES |
| **B3: VLM + Text RAG** | YES | YES | YES | NO | NO | NO | NO | NO | NO | YES |
| **B4: VLM + Multimodal Retrieval** | YES | PARTIAL | YES | YES | NO | NO | NO | NO | NO | YES |
| **B5: VLM + Spatial Grounding** | YES | NO | NO | NO | YES | NO | NO | NO | NO | YES |
| **B6: Fixed Preprocessing + VLM** | YES | NO | NO | NO | NO | NO | NO | YES | NO | YES |
| ═══════════════════════════════ | ═══ | ═══ | ═══ | ═══ | ═══ | ═══ | ═══ | ═══ | ═══ | ═══ |
| **PROPOSED SYSTEM** | **YES** | **YES** | **YES** | **YES** | **YES** | **YES** | **YES** | **YES** | **YES** | **YES** |

---

## Detailed Novelty Analysis

### 1. Distinctive Value Proposition
No prior system in the published literature simultaneously addresses:
1. **Dynamic degradation-aware routing** (assessing document corruption before committing computational resources),
2. **Multimodal cross-page evidence retrieval & fine-grained bounding-box grounding**, and
3. **Calibrated multi-signal uncertainty estimation enabling risk-controlled abstention**.

### 2. Analysis of Closest Prior Art

#### A. ColPali (Faysse et al., 2024) vs. Proposed
- *ColPali* advances multimodal retrieval via patch-level late interaction, but treats retrieval as an isolated task. It does not perform downstream document QA reasoning, does not provide spatial bounding-box provenance for generated textual answers, does not estimate predictive uncertainty, and does not dynamically adapt to image degradations like blur, skew, or occlusion.
- *Our differentiation*: We incorporate multimodal retrieval as an intermediate representation layer within an adaptive degradation pipeline, directly linking retrieval confidence and bounding-box overlap into an uncertainty estimator that triggers abstention when evidence is insufficient.

#### B. MMLongBench-Doc (Wang et al., 2024) & LongDocURL (Deng et al., 2025) vs. Proposed
- *MMLongBench-Doc* and *LongDocURL* provide crucial benchmark evaluations identifying that VLMs struggle with long-context visual documents and hallucinate on unanswerable questions. However, they are **evaluation benchmarks**, not mitigation architectures. They do not propose an adaptive system capable of routing around corruption, calibrating predictive confidence, or selectively abstaining with provenance.
- *Our differentiation*: We provide the end-to-end framework that actively solves these failure modes through quality assessment, adaptive pathway routing, and multi-signal calibrated abstention.

#### C. ReCoVERR (Gao et al., 2024) & Variational VQA (Bain et al., 2025) vs. Proposed
- These methods pioneer selective prediction and abstention in VLMs, but operate exclusively on single natural scene images (VQA-v2, GQA). They assume clean camera images without structured text, dense tables, multi-page context, or scan degradations.
- *Our differentiation*: We formulate selective prediction specifically for the document AI domain, where uncertainty is driven by physical document corruption, OCR error rates, retrieval gaps, and spatial misalignment.

#### D. Consensus Entropy (Chen et al., 2024) vs. Proposed
- *Consensus Entropy* evaluates text recognition consistency across multiple VLMs for degraded OCR, but requires multiple complete VLM passes per page, lacks an adaptive routing mechanism, does not scale to multi-page long documents, and does not ground answers to spatial bounding boxes.
- *Our differentiation*: Our quality assessment module is lightweight (classical CV features and feature statistics), avoiding redundant multi-model passes for clean documents while reserving heavy OCR and enhancement pathways strictly for degraded documents.
