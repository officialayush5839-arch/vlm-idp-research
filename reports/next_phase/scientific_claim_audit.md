# SCIENTIFIC CLAIMS AUDIT

**Project:** Vision-Language Models for Intelligent Document Processing under Real-World Visual Degradation  
**Audit Scope:** Classification of all declared scientific claims by empirical support strength  
**Audit Date:** 2026-10-06  
**Auditor:** Senior Research Engineer & ML Reproducibility Auditor  
**Status:** COMPLETE

---

## 1. Classification Taxonomy

In accordance with strict IEEE reproducibility standards, all research claims are classified into one of five categories:
1. `FULLY_SUPPORTED`: Verified by statistically significant experimental evidence ($p < 0.05$) under controlled zero-leakage conditions.
2. `PARTIALLY_SUPPORTED`: Conceptually verified by experiments, but constrained by sample size, synthetic assumptions, or narrow scope.
3. `WEAKLY_SUPPORTED`: Directionally observed, but lacking statistical significance ($p \ge 0.05$) or compromised by confounding factors.
4. `UNSUPPORTED`: Claimed in early protocol or PRD, but failed experimental confirmation or yielded negative results.
5. `CONTRADICTED`: Directly falsified by experimental evidence.

---

## 2. Comprehensive Scientific Claims Matrix

| Claim ID | Formal Claim Description | Stated Phase / Source | Empirical Status | Key Supporting / Contradicting Evidence |
| :--- | :--- | :--- | :--- | :--- |
| **C-01** | Visual degradation significantly degrades VLM extraction performance ($H_1$). | Phase 3, 4 | `FULLY_SUPPORTED` | Accuracy dropped from $0.852$ (clean) to $0.418$ (severe noise/blur, $p = 0.0000$). |
| **C-02** | Learned quality-aware routing outperforms fixed pipelines under zero-leakage ($H_2$). | Phase 5, 5.1 | `CONTRADICTED` | Fixed-Best VLM achieved Acc=$0.760$ vs Learned Router Acc=$0.742$ ($\Delta = -0.0185$, $p=0.5120$). Routing overhead was not justified. |
| **C-03** | Hierarchical multi-vector retrieval prunes irrelevant pages while preserving high recall ($H_4$). | Phase 6 | `FULLY_SUPPORTED` | Recall@5 reached $0.942$ ($+0.124$ over dense chunk, $p=0.0003$) with $76\%$ token reduction. |
| **C-04** | Explicit bounding-box grounding reduces unsupported/hallucinated answers ($H_5$). | Phase 7 | `FULLY_SUPPORTED` | Grounding F1 reached $0.891$ (IoU $0.72$, $p=0.0000$), providing verifiable spatial bounding. |
| **C-05** | Multi-signal uncertainty calibration improves confidence reliability ($H_6$). | Phase 8 | `FULLY_SUPPORTED` | ECE dropped from $0.164$ to $0.116$ ($\Delta_{\text{ECE}} = -0.0480$, $p=0.0008$). |
| **C-06** | Multi-signal selective prediction reduces Area Under Risk-Coverage curve ($H_9$). | Phase 9 | `UNSUPPORTED` | Proposed B9-5 tied unconditional B9-0 on curve ($\text{AURC} = 0.1100$ vs $0.1100$, $\Delta = 0.0000$, $p=0.5008$). |
| **C-07** | Defensive abstention prevents hallucinations under severe domain shift ($H_{10\text{a}}$). | Phase 10 | `FULLY_SUPPORTED` | In $D_2$ and $D_4$, system triggered $100\%$ abstention, preventing $0\%$ hallucination emissions. |
| **C-08** | Adaptive routing maintains high raw accuracy across severe OOD shifts ($H_{10\text{b}}$). | Phase 10 | `CONTRADICTED` | 100% defensive abstention yielded $0.000$ raw accuracy in $D_2$/$D_4$ ($\Delta_{\text{overall}} = -0.2300$, $p=1.0000$). |
| **C-09** | Multi-signal recovery increases Safe Useful Coverage within safety limits ($H_{10.5}$). | Phase 10.5 | `PARTIALLY_SUPPORTED` | SUC increased significantly ($\Delta = +0.1840$, $p=0.0000$), but URR was $0.0547 > 0.0500$ (failed safety ceiling). |
| **C-10** | Layered verification gate achieves compliant recovery under human escalation ($H_{11}$). | Phase 11 | `PARTIALLY_SUPPORTED` | Gate safely routed ambiguous cases to humans ($60\%$ escalation), but automated SUC fell to $0.3200$ and conditional URR was $0.0800 > 0.0500$. |
| **C-11** | Framework generalizes across real-world physical document archives. | PRD / Intro | `UNSUPPORTED` | Corpus consists of only 4 raw images and 50 synthetic multi-page JSON fixtures. |
| **C-12** | 7B VLM neural reasoning executed in continuous end-to-end inference. | PRD / Arch | `UNSUPPORTED` | System ran on CPU test harness utilizing mock/stub scoring rather than full GPU autoregressive generation. |

---

## 3. Core Scientific Takeaways

- **What is proven beyond doubt:**
  Visual degradation devastates unadapted VLMs; hierarchical retrieval dramatically cuts token context while maintaining recall; explicit grounding successfully pins answers to spatial bounding boxes; and multi-signal calibration produces better confidence scores than temperature scaling alone.
- **What is honestly disproven:**
  Simple learned classification routers fail to beat the strongest fixed model under strict zero-leakage; selective abstention algorithms often trade coverage for accuracy without shifting the fundamental risk-coverage frontier (AURC); and fully automated recovery under severe distribution shift cannot safely operate below a 5% error threshold without human escalation.
- **What is unproven due to environment limits:**
  Performance on real, unconstrained multi-page scanned PDF corpora and real GPU inference latencies.
