# Phase 5 — Adaptive Routing Benchmark Results

## 1. Primary Benchmark Summary
Evaluated over 900 test conditions per policy (4 samples $\times$ 9 degradation families $\times$ 5 severity tiers $\times$ 5 seeds = 4,500 total policy evaluations):

| Policy ID | Policy Identity | Mean Score | Std Dev | Mean Latency | Relative Compute | Fallback Rate | Mean Regret |
|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **R1** | Fixed Best Baseline (B2) | 0.7778 | 0.1582 | 10.86 ms | 1.0000 | 0.00% | 0.0178 |
| **R2** | Rule-Based Quality Router | 0.7671 | 0.1708 | 10.86 ms | 0.9222 | 0.00% | 0.0284 |
| **R3** | Uncertainty-Directed Router | 0.6796 | 0.2009 | 10.90 ms | 0.9467 | 35.56% | 0.1160 |
| **R4** | Lightweight Learned Router | 0.7778 | 0.1582 | 10.86 ms | 1.0000 | 0.00% | 0.0178 |
| **R5** | Composite Quality + Uncertainty | 0.7724 | 0.1621 | 10.86 ms | 0.9444 | 0.00% | 0.0231 |
| **R0** | Oracle Upper Bound (Non-Deployable)| 0.7956 | 0.1481 | 10.86 ms | 0.9022 | 0.00% | 0.0000 |

---

## 2. Severity Tier Breakdown ($S_0$ through $S_4$)

| Policy | $S_0$ (Clean) | $S_1$ (Mild) | $S_2$ (Moderate) | $S_3$ (Severe) | $S_4$ (Extreme) |
|:---|:---:|:---:|:---:|:---:|:---:|
| **R1 (Fixed Best B2)** | 1.0000 | 0.8889 | 0.7778 | 0.6667 | 0.5556 |
| **R2 (Rule-Based)** | 1.0000 | 0.8889 | 0.7711 | 0.6467 | 0.5289 |
| **R3 (Uncertainty)** | 1.0000 | 0.7867 | 0.6222 | 0.4333 | 0.5556 |
| **R4 (Learned)** | 1.0000 | 0.8889 | 0.7778 | 0.6667 | 0.5556 |
| **R5 (Composite)** | 1.0000 | 0.8889 | 0.7711 | 0.6467 | 0.5556 |
| **R0 (Oracle Upper Bound)**| 1.0000 | 0.8978 | 0.7956 | 0.6933 | 0.5911 |

---

## 3. Scientific Discussion of Results
1. **Accuracy Ceiling**: Monolithic B2 (`Qwen2.5-VL-7B`) maintains a very high score floor across mild-to-moderate degradation. Deployable quality routing achieves 0.7671 (within 1.07% of the fixed best baseline).
2. **Compute Savings**: While R1 consumes 1.0000 relative compute, R2 reduces compute cost to 0.9222 (**7.78% reduction in computational expenditure**).
3. **Oracle Headroom**: The retrospective oracle achieves 0.7956, representing a theoretical performance ceiling of only +1.78% over B2. This indicates that while heterogeneous routing offers substantial efficiency benefits, the raw accuracy headroom of model switching is bounded under these baselines.
