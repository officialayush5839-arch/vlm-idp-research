# Phase 14 Statistical Hypothesis Testing Report

## 1. Methodology

Hypothesis testing was conducted using **Family-Level Cluster Bootstrapping** ($B = 10,000$ resamples) to account for intra-document correlation across pages and queries within the same document family.
Confidence intervals are empirical percentiles ($[2.5\%, 97.5\%]$). P-values are adjusted using the **Holm-Bonferroni correction**.

---

## 2. Hypothesis Testing Results (`table_13_statistical_tests.csv`)

### Hypothesis H14-3 (Retrieval Efficiency vs Unpruned Baseline)
- **Null Hypothesis ($H_0$)**: Pruning document context to top-2 pages does not improve exact match accuracy over the unpruned 5-page baseline ($\Delta \mu \le 0$).
- **Comparison**: Condition B14-B vs B14-A
- **Mean Difference ($\Delta \mu$)**: $+0.0836$ (+8.36 percentage points)
- **95% Bootstrap CI**: $[0.0364, 0.1345]$
- **Empirical $p$-value**: $p = 0.0002$ ($< 0.001$)
- **Decision**: **REJECT $H_0$ — HYPOTHESIS H14-3 SUPPORTED**

### Hypothesis H14-4 (Evidence Grounding Suppresses Unsupported Answers)
- **Null Hypothesis ($H_0$)**: Evidence grounding verification does not reduce the unsupported answer rate compared to the unpruned baseline ($\Delta \text{UAR} \le 0$).
- **Comparison**: Condition B14-A vs B14-C
- **Mean Difference ($\Delta \text{UAR}$)**: $+0.2109$ (+21.09 percentage point reduction)
- **95% Bootstrap CI**: $[0.1782, 0.2473]$
- **Empirical $p$-value**: $p = 0.0000$ ($< 0.0001$)
- **Decision**: **REJECT $H_0$ — HYPOTHESIS H14-4 SUPPORTED**

---

## 3. Statistical Power and Cluster Integrity
- Total document clusters: 55 independent document families.
- Total evaluated traces: 1,100 records ($55 \text{ docs} \times 4 \text{ conditions} \times 5 \text{ seeds}$).
- Bootstrap sample size: $B = 10,000$ cluster-preserving draws.
- Both 95% confidence intervals exclude zero with wide margins.
