# Uncertainty Protocol — Multi-Signal Estimation & Calibration Framework

**Project Title**: Adaptive, Uncertainty-Aware and Evidence-Grounded Vision-Language Document Intelligence under Real-World Visual Degradation  
**Document Stage**: Phase 0 Research Protocol Freeze  
**Last Updated**: 2026-10-04  

---

## 1. Multi-Signal Uncertainty Formulation

Rather than querying the VLM for verbalized self-confidence (which suffers from severe sycophancy and uncalibrated overconfidence), our uncertainty module constructs a composite feature vector $\mathbf{u} \in \mathbb{R}^6$ extracted across the entire processing pipeline:

$$\mathbf{u} = \left[ u_{\text{vlm}}, u_{\text{ocr}}, u_{\text{ret}}, u_{\text{gnd}}, u_{\text{qual}}, u_{\text{agr}} \right]$$

```text
       PIPELINE STAGE                             UNCERTAINTY SIGNAL
+---------------------------+        +-----------------------------------------------+
| VLM Generation            | -----> | u_vlm: Token log-probability / consistency     |
| OCR Engine                | -----> | u_ocr: Mean OCR word/character confidence     |
| Dense Vector Retrieval    | -----> | u_ret: Top-1 retrieval cosine similarity score |
| Spatial Bounding Box      | -----> | u_gnd: Grounding overlap IoU / fuzzy text score|
| Quality Assessment Module | -----> | u_qual: Aggregated document visual quality Q   |
| OCR-VLM Agreement         | -----> | u_agr: Semantic overlap between OCR & VLM     |
+---------------------------+        +-----------------------------------------------+
                                                             |
                                                             v
                                             +-------------------------------+
                                             | Post-Hoc Calibrator           |
                                             | (Logistic / Isotonic / MLP)   |
                                             | Frozen on Validation Split    |
                                             +-------------------------------+
                                                             |
                                                             v
                                              Calibrated Confidence c in [0, 1]
                                                             |
                                           +-----------------+-----------------+
                                           |                                   |
                                      c >= tau_accept                     c < tau_accept
                                           |                                   |
                                           v                                   v
                                        VERIFIED                        REVIEW_REQUIRED
```

---

## 2. Feature Signal Definitions

1. **VLM Token Confidence ($u_{\text{vlm}}$)**:
   Normalized sequence log-likelihood of generated answer tokens:
   $$u_{\text{vlm}} = \exp\left( \frac{1}{|T_{\hat{y}}|} \sum_{t=1}^{|T_{\hat{y}}|} \log P(w_t \mid w_{<t}, I, q) \right)$$
2. **OCR Confidence ($u_{\text{ocr}}$)**:
   Mean confidence of OCR text bounding boxes intersecting the localized answer region.
3. **Retrieval Score ($u_{\text{ret}}$)**:
   Cosine similarity of top-1 retrieved chunk / page embedding to the query:
   $$u_{\text{ret}} = \max_{j} \frac{\mathbf{e}_q \cdot \mathbf{e}_{p_j}}{\|\mathbf{e}_q\| \|\mathbf{e}_{p_j}\|}$$
4. **Evidence Grounding Score ($u_{\text{gnd}}$)**:
   Fuzzy normalized token alignment score between generated answer string and raw OCR text inside the predicted bounding box:
   $$u_{\text{gnd}} = \text{Similarity}(\hat{y}, \text{CropText}(I, B_{\text{pred}}))$$
5. **Visual Quality Score ($u_{\text{qual}}$)**:
   Aggregated quality score $\mathcal{Q} \in [0, 1]$ output by the quality assessment module.
6. **Answer-Evidence Agreement ($u_{\text{agr}}$)**:
   Cosine similarity between VLM answer embedding and extracted OCR evidence chunk embedding.

---

## 3. Calibration Architectures

We benchmark three candidate post-hoc calibration architectures:

1. **Platt / Logistic Calibration (Baseline Calibrator)**:
   $$c = \sigma(\mathbf{w}^T \mathbf{u} + b) = \frac{1}{1 + \exp(-(\mathbf{w}^T \mathbf{u} + b))}$$
   Fitted via cross-entropy loss with $L_2$ regularization on the validation partition.
2. **Isotonic Regression**:
   Non-parametric isotonic regression fitted on a scalar projection of $\mathbf{u}$. Preserves monotonicity without assuming linear log-odds.
3. **Calibrated Multi-Layer Perceptron (Small MLP)**:
   A lightweight 2-layer MLP (Hidden dimension = 16, ReLU activation, Dropout = 0.1, Sigmoid output).

---

## 4. Frozen Threshold Protocol (Strict Validation Partitioning)

> [!IMPORTANT] Anti-Overfitting Protocol
> All calibration model parameters $(\mathbf{w}, b)$ and decision boundaries $(\tau_{\text{accept}}, \tau_{\text{review}})$ MUST be fitted strictly on the **Validation Partition** and frozen before evaluation on the Test Partition.

Decision Rules:
- If $c \ge \tau_{\text{accept}}$ and Grounding Status = Success: **`VERIFIED`**
- If $\tau_{\text{review}} \le c < \tau_{\text{accept}}$: **`UNCERTAIN`** (flagged with partial evidence)
- If $c < \tau_{\text{review}}$ or Grounding Status = Failed: **`REVIEW_REQUIRED`** (abstains from final assertion)

Threshold $\tau_{\text{accept}}$ is chosen on validation data to achieve a pre-specified target risk bound (e.g., empirical validation error $\le 5\%$).
