# Phase-by-Phase Scientific Inventory (Phases 0 through 11)

**Audited Repository:** `vlm-idp-research`  
**Parent Commit:** `7ce760d7`  
**Date:** 2026-10-06  

---

## 1. Master Phase Matrix

| Phase | Objective | Hypothesis | Dataset | Baselines | Proposed Method | Main Metric | Best Result | Statistical Test | Result | Known Limitation |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **P0** | Protocol & Literature Freeze | — | — | B0–B6 | Integrated System | — | Complete specs | — | **CONFIRMED** | Literature-only; no experiments. |
| **P1** | Environment & Ingestion | — | Fixtures | — | Normalization | Throughput / CER | Clean parsing | — | **CONFIRMED** | Evaluated on local mock PDFs. |
| **P2** | Baseline OCR & VLM | — | Fixtures | B0, B1, B2 | Direct VLM | Exact Match / F1 | B2 EM=0.88 | — | **CONFIRMED** | CPU-only PyTorch; stubbed local weights. |
| **P2.5** | Unlimited-OCR Integration | — | Fixtures | B0-U vs B0 | Unlimited OCR | Character Recall | 100% fixture match | — | **CONFIRMED** | Validated on narrow test sample. |
| **P3** | Document Quality Scoring | RQ1 | Synthetic | Baseline Heuristic | 10-Feature Vector | Spearman $\rho$ | $\rho = -0.78$ vs noise | — | **CONFIRMED** | Handcrafted features; linear correlation. |
| **P4** | Controlled Degradation | H1 | 4 Datasets (Synthetic) | B0, B1, B2, B0-U | Severity Grids | ANLS vs Severity | Drop $= -41.2\%$ at Sev4 | Paired t-test | **SUPPORTED** | Synthetic degradation models only. |
| **P5** | Adaptive Routing (Historical) | H2 | DocVQA / SROIE | Fixed Best vs Rule | Rule-based Routing | Accuracy / Cost | Cost $\downarrow 42\%$ | Paired Bootstrap | *AUDIT PASS W/ CORRECTIONS* | Test-set threshold leakage detected in audit. |
| **P5.1** | Routing Correction & Revalidation | H2 | DocVQA / SROIE | Fixed Best, Oracle, Rule | Learned Logistic Router | Route Accuracy | Acc $= 0.742$ (vs 0.760 Fixed) | Paired Bootstrap ($B=10k$) | **NOT_SUPPORTED** | Under zero-leakage, routing did not beat Fixed Best. |
| **P6** | Long-Doc Multimodal Retrieval | H4 | 50 Multi-page docs | B6-0 to B6-5 | Hierarchical BM25+Dense | Recall@K, Token Reduction | Recall@5 $= 0.942$, Compute $\downarrow 84\%$ | Paired Bootstrap ($p=0.000$) | **SUPPORTED** | Small corpus (50 docs, 25 test). |
| **P7** | Evidence Grounding & Verification | H5 | 25 Test Docs | B7-0 to B7-5 | Spatial IoU + Semantic Gate | Grounding F1, IoU@0.5 | F1 $= 0.891$, IoU $= 0.72$ | Paired Bootstrap ($p=0.000$) | **SUPPORTED** | Synthetic bounding box fixtures. |
| **P8** | Uncertainty Calibration & Abstention | H6 | 25 Test Docs | A0 to A5 | Temperature + Isotonic | ECE, Brier, Selective Risk | Selective Acc $= 0.870$, ECE $= 0.116$ | Paired Bootstrap ($p=0.000$) | **SUPPORTED** | Tested on single in-domain partition. |
| **P9** | Reliability & Failure Diagnosis | H9 | 25 Test Docs | B9-0 to B9-5 | 8D Uncertainty + Policy | AURC, Selective Acc | Selective Acc $= 0.821$, AURC $= 0.110$ | Paired Bootstrap ($p=0.5008$) | **NOT_SUPPORTED** | Proposed AURC tied unconditional B9-0 on curve. |
| **P10** | Robustness & Distribution Shift | H10 | 5 Domains ($D_0$–$D_4$) | B10-0 to B10-4 | Multi-signal Shift Gating | Robustness Gap, Acc | In-domain $= 0.92$, $D_2=0.0$, $D_4=0.0$ | Paired Bootstrap ($p=1.000$) | **NOT_SUPPORTED** | 100% defensive abstention in $D_2/D_4$ caused 0 coverage. |
| **P10.5** | Safety-Preserving Recovery | H10.5 | 5 Domains ($D_0$–$D_4$) | B10.5-0 to B10.5-5 | Preprocessing + Retry | Safe Useful Coverage, URR | SUC $= 0.6720$ ($\Delta = +0.184$), URR $= 0.0547$ | Paired Bootstrap ($p=0.000$) | **NOT_SUPPORTED** | URR $= 0.0547 > 0.0500$ safety tolerance. |
| **P11** | Safety-Constrained & Human Loop | H11 | 5 Domains ($D_0$–$D_4$) | B11-0 to B11-6 | 7-Layer Gate + Human Review | URR, SUC, Escalation Rate | URR $= 0.0800$, SUC $= 0.3200$, Esc $= 0.60$ | Paired Bootstrap ($p=1.000$) | **NOT_SUPPORTED** | Automated coverage penalized by 60% escalation. |

---

## 2. Key Synthesis
Across 12 distinct phase boundaries:
- **3 Hypotheses Supported:** $H_1$ (Degradation Vulnerability), $H_4$ (Hierarchical Retrieval), $H_5$ (Evidence Grounding), $H_6$ (Uncertainty Trade-off).
- **5 Hypotheses Not Supported:** $H_2$ (Routing under zero-leakage), $H_9$ (AURC reduction), $H_{10}$ (Raw cross-domain accuracy under defensive abstention), $H_{10.5}$ (Safety-preserving recovery below 5% URR), $H_{11}$ (Safety-constrained recovery without human scoring).
- **Fundamental Pattern:** Whenever the research team introduced rigorous zero-leakage and strict safety constraints, hypotheses evaluated honestly failed, exposing critical trade-offs between autonomous coverage and verified safety.
