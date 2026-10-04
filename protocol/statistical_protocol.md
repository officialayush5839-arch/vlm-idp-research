# Statistical Protocol — Hypothesis Testing & Significance Framework

**Project Title**: Adaptive, Uncertainty-Aware and Evidence-Grounded Vision-Language Document Intelligence under Real-World Visual Degradation  
**Document Stage**: Phase 0 Research Protocol Freeze  
**Last Updated**: 2026-10-04  

---

## 1. Multi-Seed Replication Protocol

To ensure that reported improvements are statistically robust and not artifacts of stochastic sampling or weight initialization, all core experiments must be replicated across multiple seeds:

*   **Minimum Required Seeds**: 3 seeds ($S_3 = \{42, 123, 456\}$)
*   **Preferred Publication Seeds**: 5 seeds ($S_5 = \{42, 123, 456, 789, 101112\}$)

For every metric $M$, results must be reported in publication tables as:
$$\text{Reported Metric} = \bar{M} \pm \sigma_M \quad [95\% \text{ CI}: \text{LB}, \text{UB}]$$
Where $\bar{M}$ is the sample mean, $\sigma_M$ is standard deviation, and $[\text{LB}, \text{UB}]$ is the empirical $95\%$ confidence interval.

---

## 2. Hypothesis Testing Methodology

We formalize statistical tests for each of the six research hypotheses (H1–H6):

| Hypothesis | Independent Variable | Dependent Variable | Null Hypothesis ($H_0$) | Statistical Test | Target Effect |
|:---|:---|:---|:---|:---|:---|
| **H1** | Degradation Severity $s \in [0, 4]$ | Task F1 / ANLS | Performance is invariant to degradation ($\beta_{\text{rob}} = 0$) | Repeated-Measures ANOVA / Page Trend Test | Significant downward slope ($p < 0.001$) |
| **H2** | Pipeline Type (Adaptive vs Fixed VLM B2/B6) | Degraded F1 / ANLS | Adaptive routing yields no improvement over fixed pipeline | Paired Bootstrap Resampling ($B=10,000$) | $\Delta F_1 > 0$, $p < 0.01$ |
| **H3** | Grounding Enforcement (B5/Proposed vs B2) | Unsupported Answer Rate (UAR) | Grounding does not reduce unsupported answers | Paired Wilcoxon Signed-Rank Test | $\Delta \text{UAR} < 0$, $p < 0.01$ |
| **H4** | Abstention Mechanism (Proposed vs Fixed) | Selective Accuracy at 80% Coverage | Selective abstention yields no accuracy gain | Paired Bootstrap Test on Risk-Coverage Curve | Lower AURC, $p < 0.01$ |
| **H5** | Integrated System vs Components (Ablations) | Composite Efficiency-Reliability Score | Integrated system equals individual components | Paired permutation test across ablations A1–A7 | Significant Pareto improvement |
| **H6** | Dataset Domain (Forms vs Invoices vs Reports) | Normalized F1 across domains | Relative performance gains do not transfer across domains | Two-Way ANOVA (Method $\times$ Domain interaction) | No negative cross-domain interaction |

---

## 3. Paired Bootstrap Resampling Specification

For comparing model pairs (e.g., Proposed vs. Baseline B2), we adopt non-parametric **Paired Bootstrap Resampling** ($B=10,000$ iterations):

```python
def paired_bootstrap_test(
    scores_proposed: np.ndarray,
    scores_baseline: np.ndarray,
    n_bootstraps: int = 10000,
    seed: int = 42
) -> tuple[float, tuple[float, float], float]:
    rng = np.random.default_rng(seed)
    n = len(scores_proposed)
    delta_observed = np.mean(scores_proposed - scores_baseline)
    
    bootstrap_deltas = np.empty(n_bootstraps)
    for b in range(n_bootstraps):
        idx = rng.integers(0, n, size=n)
        bootstrap_deltas[b] = np.mean(scores_proposed[idx] - scores_baseline[idx])
        
    ci_lower = np.percentile(bootstrap_deltas, 2.5)
    ci_upper = np.percentile(bootstrap_deltas, 97.5)
    p_value = np.mean(bootstrap_deltas <= 0) if delta_observed > 0 else np.mean(bootstrap_deltas >= 0)
    
    return delta_observed, (ci_lower, ci_upper), p_value
```

---

## 4. Effect Size Reporting

In accordance with IEEE publication guidelines, reporting $p$-values alone is strictly prohibited. Every statistical test must accompany an effect size metric:
1. **Cohen's $d$** for normally distributed differences:
   $$d = \frac{\bar{x}_1 - \bar{x}_2}{s_{\text{pooled}}}$$
2. **Cliff's Delta ($\delta$)** for non-parametric ranking:
   $$\delta = \frac{\#(\text{Proposed} > \text{Baseline}) - \#(\text{Proposed} < \text{Baseline})}{N_1 \cdot N_2}$$
   Interpretation: $|\delta| < 0.147$ (negligible), $0.147 \le |\delta| < 0.33$ (small), $0.33 \le |\delta| < 0.474$ (medium), $|\delta| \ge 0.474$ (large).
