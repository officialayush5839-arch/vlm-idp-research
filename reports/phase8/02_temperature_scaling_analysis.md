# Report 02: Temperature Scaling Optimization and Empirical Dynamics

## 1. Formulation
Temperature scaling is a single-parameter extension of Platt scaling that rescales logit representations via temperature scalar $T > 0$.
Given confidence probability $p \in (0, 1)$, we recover raw logit $z = \text{logit}(p) = \log\left(\frac{p}{1 - p}\right)$.
The calibrated confidence is given by:
$$\hat{q}(p; T) = \sigma\left(\frac{z}{T}\right) = \frac{1}{1 + e^{-z/T}}$$

The optimal temperature $T^*$ is obtained by minimizing Negative Log-Likelihood on the frozen validation partition $\mathcal{D}_{\text{val}}$:
$$T^* = \arg\min_{T > 0} -\sum_{i \in \mathcal{D}_{\text{val}}} \left[ y_i \log\sigma\left(\frac{z_i}{T}\right) + (1 - y_i) \log\left(1 - \sigma\left(\frac{z_i}{T}\right)\right) \right]$$

## 2. Monotonicity Invariant
Because the mapping $z \mapsto \sigma(z/T)$ is strictly monotonically increasing for any $T > 0$, temperature scaling preserves rank ordering:
$$\text{rank}(\hat{q}_i) = \text{rank}(p_i), \quad \forall i$$
Consequently, the Area Under the ROC Curve (AUROC) and the ranking of candidates for selective prediction remain invariant under pure temperature scaling:
$$\text{AUROC}(\hat{q}) = \text{AUROC}(p) = 0.7817$$

## 3. Empirical Optimization on Validation Partition
On the 15-document validation partition (`split == 'val'`):
- Optimal Temperature $T^* = 0.4245$.
- Minimization converged via L-BFGS-B in 8 iterations.
- Test ECE decreased from 0.1120 (uncalibrated) to **0.0792** (temperature scaled).
- Artifact cryptographic SHA-256: `da4f1b410751488c...`
