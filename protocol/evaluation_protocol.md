# Evaluation Protocol — Formal Metric Definitions & Thresholds

**Project Title**: Adaptive, Uncertainty-Aware and Evidence-Grounded Vision-Language Document Intelligence under Real-World Visual Degradation  
**Document Stage**: Phase 0 Research Protocol Freeze  
**Last Updated**: 2026-10-04  

---

## 1. Metric Hierarchy Overview

Evaluation encompasses seven quantitative performance dimensions to evaluate accuracy, robustness, calibration, reliability, and computational efficiency simultaneously:

```text
                             EVALUATION SUITE
                                    |
      +---------------+-------------+-------------+---------------+
      |               |             |             |               |
  EXTRACTION & QA    OCR      RETRIEVAL &      UNCERTAINTY &   ROBUSTNESS &
  - Exact Match      - CER     GROUNDING        ABSTENTION      EFFICIENCY
  - Token F1         - WER     - Recall@K       - ECE           - Robustness Slope
  - ANLS                       - IoU            - Brier Score   - Latency / VRAM
                               - Region Rec@K   - Risk-Coverage - Route Dist.
```

---

## 2. Mathematical Metric Definitions

### A. Extraction & Question Answering
1. **Exact Match (EM)**:
   $$\text{EM} = \frac{1}{N} \sum_{i=1}^N \mathbb{I}(\hat{y}_i = y_i)$$
   Binary indicator after lowercasing and stripping punctuation.
2. **Token F1**:
   $$F_1 = \frac{2 \cdot P \cdot R}{P + R}, \quad P = \frac{|T_{\hat{y}} \cap T_y|}{|T_{\hat{y}}|}, \quad R = \frac{|T_{\hat{y}} \cap T_y|}{|T_y|}$$
   Computed over whitespace/character token bags.
3. **Average Normalized Levenshtein Similarity (ANLS)** (DocVQA standard):
   $$\text{ANLS} = \frac{1}{N} \sum_{i=1}^N \max_{j} \left( 1 - \frac{\text{Lev}(\hat{y}_i, y_{ij})}{\max(|\hat{y}_i|, |y_{ij}|)} \right) \cdot \mathbb{I}\left( \frac{\text{Lev}(\hat{y}_i, y_{ij})}{\max(|\hat{y}_i|, |y_{ij}|)} < \tau_{\text{anls}} \right)$$
   Where threshold $\tau_{\text{anls}} = 0.50$. Penalizes edit distance while zeroing out severe mismatches.

---

### B. OCR Quality
1. **Character Error Rate (CER)**:
   $$\text{CER} = \frac{S_c + D_c + I_c}{N_c}$$
   Where $S_c, D_c, I_c$ are character substitutions, deletions, and insertions, and $N_c$ is ground-truth character count.
2. **Word Error Rate (WER)**:
   $$\text{WER} = \frac{S_w + D_w + I_w}{N_w}$$

---

### C. Retrieval & Evidence Grounding
1. **Page Recall@$K$**:
   $$\text{Recall}@K = \frac{1}{N} \sum_{i=1}^N \mathbb{I}(p_i^* \in \text{Top-}K(\mathcal{R}_i))$$
   Proportion of queries where ground-truth evidence page $p_i^*$ is within retrieved top-$K$ candidates.
2. **Intersection-over-Union (IoU)**:
   $$\text{IoU}(B_{\text{pred}}, B_{\text{gt}}) = \frac{\text{Area}(B_{\text{pred}} \cap B_{\text{gt}})}{\text{Area}(B_{\text{pred}} \cup B_{\text{gt}})}$$
   Evaluated at thresholds $\text{IoU} \ge 0.50$ and $\text{IoU} \ge 0.75$.
3. **Region Recall@$K$**:
   Fraction of true supporting visual bounding boxes overlapped with $\text{IoU} \ge 0.50$ by predicted regions.
4. **Unsupported Answer Rate (UAR)**:
   $$\text{UAR} = \frac{\sum_{i=1}^N \mathbb{I}(\text{Answer Correct}_i \wedge \text{Grounding Failed}_i)}{\sum_{i=1}^N \mathbb{I}(\text{Answer Correct}_i)}$$
   Measures answers generated via language prior or spurious tokens rather than true evidence.

---

### D. Calibration & Uncertainty
1. **Expected Calibration Error (ECE)**:
   $$\text{ECE} = \sum_{m=1}^M \frac{|B_m|}{N} \left| \text{acc}(B_m) - \text{conf}(B_m) \right|$$
   Partitioning confidence estimates into $M=10$ equal-width bins $B_m$.
2. **Brier Score**:
   $$\text{BS} = \frac{1}{N} \sum_{i=1}^N (c_i - z_i)^2$$
   Where $c_i \in [0, 1]$ is estimated confidence and $z_i \in \{0, 1\}$ is correctness indicator.
3. **Reliability Diagram**: Binned plot of empirical accuracy vs. mean confidence with diagonal $y=x$ representing perfect calibration.

---

### E. Selective Prediction & Abstention
1. **Coverage**:
   $$\text{Coverage}(\tau) = \frac{1}{N} \sum_{i=1}^N \mathbb{I}(c_i \ge \tau)$$
   Fraction of instances accepted by the model at uncertainty threshold $\tau$.
2. **Selective Risk**:
   $$\text{Risk}(\tau) = \frac{\sum_{i=1}^N \mathcal{L}(\hat{y}_i, y_i) \cdot \mathbb{I}(c_i \ge \tau)}{\sum_{i=1}^N \mathbb{I}(c_i \ge \tau)}$$
   Where $\mathcal{L}(\hat{y}_i, y_i) = 1 - \mathbb{I}(\text{Correct}_i)$.
3. **Selective Accuracy**:
   $$\text{Selective Accuracy}(\tau) = 1 - \text{Risk}(\tau)$$
4. **Area Under the Risk-Coverage Curve (AURC)**:
   Integral of risk across coverage $\in [0, 1]$; lower AURC signifies better selective prediction.

---

### F. Robustness & Efficiency
1. **Performance Drop ($\Delta_{\text{deg}}$)**:
   $$\Delta_{\text{deg}}(s) = \text{Metric}(s=0) - \text{Metric}(s)$$
2. **Robustness Slope ($\beta_{\text{rob}}$)**:
   Linear regression slope of metric degradation against severity level $s \in \{0, 1, 2, 3, 4\}$. Flatter slope indicates superior robustness.
3. **Latency**: End-to-end processing time per query in milliseconds (mean and p95).
4. **VRAM Footprint**: Peak allocated GPU memory in Megabytes.
5. **Route Distribution**: Percentage of document instances assigned to `CLEAN`, `MODERATE`, and `SEVERE` pathways.
