# Report 09: Formal Statistical Hypothesis Testing for Hypothesis H6

## 1. Hypothesis Formulation
- **Research Question RQ8**: Can calibrated uncertainty estimates identify unreliable document intelligence outputs and support selective abstention under realistic visual degradation and long-document retrieval conditions?
- **Hypothesis H6 (Frozen Protocol)**:
  *Post-hoc calibrated uncertainty combined with abstention produces a reliable risk-coverage trade-off, reducing error among answered queries as coverage decreases, while maintaining calibration across visual degradation conditions.*
- **Formal Null Hypothesis ($H_0$)**:
  $$\mu_{\text{Risk}}(A0) - \mu_{\text{Risk}}(A5) \le 0$$
- **Alternative Hypothesis ($H_1$)**:
  $$\mu_{\text{Risk}}(A0) - \mu_{\text{Risk}}(A5) > 0$$

## 2. Statistical Methodology
- **Test**: Paired non-parametric bootstrap test.
- **Resampling Iterations**: $B = 10,000$.
- **RNG Seed**: 42 (Frozen).
- **Test Sample Size**: $N = 125$ evaluation runs (25 documents $\times$ 5 seeds: 42, 123, 456, 789, 101112).
- **Significance Level**: $\alpha = 0.05$.

## 3. Empirical Results
From the master benchmark evaluation:
- Observed Mean Error (A0): 0.2800
- Observed Selective Error at 80% Coverage (A5): 0.1200 (incurred errors among test queries)
- **Observed Mean Difference ($\bar{d}$)**: **0.1600**
- **95% Bootstrap Confidence Interval**: **[0.0960, 0.2320]**
- **Empirical P-Value**: **$p = 0.000000 < 0.0001$**
- **Effect Size (Cohen's $d_z$)**: **1.1429** (Large effect size)

## 4. Formal Verdict
Because $\bar{d} = 0.1600 > 0$, the 95% CI strictly excludes zero, and $p < 0.0001 \ll 0.05$, the null hypothesis $H_0$ is decisively rejected.

$$\mathbf{VERDICT: \quad SUPPORTED}$$
