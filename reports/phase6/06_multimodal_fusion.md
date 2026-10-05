# Phase 6 Report 06: Multimodal Score Fusion and Normalization

## 1. Score Alignment Problem
Text retrieval (BM25 or dense) produces unbounded or differing score distributions compared to visual cosine similarities. Direct summation creates domain bias and instability.

## 2. Normalization Formulation
In `src/retrieval/fusion.py`, raw scores are normalized per document across all candidate pages:

$$S^{\text{norm}}_i = \frac{S_i - \min_{j} S_j}{\max_{j} S_j - \min_{j} S_j + \epsilon}$$

When all scores are identical ($\max = \min$), the normalized score safely defaults to $1.0$ (if $S > 0$) or $0.0$, avoiding division by zero.

## 3. Weighted Linear Interpolation
Scores are combined via linear interpolation with frozen configuration parameter $\alpha = 0.60$:

$$S_{\text{hybrid}} = 0.60 \cdot S^{\text{norm}}_{\text{text}} + 0.40 \cdot S^{\text{norm}}_{\text{visual}}$$

## 4. Empirical Validation of Alpha
Ablation A3 evaluated $\alpha \in [0.0, 1.0]$:
- $\alpha = 0.00$ (Visual only): Recall@3 = 100.0%, MRR = 1.0000
- $\alpha = 0.40$: Recall@3 = 100.0%, MRR = 1.0000
- $\alpha = 0.60$ (Proposed default): Recall@3 = 100.0%, MRR = 1.0000
- $\alpha = 0.80$: Recall@3 = 100.0%, MRR = 1.0000
- $\alpha = 1.00$ (Text only): Recall@3 = 84.0%, MRR = 0.8400

Assigning a modest visual weight ($1 - \alpha \ge 0.20$) protects the system against text corruption while preserving lexical specificity on clean documents.
