# Report 01: Theoretical Foundations of Uncertainty Calibration in Vision-Language Models

## 1. Executive Summary
In safety-critical intelligent document processing (IDP), raw confidence scores emitted by Vision-Language Models (VLMs) frequently fail to reflect true posterior correctness. Modern neural architectures exhibit severe overconfidence due to over-parameterization, unregularized cross-entropy minimization, and visual distribution shifts induced by real-world degradation. Phase 8 establishes a formal probabilistic framework for post-hoc uncertainty calibration and selective prediction under multimodal degradation.

## 2. Mathematical Formulation
Let $(X, Y) \sim \mathcal{D}$ represent the joint data distribution, where $X = (I, Q, E)$ comprises document image $I$, query text $Q$, and retrieved evidence $E$, while $Y \in \{0, 1\}$ denotes task accuracy ($Y=1$ if predicted answer $\hat{A}$ matches ground truth, $0$ otherwise).
The model outputs raw confidence $\hat{P} = f(X) \in [0, 1]$.

A model is defined to be **perfectly calibrated** if:
$$\mathbb{P}(Y = 1 \mid \hat{P} = p) = p, \quad \forall p \in [0, 1]$$

### 2.1 Calibration Error Metrics
1. **Expected Calibration Error (ECE)**:
   Given $M$ equal-width probability bins $B_m = (\frac{m-1}{M}, \frac{m}{M}]$, the ECE weights the bin-level absolute deviation:
   $$\text{ECE} = \sum_{m=1}^M \frac{|B_m|}{N} \left| \text{acc}(B_m) - \text{conf}(B_m) \right|$$
   where $\text{acc}(B_m) = \frac{1}{|B_m|} \sum_{i \in B_m} y_i$ and $\text{conf}(B_m) = \frac{1}{|B_m|} \sum_{i \in B_m} \hat{p}_i$.

2. **Maximum Calibration Error (MCE)**:
   $$\text{MCE} = \max_{m \in \{1, \dots, M\}} \left| \text{acc}(B_m) - \text{conf}(B_m) \right|$$

3. **Brier Score (Strictly Proper Scoring Rule)**:
   $$\text{Brier} = \frac{1}{N} \sum_{i=1}^N (\hat{p}_i - y_i)^2$$

4. **Negative Log-Likelihood (NLL)**:
   $$\text{NLL} = -\frac{1}{N} \sum_{i=1}^N \left[ y_i \log(\hat{p}_i) + (1 - y_i) \log(1 - \hat{p}_i) \right]$$

## 3. Empirical Observations
In our Phase 8 benchmark on 25 multi-page documents (125 evaluations across 5 seeds):
- **Raw Uncalibrated Confidence (A0/A2)**: ECE = 0.1120, MCE = 0.1733, Brier = 0.1581. Overconfidence is concentrated in degraded queries where visual distortion masks missing context.
- **Evidence-Aware Calibrated Confidence (A5)**: Brier score drops to **0.1116** (a 29.4% reduction in mean squared calibration error), and correctness AUROC rises from 0.7817 to **0.8333**.
