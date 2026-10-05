# Phase 5 — Routing Regret Analysis

## 1. Mathematical Formulation
Routing regret measures the sub-optimality of a model decision compared to the retrospective oracle choice:
$$\text{Regret}(x) = \max_{m \in \mathcal{M}} S(m, x) - S(m_{\text{selected}}, x)$$
where $S(m, x) \in [0, 1]$ is the task evaluation metric. Regret is strictly non-negative ($\text{Regret}(x) \ge 0$).

---

## 2. Empirical Regret Distributions

| Policy | Mean Regret | Median Regret | 75th Percentile | 95th Percentile | Max Regret |
|:---|:---:|:---:|:---:|:---:|:---:|
| **R1_FIXED_BEST (B2)** | 0.0178 | 0.0000 | 0.0000 | 0.1200 | 0.1600 |
| **R2_RULE_BASED** | 0.0284 | 0.0000 | 0.0400 | 0.1200 | 0.1800 |
| **R3_UNCERTAINTY** | 0.1160 | 0.1200 | 0.2000 | 0.3000 | 0.4400 |
| **R4_LEARNED** | 0.0178 | 0.0000 | 0.0000 | 0.1200 | 0.1600 |
| **R5_COMPOSITE** | 0.0231 | 0.0000 | 0.0000 | 0.1200 | 0.1600 |

---

## 3. Analysis by Degradation Family
- **Skew & Perspective Distortion**:
  - R1 Regret: **0.0000** (B2 is already the oracle optimal model)
  - R2 Regret: **0.0000** (Rule engine correctly routed 100% of geometric cases to B2)
- **JPEG Compression & Illumination**:
  - R1 Regret: **0.0800** (B2 suffers slightly under heavy 8x8 DCT quantization)
  - R2 Regret: **0.0200** (R2 captures B0-U superiority, reducing regret by 75%)
- **Mild Structured Noise / Clean**:
  - R1 Regret: **0.0000** (All models achieve 1.000 on pristine inputs)
- **High Occlusion**:
  - R2 Regret: **0.0000** (Routes to B2)

## 4. Key Takeaway
The mean regret of the deployable Rule-Based router R2 is only **0.0284** across all 900 conditions, confirming that while it trades away a negligible amount of accuracy for computational efficiency, its decisions rarely deviate substantially from the optimal choice.
