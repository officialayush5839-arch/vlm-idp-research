# Report 08: Failure Taxonomy and Error Distribution in Selective Prediction

## 1. Uncertainty Failure Taxonomy
Selective prediction produces four distinct quadrant outcomes:
1. **Confident Correct (True Positive)**: High confidence ($\ge \tau$), correct answer. Desired automation zone.
2. **Uncertain Incorrect (True Negative)**: Low confidence ($< \tau$), incorrect answer. Successfully abstained.
3. **Confident Incorrect (Type I Error / Dangerous)**: High confidence ($\ge \tau$), incorrect answer. Undetected hallucination.
4. **Uncertain Correct (Type II Error / Inefficient)**: Low confidence ($< \tau$), correct answer. Unnecessary human review.

## 2. Quantitative Distribution (Target Coverage = 80%, N=125 Runs)

| Metric / Quadrant | A0 (No Abstention) | A2 (Uncalibrated) | A5 (Proposed Evidence-Aware) |
| :--- | :---: | :---: | :---: |
| **Confident Correct** | 90 (72.0%) | 82 (65.6%) | **87 (69.6%)** |
| **Uncertain Incorrect** | 0 (0.0%) | 17 (13.6%) | **22 (17.6%)** |
| **Confident Incorrect (Dangerous)** | 35 (28.0%) | 18 (14.4%) | **13 (10.4%)** |
| **Uncertain Correct (Inefficient)** | 0 (0.0%) | 8 (6.4%) | **3 (2.4%)** |

## 3. Key Observations
1. **Dangerous Hallucination Reduction**:
   Baseline A0 exposes the system to 35 confident errors (28.0%). Proposed A5 slashes dangerous errors to **13 (10.4%)**, a **62.9% reduction in undetected failures**.
2. **Efficiency Loss Minimization**:
   Proposed A5 only incorrectly abstains on 3 correct queries (2.4%), compared to 8 queries (6.4%) for the uncalibrated heuristic, demonstrating superior discriminative capacity (AUROC = 0.8333).
