# PHASE 5 SCIENTIFIC AUDIT — STATISTICAL RECALCULATION & H2 VALIDATION

**Audit Item**: Statistical Tests, Paired Bootstrap Resampling ($B=10,000$), Effect Sizes, and Hypothesis H2  
**Audit Status**: VERIFIED PASS  

---

## 1. Audit Objective
Hypothesis H2 states:
> *"Adaptive degradation-aware routing reduces performance degradation compared with a fixed VLM pipeline."*

The audit independently verified the statistical comparison between **R2 (Rule-Based Quality Router)** and **R1 (Fixed Best Baseline - B2)** across all 900 benchmark conditions.

---

## 2. Statistical Reconciliation Table

| Metric | Reported in Phase 5 Report | Stored in `E5_ROUTING_summary.json` | Recomputed Value | Absolute Difference | Status |
|:---|:---:|:---:|:---:|:---:|:---:|
| **Control Mean (R1: B2)** | 0.7778 | 0.7777777777777778 | 0.7777777777777778 | $0.0000$ | **VERIFIED** |
| **Treatment Mean (R2)** | 0.7671 | 0.7671111111111112 | 0.7671111111111112 | $0.0000$ | **VERIFIED** |
| **Observed Delta (R2 - R1)**| **-0.0107** | -0.0106666666666667 | -0.0106666666666667 | $0.0000$ | **VERIFIED** |
| **Empirical 95% CI Lower** | -0.0127 | -0.0126666666666667 | -0.0126666666666667 | $0.0000$ | **VERIFIED** |
| **Empirical 95% CI Upper** | -0.0086 | -0.0086333333333333 | -0.0086333333333333 | $0.0000$ | **VERIFIED** |
| **Empirical $p$-value** | $< 0.0001$ | $0.0$ | $0.0$ | $0.0000$ | **VERIFIED** |
| **Cliff's $\delta$** | **-0.0286** | -0.0286419753086420 | -0.0286419753086420 | $0.0000$ | **VERIFIED** |
| **Cliff's Interpretation** | Negligible | Negligible ($|\delta| < 0.147$) | Negligible ($|\delta| < 0.147$) | Identical | **VERIFIED** |
| **Cohen's $d$** | **-0.0648** | -0.0647713000910570 | -0.0647713000910570 | $0.0000$ | **VERIFIED** |
| **Cohen's Interpretation** | Negligible | Negligible ($|d| < 0.20$) | Negligible ($|d| < 0.20$) | Identical | **VERIFIED** |

Numerical verification is exact across all parameters.

---

## 3. Scientific Interpretation of Hypothesis H2
1. **Direction of Effect**: The deployable rule-based router (R2) scored slightly lower than the unconditional monolithic B2 model ($\Delta = -0.0107$).
2. **Statistical Significance vs Practical Significance**:
   - Because $N = 900$ is large, the $-0.0107$ drop is statistically significant ($p < 0.0001$, CI $[-0.0127, -0.0086]$ strictly excludes $0$).
   - However, the effect size is **Negligible** by both non-parametric (Cliff's $\delta = -0.0286$) and parametric (Cohen's $d = -0.0648$) standards.
3. **Scientific Status**:
   - The reported conclusion: **`H2 = NOT_SUPPORTED`** is **SCIENTIFICALLY SOUND AND FULLY JUSTIFIED**.
   - Under the pre-declared criterion of task accuracy superiority, adaptive routing does not outperform the monolithic 7B VLM.
   - However, as documented in `cost_analysis.md`, adaptive routing achieves a **$7.78\%$ computational cost reduction** with only a negligible $1.07\%$ accuracy penalty.

## 4. Verdict
**STATUS: PASS**. The reported statistical tests, effect sizes, confidence intervals, and hypothesis verdict are 100% mathematically correct and reproducible.
