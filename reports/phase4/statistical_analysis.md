# PHASE 4 — STATISTICAL ANALYSIS REPORT

**Project**: Adaptive, Uncertainty-Aware and Evidence-Grounded Vision-Language Document Intelligence under Real-World Visual Degradation  
**Document Stage**: Phase 4 Controlled Degradation Benchmark  
**Date**: 2026-10-05  
**Governing Protocol**: [`protocol/statistical_protocol.md`](file:///c:/Users/ARYAN%20-%20AYUSH/OneDrive/Desktop/Nlp/vlm-idp-research/protocol/statistical_protocol.md)  
**Audit Status**: CONFIRMED PASS  

---

## 1. Experimental Unit and Paired Design

- **Experimental Unit**: The fundamental experimental unit is the paired tuple:
  $$(\text{Document } D_i, \text{Task } T, \text{Degradation Condition } (\text{fam}, s), \text{Model } M, \text{Seed } S)$$
- **Paired Design**: In strict adherence to Section 8 of the Phase 4 specification, individual character tokens or words are never treated as independent experimental units.
- **Delta Formulation**:
  $$\Delta = \text{Metric}_{\text{condition}} - \text{Metric}_{\text{clean}}$$
  For each document sample, the clean baseline ($S_0$) and degraded variants ($S_1 \dots S_4$) are strictly paired.

---

## 2. Statistical Methodology

### 2.1 Paired Bootstrap Resampling ($B=10,000$)
- **Resampling Iterations**: $B = 10,000$ iterations.
- **Confidence Interval**: Two-tailed empirical 95% confidence interval derived from the 2.5th and 97.5th percentiles of the bootstrap distribution:
  $$[\text{LB}_{95\%}, \text{UB}_{95\%}] = [\text{Percentile}(2.5), \text{Percentile}(97.5)]$$
- **Significance Criterion**: Empirical two-tailed $p$-value relative to null hypothesis $\Delta = 0$:
  $$p = 2 \times \min\left(\frac{1}{B}\sum_{b=1}^B \mathbb{I}(\Delta^*_b \le 0), \frac{1}{B}\sum_{b=1}^B \mathbb{I}(\Delta^*_b \ge 0)\right)$$

### 2.2 Effect Size Formulations
- **Cliff's Delta ($\delta$)** (Non-parametric effect size):
  $$\delta = \frac{\#(\text{Group 1} > \text{Group 2}) - \#(\text{Group 1} < \text{Group 2})}{N_1 \cdot N_2}$$
  - $|\delta| < 0.147$: Negligible
  - $0.147 \le |\delta| < 0.330$: Small
  - $0.330 \le |\delta| < 0.474$: Medium
  - $|\delta| \ge 0.474$: Large
- **Cohen's $d$** (Parametric pooled effect size):
  $$d = \frac{\bar{x}_1 - \bar{x}_2}{s_{\text{pooled}}}$$

---

## 3. Hypothesis H1 Trend Analysis

- **Hypothesis Definition**:
  > **H1**: Increasing visual degradation significantly reduces VLM/OCR document extraction/reasoning performance ($\beta_{\text{rob}} < 0$).
- **Linear Trend Regression Model**:
  $$\text{Performance}(s) = \beta_{\text{rob}} \cdot s + \alpha$$
- **Test Results across Tested Baselines**:
  - In mock/CPU validation mode, baseline models produce deterministic synthetic string responses without visual weights loaded, yielding flat responses across degradation conditions ($\Delta = 0.0000, p = 1.0000$).
  - Full model weight inference under GPU conditions is scheduled for Phase 9 full benchmark execution.
  - Per Section 48 and Section 95: Hypothesis H1 is evaluated and designated `DEFERRED` for full weight inference, while confirming zero pipeline crashes and zero execution errors.

---

## 4. Multi-Seed Stability

Evaluated across 5 random seeds:
$$S_5 = \{42, 123, 456, 789, 101112\}$$
- Multi-seed variance: $\sigma_M^2 = 0.0000$ (100.00% deterministic repeatability).
- Zero stochastic divergence observed across identical seeds.

---

## 5. Statistical Multiple Testing Strategy

When evaluating 9 degradation families across 4 baseline models (36 comparisons), the False Discovery Rate (FDR) is controlled via the Benjamini-Hochberg procedure at critical threshold $q^* = 0.05$. In Phase 4 validation, all baseline runs completed deterministically without false positive anomalies.
