# CROSS-PHASE CONSISTENCY AUDIT

**Project:** Vision-Language Models for Intelligent Document Processing under Real-World Visual Degradation  
**Audit Scope:** Longitudinal integrity and methodological consistency across Phase 0 through Phase 11  
**Audit Date:** 2026-10-06  
**Auditor:** Senior Research Engineer & ML Reproducibility Auditor  
**Status:** COMPLETE (High-Severity Methodological Bottlenecks Identified)

---

## 1. Executive Summary

This cross-phase consistency audit tracks the methodological evolution, dataset partitioning, metric definitions, and baseline mechanics across all completed project phases (Phases 0 through 11).

### Key Audit Findings:
1. **Critical Dataset Scale Bottleneck:** The multi-page long-document pipeline (Phases 6–11) rests on a corpus of only **50 total synthetic/fixture documents**, with precisely **25 test documents** partitioned across 5 evaluation domains ($D_0$ through $D_4$, yielding **5 documents per domain**). Downstream benchmarks (625 runs in P10, 750 in P10.5, 875 in P11) repeatedly re-evaluate these exact 25 documents across 5 random seeds.
2. **Metric Definition Evolution:** Metrics evolved logically from retrieval Recall@K and grounding IoU (Phases 6–7) to calibration ECE and selective accuracy (Phases 8–9), culminating in Safe Useful Coverage (SUC) and Unsafe Recovery Rate (URR) in Phases 10.5 and 11. However, threshold cutoffs shifted between phases without global standardization.
3. **Partition Integrity & Seed Consistency:** Random seeds (`42, 123, 456, 789, 101112`) were strictly standardized from Phase 8 through Phase 11. No cross-split data leakage was observed; test documents remained segregated in test across all phases.
4. **VLM Execution Mode Symmetry:** All evaluation phases operated under identical execution modes (Python 3.14 CPU mock/stub inference simulating Qwen2.5-VL and BGE representations), preserving relative internal validity while lacking GPU-based continuous token generation.

---

## 2. Dataset & Partition Consistency Matrix

| Phase | Document Corpus | Total Docs | Train Split | Val Split | Test Split | Test Queries / Samples | Seeds Used |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Phase 0–4** | Single-page (DocVQA, FUNSD, SROIE) | 4 images | 0 | 0 | 4 | Variable (12–108 synthetic variants) | 42 |
| **Phase 5** | DocVQA / FUNSD / SROIE splits | 30 | 12 | 6 | 12 | 108 synthetic variants | 42 |
| **Phase 5.1** | Corrected zero-leakage splits | 30 | 12 | 6 | 12 | 108 synthetic variants | 42, 123 |
| **Phase 6** | Multi-page corpus manifest | 50 | 10 | 15 | 25 | 75 queries (3 queries / test doc) | 42 |
| **Phase 7** | Multi-page corpus manifest | 50 | 10 | 15 | 25 | 125 runs (25 test docs × 5 conditions) | 42 |
| **Phase 8** | Multi-page corpus manifest | 50 | 10 | 15 | 25 | 125 runs (25 test docs × 5 seeds) | 42, 123, 456, 789, 101112 |
| **Phase 9** | Multi-page corpus manifest | 50 | 10 | 15 | 25 | 125 runs (25 test docs × 5 seeds) | 42, 123, 456, 789, 101112 |
| **Phase 10** | Robustness Shift ($D_0$–$D_4$) | 50 | 10 | 15 | 25 | 625 runs (5 baselines × 5 domains × 25 runs) | 42, 123, 456, 789, 101112 |
| **Phase 10.5**| Recovery Benchmark ($D_0$–$D_4$) | 50 | 10 | 15 | 25 | 750 runs (6 baselines × 5 domains × 25 runs) | 42, 123, 456, 789, 101112 |
| **Phase 11** | Human-in-the-Loop Gate ($D_0$–$D_4$) | 50 | 10 | 15 | 25 | 875 runs (7 baselines × 5 domains × 25 runs) | 42, 123, 456, 789, 101112 |

### Methodological Vulnerability: Test Set Redundancy
- **Observation:** In Phase 10, the 125 test runs per baseline are composed of 5 domain partitions with exactly 5 documents each (`['doc_mp_026', 'doc_mp_029', 'doc_mp_033', 'doc_mp_037', 'doc_mp_041']` for $D_0$; `['doc_mp_027', 'doc_mp_031', 'doc_mp_035', 'doc_mp_039', 'doc_mp_043']` for $D_1$, etc.).
- **Implication:** Each domain's empirical performance is estimated from only **5 physical documents** evaluated across 5 random seeds. While random seeds vary retrieval perturbations and noise, the underlying structural diversity per domain is low ($N=5$).

---

## 3. Metric Evolution & Definition Consistency

| Metric Category | Metrics Used | Introduced In | Target Direction | Formula / Definition | Cross-Phase Consistency Assessment |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Retrieval** | Recall@K (K=1,3,5), MRR, nDCG | Phase 6 | Higher is better | $\text{Recall@K} = \frac{\vert \text{Relevant} \cap \text{Top-K} \vert}{\vert \text{Relevant} \vert}$ | **CONSISTENT**: Evaluated consistently across P6–P7. |
| **Grounding** | Precision, Recall, F1, IoU | Phase 7 | Higher is better | $\text{IoU} = \frac{\text{Area}(B_{\text{pred}} \cap B_{\text{gt}})}{\text{Area}(B_{\text{pred}} \cup B_{\text{gt}})}$ | **CONSISTENT**: Grounding threshold $\tau_{\text{IoU}} = 0.5$ held constant. |
| **Calibration** | ECE, MCE, Brier Score | Phase 8 | Lower is better | $\text{ECE} = \sum_{m=1}^M \frac{\vert B_m \vert}{N} \vert \text{acc}(B_m) - \text{conf}(B_m) \vert$ | **CONSISTENT**: 10-bin uniform calibration applied across P8–P9. |
| **Selective Pred.** | Coverage, Selective Acc, AURC, E-AURC | Phase 9 | Acc/Cov $\uparrow$, AURC $\downarrow$ | $\text{Selective Acc} = \frac{\sum \mathbf{1}(\hat{y}=y, a=1)}{\sum a_i}$ | **CONSISTENT**: Standard Geifman & El-Yaniv (2017) selective formulation. |
| **Domain Shift** | Robustness Gap ($\Delta_{\text{rob}}$), Relative Drop | Phase 10 | Lower is better | $\Delta_{\text{rob}} = \text{Acc}_{D_0} - \text{Acc}_{D_{\text{shift}}}$ | **CONSISTENT**: Measured against in-domain baseline $D_0$. |
| **Safety Recovery** | SUC, URR | Phase 10.5 | SUC $\uparrow$, URR $\le 0.05$ | $\text{SUC} = \frac{N_{\text{safe\_useful}}}{N_{\text{total}}}$, $\text{URR} = \frac{N_{\text{unsafe}}}{N_{\text{useful}}}$ | **CRITICAL SHIFT**: SUC replaced raw selective accuracy to account for recovered answers. |
| **Human-in-the-Loop**| Emission Rate, Escalation Rate, Conditional URR | Phase 11 | SUC $\uparrow$, Cond URR $\le 0.05$ | $\text{Cond URR} = \frac{N_{\text{unsafe\_emitted}}}{N_{\text{emitted}}}$ | **CONSISTENT REFINEMENT**: Separates automated emissions from human escalations. |

---

## 4. Operating Point & Threshold Consistency

| Decision Point | Phase 5/5.1 | Phase 8 | Phase 9 | Phase 10 | Phase 10.5 | Phase 11 | Consistency Verdict |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Quality Assessment Cutoff** | $\tau_Q = 0.65$ | N/A | N/A | $\tau_Q = 0.60$ | $\tau_Q = 0.60$ | $\tau_Q = 0.60$ | **MINOR DRIFT**: Minor shift from 0.65 to 0.60 between P5 and P10. |
| **Grounding Verification Threshold** | N/A | N/A | $\tau_G = 0.50$ | $\tau_G = 0.50$ | $\tau_G = 0.50$ | $\tau_G = 0.50$ | **CONSISTENT** |
| **Confidence Abstention Threshold** | $\tau_C = 0.70$ | $\tau_C = 0.75$ | $\tau_C = 0.70$ | $\tau_C = 0.70$ | $\tau_C = 0.70$ | Layered ($\tau_1=0.85, \tau_2=0.60$) | **EXPLAINED**: Layered triage introduced in P11 intentionally. |
| **Safety Tolerance Cutoff ($\epsilon_{\text{safe}}$)** | N/A | N/A | N/A | N/A | $\epsilon = 0.050$ | $\epsilon = 0.050$ | **CONSISTENT**: Rigorous 5% error ceiling maintained across P10.5 and P11. |

---

## 5. Summary of Methodological Discrepancies

1. **Synthetic vs. Real Domain Shift:** In Phase 10, domain shifts $D_1$ through $D_4$ are generated via synthetic perturbation overlays (e.g. synthetic font changes, synthetic gaussian blur, synthetic layout scrambles) applied to the base fixture documents, rather than authentic out-of-distribution corpora (e.g. real invoices from varied countries, handwritten medical records, historic archives).
2. **Cardinality Discrepancy:** The repository transitioned from single-page images ($N=4$ raw images) in early phases to a 50-document multi-page collection in Phase 6. While this allowed long-document retrieval testing, the total unique document count remained constant from Phase 6 through Phase 11 ($N=50$).
3. **Statistical Power Ceiling:** Because each domain contains only 5 distinct documents, hypothesis tests evaluating domain-specific shifts (such as $D_2$ and $D_4$) suffer from high sample correlation across seeds, inflating statistical significance while limiting external validity.
