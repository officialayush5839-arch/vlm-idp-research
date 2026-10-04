# Claim Traceability Matrix — Paper Claims to Experimental Evidence

**Project Title**: Adaptive, Uncertainty-Aware and Evidence-Grounded Vision-Language Document Intelligence under Real-World Visual Degradation  
**Document Stage**: Phase 0 Research Protocol Freeze  
**Last Updated**: 2026-10-04  

---

## 1. Overview & Research Claim Governance

To prevent unsupported conclusions in the IEEE manuscript, every factual claim intended for the abstract, introduction, and conclusion must map bijectively to a formal hypothesis, a planned experiment, specific baselines, frozen metrics, designated ablations, and a multi-seed statistical significance test.

If an experiment fails to support a claim, the claim must be scientifically revised to `NOT_SUPPORTED` or `PARTIALLY_SUPPORTED`.

---

## 2. Claim-to-Experiment Mapping Matrix

### Claim 1: Vulnerability of Modern VLMs to Document Degradation
*   **Intended Paper Claim**: "State-of-the-art open-source Vision-Language Models suffer severe non-linear performance drops under common document corruptions, with optical blur and high-frequency noise causing up to 40% loss in extraction accuracy."
*   **Supported By Hypothesis**: **H1**
*   **Planned Experiment**: `EXP_ROB_001_DEGRADATION_CURVES`
*   **Evaluated Baselines**: Baseline B0 (OCR-Only), Baseline B2 (VLM-Only: Qwen2.5-VL 7B), Baseline B6 (Fixed Preprocessing + VLM).
*   **Datasets**: DocVQA-Degraded (9 corruption families $\times$ 5 severity levels).
*   **Metrics**: ANLS, Token F1, Character Error Rate (CER), Degradation Drop ($\Delta_{\text{deg}}$), Robustness Slope ($\beta_{\text{rob}}$).
*   **Designated Ablations**: Ablation A11 (Single degradation vs mixed composite degradation).
*   **Statistical Methodology**: 5 seeds ($S_5$), Repeated-Measures ANOVA and linear trend test ($p < 0.001$).
*   **Current Verification Status**: `DECLARED` (Planned for Phase 4 / Phase 9).

---

### Claim 2: Superiority of Degradation-Aware Adaptive Routing
*   **Intended Paper Claim**: "Dynamic degradation-aware routing significantly mitigates accuracy loss under corruption compared to static VLM pipelines, achieving a 12% improvement in degraded ANLS while reducing average latency by 35% relative to universal enhancement."
*   **Supported By Hypothesis**: **H2**
*   **Planned Experiment**: `EXP_ROUTE_001_ADAPTIVE_VS_FIXED`
*   **Evaluated Baselines**: Baseline B2 (VLM-Only), Baseline B6 (Fixed Preprocessing + VLM), Proposed Adaptive System.
*   **Datasets**: DocVQA-Degraded, FUNSD (real degraded scans).
*   **Metrics**: ANLS, F1, Average Latency (ms), Route Distribution (Clean / Moderate / Severe), Routing Accuracy vs. Oracle Routing.
*   **Designated Ablations**: Ablation A1 (Remove quality assessment), Ablation A2 (Remove adaptive routing), Ablation A3 (Remove OCR fallback), Ablation A8 (Fixed vs adaptive preprocessing).
*   **Statistical Methodology**: 5 seeds ($S_5$), Paired Bootstrap Resampling ($B=10,000$, $p < 0.01$), Cliff's delta effect size.
*   **Current Verification Status**: `DECLARED` (Planned for Phase 5 / Phase 9).

---

### Claim 3: Hallucination Reduction via Explicit Evidence Grounding
*   **Intended Paper Claim**: "Enforcing spatial evidence grounding anchors model generation directly in source pixels, reducing unsupported and hallucinated answers by over 60% in multi-page document regimes."
*   **Supported By Hypothesis**: **H3**
*   **Planned Experiment**: `EXP_GND_001_EVIDENCE_PROVENANCE`
*   **Evaluated Baselines**: Baseline B2 (Ungrounded VLM), Baseline B5 (VLM + Spatial Grounding Prompting), Proposed System.
*   **Datasets**: Grounding-DocVQA, MMLongBench-Doc (unanswerable questions), XL-DocBench.
*   **Metrics**: Unsupported Answer Rate (UAR), Grounding IoU@0.50, Region Recall@$K$, Hallucination-Free Accuracy.
*   **Designated Ablations**: Ablation A5 (Remove evidence grounding verification).
*   **Statistical Methodology**: 5 seeds ($S_5$), Paired Wilcoxon Signed-Rank Test ($p < 0.01$), Cohen's $d > 0.5$.
*   **Current Verification Status**: `DECLARED` (Planned for Phase 7 / Phase 9).

---

### Claim 4: Calibrated Uncertainty Enables Trustworthy Selective Abstention
*   **Intended Paper Claim**: "Multi-signal uncertainty estimation achieves superior calibration (ECE < 0.06) compared to raw model logits, allowing the system to selectively abstain from answering low-confidence queries and boosting effective accuracy on accepted documents to over 92% at 75% coverage."
*   **Supported By Hypothesis**: **H4**
*   **Planned Experiment**: `EXP_UNC_001_SELECTIVE_PREDICTION`
*   **Evaluated Baselines**: Raw VLM Softmax Confidence, Token Self-Consistency (B1), Proposed Multi-Signal Calibrated Estimator.
*   **Datasets**: MMLongBench-Doc, DocVQA, FUNSD.
*   **Metrics**: Expected Calibration Error (ECE), Brier Score, Area Under the Risk-Coverage Curve (AURC), Selective Accuracy, Coverage.
*   **Designated Ablations**: Ablation A6 (Remove calibration), Ablation A7 (Remove abstention).
*   **Statistical Methodology**: 5 seeds ($S_5$), Paired Bootstrap comparison of AURC, Reliability diagrams with 10 bins.
*   **Current Verification Status**: `DECLARED` (Planned for Phase 8 / Phase 9).

---

### Claim 5: Multimodal Cross-Page Evidence Retrieval Outperforms Text RAG
*   **Intended Paper Claim**: "Multimodal page and region retrieval recovers dispersed cross-page evidence more reliably than traditional text-based RAG, increasing Page Recall@3 by 18% on complex visual layouts and financial tables."
*   **Supported By Hypothesis**: **H4** & **RQ4**
*   **Planned Experiment**: `EXP_RET_001_MULTIMODAL_VS_TEXT`
*   **Evaluated Baselines**: Baseline B3 (VLM + Text RAG), Baseline B4 (VLM + Multimodal Retrieval), Proposed System.
*   **Datasets**: MMLongBench-Doc, LongDocURL.
*   **Metrics**: Page Recall@$k$ ($k \in \{1, 3, 5, 10\}$), Mean Reciprocal Rank (MRR), End-to-End QA F1.
*   **Designated Ablations**: Ablation A4 (Remove multimodal retrieval), Ablation A10 (Retrieval $k$ comparison).
*   **Statistical Methodology**: 5 seeds ($S_5$), Paired Bootstrap Resampling ($p < 0.01$).
*   **Current Verification Status**: `DECLARED` (Planned for Phase 6 / Phase 9).

---

### Claim 6: Cross-Domain Generalizability
*   **Intended Paper Claim**: "The proposed adaptive framework generalizes across document categories (financial prospectuses, historical forms, administrative receipts) without requiring dataset-specific prompt engineering or fine-tuning."
*   **Supported By Hypothesis**: **H6**
*   **Planned Experiment**: `EXP_GEN_001_CROSS_DOMAIN`
*   **Evaluated Baselines**: Proposed System evaluated zero-shot across distinct domains.
*   **Datasets**: SROIE, CORD, XL-DocBench, FUNSD.
*   **Metrics**: Macro-averaged F1, Cross-Domain Relative Gain ($\Delta F_1 / F_{1, \text{base}}$), Selective Accuracy Stability.
*   **Designated Ablations**: Ablation A9 (Model family comparison: Qwen2.5-VL vs. InternVL2).
*   **Statistical Methodology**: Two-Way ANOVA assessing domain $\times$ method interaction effect.
*   **Current Verification Status**: `DECLARED` (Planned for Phase 9).
