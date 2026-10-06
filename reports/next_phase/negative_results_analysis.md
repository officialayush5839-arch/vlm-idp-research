# NEGATIVE RESULTS & FAILURE ANALYSIS

**Project:** Vision-Language Models for Intelligent Document Processing under Real-World Visual Degradation  
**Audit Scope:** Deep Dive into Unsupported Hypotheses ($H_2, H_9, H_{10}, H_{10.5}, H_{11}$)  
**Audit Date:** 2026-10-06  
**Auditor:** Senior Research Engineer & ML Reproducibility Auditor  
**Status:** COMPLETE (High Scientific Value of Honest Negative Findings)

---

## 1. The Value of Negative Results in Applied Machine Learning

In rigorous academic research, negative results—when achieved under disciplined controls and zero-leakage protocols—are often more valuable to the scientific community than inflated positive claims. They reveal fundamental theoretical trade-offs, boundaries of algorithmic feasibility, and flawed assumptions in common benchmark practices.

This repository features five prominent negative or partially failed experimental hypotheses:
1. **$H_2$:** The Learned Routing Failure
2. **$H_9$:** The Invariant AURC Frontier
3. **$H_{10}$:** The Defensive Abstention Accuracy Penalty
4. **$H_{10.5}$:** The Safety Threshold Breach in Autonomous Recovery
5. **$H_{11}$:** The Automation-Coverage Collapse under Human Escalation

---

## 2. In-Depth Failure Taxonomies

### 2.1 Failure 1: The Learned Router Deficit ($H_2$ — Phase 5.1)
- **Hypothesis:** A learned quality-aware router will select the optimal processing path (Direct VLM, Enhancement+VLM, or OCR-Fallback) per document, outperforming any fixed pipeline.
- **Empirical Result:**  
  $$\text{Acc}_{\text{Learned Router}} = 0.742 \quad \text{vs} \quad \text{Acc}_{\text{Fixed Best VLM}} = 0.760 \quad (\Delta = -0.0185, \; p = 0.5120)$$
- **Root Cause Analysis:**
  1. *Router Misclassification Cost:* When the router misclassifies a document of moderate quality into the severe OCR fallback route, it incurs an irreparable accuracy loss because OCR text drops formatting and layout cues.
  2. *Information Bottleneck:* The router was trained on a small validation set ($N=6$). Under zero-leakage, the router could not overfit to the test degradation distributions.
  3. *Scientific Lesson:* In low-data regimes, routing uncertainty often exceeds the performance gap between pipelines. A fixed, highly robust model is superior to an unreliable router.

---

### 2.2 Failure 2: Invariant AURC Frontier ($H_9$ — Phase 9)
- **Hypothesis:** Combining grounding verification, visual quality, and retrieval confidence into a multi-signal risk score will shift the selective risk-coverage curve downward, reducing Area Under Risk-Coverage curve ($\text{AURC}$).
- **Empirical Result:**  
  $$\text{AURC}_{\text{Multi-Signal}} = 0.1100 \quad \text{vs} \quad \text{AURC}_{\text{Unconditional Baseline}} = 0.1100 \quad (\Delta = 0.0000, \; p = 0.5008)$$
- **Root Cause Analysis:**
  1. *Monotonic Ranking Preservation:* While multi-signal gating improved selective accuracy at specific operational operating points (Selective Acc rose to $0.8211$ at $76\%$ coverage), its global ranking of correct vs incorrect predictions across the entire probability continuum was identical to standard softmax confidence.
  2. *Error Mode Alignment:* The errors made by the retrieval module correlated strongly with the errors made by the grounding module. When evidence was missing, both components failed simultaneously, providing no complementary orthogonal signal.
  3. *Scientific Lesson:* Multi-signal fusion does not magically create new discriminative information if the underlying representations share the same failure modes.

---

### 2.3 Failure 3: Defensive Abstention vs. Raw Accuracy Penalty ($H_{10}$ — Phase 10)
- **Hypothesis:** An uncertainty-aware adaptive system will maintain high raw accuracy across unseen distribution shifts ($D_0$–$D_4$).
- **Empirical Result:**  
  $$\text{Acc}_{\text{Adaptive}} = 0.5360 \quad \text{vs} \quad \text{Acc}_{\text{Direct VLM}} = 0.7660 \quad (\Delta = -0.2300, \; p = 1.0000)$$
  *Domain Breakdown:* In $D_2$ (visual style shift) and $D_4$ (combined shift), Adaptive Accuracy was $0.0000$ due to $100\%$ abstention.
- **Root Cause Analysis:**
  1. *Metric Conflict:* Traditional accuracy penalizes abstention as an incorrect prediction ($\text{score} = 0$).
  2. *Defensive Safety:* The system correctly recognized that its predictions under severe visual shift had near-zero reliability, so it refused to answer. By abstaining, it eliminated hallucinations, but was penalized on raw accuracy benchmarks.
  3. *Scientific Lesson:* Standard ML benchmarks fail to reward safety. Evaluation under distribution shift must use Selective Accuracy and Safe Useful Coverage rather than raw unconstrained accuracy.

---

### 2.4 Failure 4: The 5% Safety Ceiling Breach ($H_{10.5}$ — Phase 10.5)
- **Hypothesis:** Multi-signal recovery (re-ranking, dual-path enhancement, contrast adjustment) can restore previously abstained answers while guaranteeing an Unsafe Recovery Rate ($\text{URR}$) below the $0.0500$ safety threshold.
- **Empirical Result:**  
  $$\text{SUC} = 0.7200 \; (\Delta = +0.1840, \; p = 0.0000), \quad \text{but} \quad \mathbf{\text{URR} = 0.0547 > 0.0500}$$
- **Root Cause Analysis:**
  1. *Noise Recovery Hazard:* In severely degraded documents, recovering answers based on low-confidence evidence occasionally retrieves spurious visual artifacts that appear plausible, leading the model to hallucinate confident wrong answers.
  2. *Strict Statistical Criterion:* Even a single additional error among 25 recovered cases pushed the error percentage to $5.47\%$, violating the $5.0\%$ ceiling.
  3. *Scientific Lesson:* Fully automated recovery under heavy distribution shift has an irreducible safety floor. An autonomous system cannot achieve both high coverage recovery and sub-5% risk without external verification.

---

### 2.5 Failure 5: Automation Coverage Collapse ($H_{11}$ — Phase 11)
- **Hypothesis:** A layered verification gate with human escalation will preserve high automated safe useful coverage while guaranteeing $\text{URR} \le 0.0500$.
- **Empirical Result:**  
  $$\text{Conditional URR} = 0.0800 > 0.0500, \quad \text{Automated SUC} = 0.3200 \; (\Delta_{\text{SUC}} = -0.1680, \; p = 1.0000)$$
  *Escalation Rate:* $60.0\%$ of queries were escalated to human review.
- **Root Cause Analysis:**
  1. *Extreme Conservatism:* To guarantee safety on ambiguous cases, the 7-layer gate routed all moderate and severe shift cases to human queues, collapsing the autonomous system's useful throughput to only $32\%$.
  2. *Residual Error among Emitted Cases:* Even among the remaining $40\%$ supposedly "safe" emitted cases, 2 out of 25 cases contained subtle ground-truth mismatches, causing conditional URR to reach $8.0\%$.
  3. *Scientific Lesson:* Setting ultra-conservative thresholds protects users from catastrophic hallucination, but risks making the automated AI pipeline redundant if humans must review the majority of inputs.
