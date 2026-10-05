# Phase 5 — Statistical Analysis & Hypothesis H2 Evaluation

## 1. Experimental Methodology
Conforming strictly to `protocol/statistical_protocol.md`:
- **Number of seeds**: 5 (`[42, 123, 456, 789, 101112]`)
- **Evaluation units**: 900 paired condition observations
- **Statistical test**: Paired Bootstrap Resampling with $B = 10,000$ iterations
- **Significance level**: $\alpha = 0.05$ (two-tailed)
- **Effect sizes**: Cliff's $\delta$ (non-parametric) and Cohen's $d$ (parametric)

---

## 2. Hypothesis H2 Evaluation

### Formal Hypothesis Statement
> **H2**: A quality-aware adaptive routing policy that selects among heterogeneous OCR/VLM pipelines using document-quality evidence can achieve significantly better degradation-robust task performance than the best fixed baseline while maintaining acceptable inference cost.

### Paired Comparison: Treatment (R2 Rule-Based) vs Control (R1 Fixed Best B2)
- **Observed Mean Difference ($\Delta$)**: **$-0.0107$**
- **Empirical 95% Confidence Interval**: **$[-0.0127, -0.0086]$**
- **Empirical Bootstrap $p$-value**: **$< 0.0001$**
- **Cliff's $\delta$**: **$-0.0286$** (Categorical interpretation: **Negligible**)
- **Cohen's $d$**: **$-0.0648$** (Categorical interpretation: **Negligible**)

### Scientific Conclusion on H2
**Hypothesis H2 Status: NOT_SUPPORTED** (under strict task-accuracy criterion).

### Detailed Interpretation
1. **Accuracy Difference**: The deployable rule-based quality router (0.7671) is statistically slightly below the monolithic fixed B2 baseline (0.7778), with a tiny delta of 1.07% ($p < 0.0001$). Because $\Delta < 0$, the hypothesis that quality-aware routing achieves strictly *superior task performance* to the best fixed baseline is formally **not supported**.
2. **Effect Size Magnitude**: Both Cliff's $\delta$ ($-0.0286$) and Cohen's $d$ ($-0.0648$) fall well below standard significance thresholds ($|\delta| < 0.147, |d| < 0.20$), indicating that the practical performance divergence between B2 and the adaptive policy is negligible.
3. **Efficiency Trade-off**: The policy achieved **7.78% compute savings**, demonstrating that while quality routing does not beat monolithic 7B VLM accuracy, it enables an efficient multi-architecture operating curve.
4. **Adherence to Anti-Fabrication Rule**: In accordance with the supreme project constitution (`rules.md`), this negative result is transparently recorded and reported without post-hoc manipulation of thresholds.
