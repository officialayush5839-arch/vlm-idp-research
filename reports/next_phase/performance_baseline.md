# Current Quantitative Performance Baseline

**Audited Repository:** `vlm-idp-research`  
**Date:** 2026-10-06  
**Auditor:** Senior Research Engineer & ML Reproducibility Reviewer  

---

## 1. Document Understanding & Extraction
- **In-Domain Clean Extraction ($D_0$):**
  - Selective Accuracy: **92.00%**
  - Coverage: **100.00%**
  - Exact Match / Normalized Score: **0.9200**
- **Degraded Extraction Collapse ($D_2$ Unconditional):**
  - Unconditional Accuracy: **40.00%** (Drop of $-52.00$ percentage points from clean)
  - Unsupported Error Rate: **60.00%**
- **Combined Stress Collapse ($D_4$ Unconditional):**
  - Unconditional Accuracy: **52.00%**
  - Unsupported Error Rate: **48.00%**

---

## 2. Retrieval Subsystem (Phase 6 Findings)
- **Top-K Retrieval Recall:**
  - Recall@1: **0.7840**
  - Recall@3: **0.8920**
  - Recall@5: **0.9420**
  - Recall@10: **0.9680**
- **Mean Reciprocal Rank (MRR):** **0.8340**
- **Normalized Discounted Cumulative Gain (nDCG@5):** **0.8710**
- **Evidence-Region Recall:** **0.8120**
- **Token Reduction / Computational Efficiency:** **72.2% to 94.0%** reduction in input tokens passed to the VLM reasoning engine compared to feeding complete un-indexed multi-page documents.

---

## 3. Evidence Grounding Subsystem (Phase 7 Findings)
- **Spatial IoU Metrics:**
  - Mean Bounding Box IoU: **0.7240**
  - Region Recall @ IoU $\ge 0.50$: **0.8400**
  - Region Recall @ IoU $\ge 0.75$: **0.6280**
- **Citation Integrity & Verification:**
  - Precision: **0.9120**
  - Recall: **0.8710**
  - Grounding F1: **0.8911**
  - Evidence Sufficiency Pass Rate: **0.8540**

---

## 4. Uncertainty & Reliability Subsystem (Phases 8 & 9 Findings)
- **Calibration Metrics (Post-Hoc Isotonic / Temperature):**
  - Expected Calibration Error (ECE): **0.1159** (Uncalibrated: $0.1736$)
  - Brier Score: **0.0892**
- **Selective Prediction Metrics:**
  - Selective Accuracy (at 80% coverage): **87.00%** (Unconditional: $72.00\%$)
  - Area Under Risk-Coverage Curve (AURC): **0.1100**
  - Excessive AURC (E-AURC): **0.0447**
- **Abstention Decision Quality:**
  - Abstention Precision: **0.8240**
  - Abstention Recall: **0.7610**
  - Abstention F1: **0.7912**

---

## 5. Robustness Across Distribution Shifts (Phases 10, 10.5, 11)

| Domain | Characteristic | Unconditional Acc ($B10\text{-}0$) | Phase 10 Gated ($B10\text{-}4$) | Phase 10.5 Recovered ($B10.5\text{-}5$) | Phase 11 Safe Gated ($B11\text{-}6$) |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **$D_0$** | In-Domain Clean | 92.00% | 92.00% (Cov 1.00) | 92.00% (Cov 1.00, URR 0.08) | 92.00% (Cov 1.00, URR 0.08) |
| **$D_1$** | Layout Shift (Dense Tabular) | 84.00% | 84.00% (Cov 1.00) | 84.00% (Cov 1.00, URR 0.16) | 0.00% (Escalated 100%) |
| **$D_2$** | Severe Visual Blur / Noise | 40.00% | 0.00% (Abstain 100%) | 40.00% (Cov 1.00, URR 0.60) | 0.00% (Escalated 100%) |
| **$D_3$** | Structure Shift (Forms) | 68.00% | 68.00% (Cov 1.00) | 68.00% (Cov 1.00, URR 0.32) | 68.00% (Cov 1.00, URR 0.32) |
| **$D_4$** | Combined Multimodal Stress | 52.00% | 0.00% (Abstain 100%) | 52.00% (Cov 1.00, URR 0.48) | 0.00% (Escalated 100%) |
| **Overall** | **Mean SUC / URR** | **0.6720 / 0.3280** | **0.4880 / 0.0240** | **0.6720 / 0.0547** | **0.3200 / 0.0800** |

---

## 6. Computational Efficiency Baseline
- **Execution Profile per Sample (CPU benchmark):**
  - Document Normalization & Parsing: **~35 ms**
  - Feature Quality Extraction (10-D): **~12 ms**
  - BM25 + Dense BGE Retrieval: **~18 ms**
  - Evidence Verification & 7-Layer Gate: **~8 ms**
  - Total Overhead excluding VLM generation: **< 75 ms**
- **VLM Call Reduction:**
  - Filtering multi-page documents to top-1/top-2 pages eliminates an average of **76% of downstream image tokens**, fitting comfortably within consumer hardware memory constraints (e.g. RTX 3050 6GB).
