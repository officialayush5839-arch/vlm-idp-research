# Report 07: Degradation-Stratified Calibration and Uncertainty Behavior

## 1. Overview
Document visual degradation (blur, noise, low resolution, skew) severely distorts VLM internal representations. This report analyzes how calibration and uncertainty metrics behave when stratified across document degradation strata.

## 2. Empirical Stratification (Test Partition)

| Condition | Sample Count | Accuracy (Full Cov) | Mean Calibrated Conf | ECE | Brier Score |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Clean** | 6 | 1.0000 | 1.0000 | **0.0000** | **0.0000** |
| **Mild** | 7 | 0.7143 | 1.0000 | 0.2857 | 0.2857 |
| **Moderate** | 6 | 1.0000 | 1.0000 | **0.0000** | **0.0000** |
| **Severe** | 6 | 0.3333 | 0.2330 | 0.2330 | **0.0899** |

## 3. Analysis of Degradation Dynamics
1. **Severe Degradation Handling**:
   In severely degraded documents, raw model outputs are highly prone to hallucinated tokens. However, the multi-signal evidence aggregator captures low visual quality ($Q < 0.40$) and low semantic support ($S < 0.40$), successfully suppressing mean confidence to **0.2330**.
2. **Selective Abstention Effect**:
   Because severe documents have low confidence, the selective prediction threshold $\tau = 0.50$ automatically abstains on these queries, routing them to `REVIEW_REQUIRED` and preventing false downstream automation.
3. **Mild Degradation Miscalibration**:
   Under mild degradation, document text remains partially legible, leading the model to maintain higher confidence than actual correctness warrant, highlighting the need for continual multi-seed calibration.
