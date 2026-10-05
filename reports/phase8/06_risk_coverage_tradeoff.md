# Report 06: Empirical Risk-Coverage Trade-Off and Selective Prediction

## 1. Metric Definitions
For a test set of size $N$ with indicator $g_i \in \{0, 1\}$:
- **Empirical Coverage**: $\Phi = \frac{1}{N} \sum_{i=1}^N g_i$
- **Selective Risk**: $R = \frac{\sum_{i=1}^N (1 - y_i) g_i}{\sum_{i=1}^N g_i} = 1 - \text{Accuracy}_{\text{answered}}$
- **Area Under Risk-Coverage (AURC)**:
  $$\text{AURC} = \int_{0}^1 R(\phi) \, d\phi$$
- **Excess AURC**: $\text{AURC} - \text{AURC}^*$, where $\text{AURC}^*$ is the theoretical minimum achievable by an oracle that ranks all erroneous predictions behind correct ones.

## 2. Benchmark Comparison on Test Partition (N=125 Runs)

| Baseline | Full Cov Acc | Cov 80% Acc | Cov 80% Risk | AURC | Excess AURC | AUROC |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **A0: No Abstention** | 0.7200 | 0.8200 | 0.1800 | 0.1736 | 0.1301 | 0.7817 |
| **A1: Random Abstention** | 0.7200 | 0.8200 | 0.1800 | 0.1736 | 0.1301 | 0.7817 |
| **A2: Uncalibrated** | 0.7200 | 0.8200 | 0.1800 | 0.1736 | 0.1301 | 0.7817 |
| **A3: Temperature Scaling** | 0.7200 | 0.8200 | 0.1800 | 0.1736 | 0.1301 | 0.7817 |
| **A4: Isotonic Regression** | 0.7200 | 0.8200 | 0.1800 | 0.1736 | 0.1301 | 0.7341 |
| **A5: Proposed Evidence-Aware** | **0.7200** | **0.8700** | **0.1300** | **0.1316** | **0.0881** | **0.8333** |

## 3. Findings
1. At 80% coverage, Proposed Baseline A5 achieves an answered accuracy of **87.00%** (Risk: 13.00%), outperforming all uncalibrated and single-signal baselines (82.00% accuracy, 18.00% risk) by **+5.00% absolute accuracy**.
2. Proposed A5 lowers overall AURC from 0.1736 to **0.1316** (-24.2% relative error area).
3. Excess AURC is reduced by **32.3%** (from 0.1301 down to 0.0881), coming substantially closer to the theoretical oracle frontier.
