# Report 04: Multi-Signal Evidence Weighting and Composite Confidence

## 1. Feature Synthesis
Single-signal model confidence reflects only token likelihood, which is often blind to missing document regions or visual blur.
Phase 8 constructs an inference-time composite raw confidence $C_{\text{comp}}$ synthesizing four orthogonal observable channels:
$$C_{\text{comp}} = w_m C_{\text{model}} + w_r C_{\text{retrieval}} + w_g C_{\text{grounding}} + w_q C_{\text{quality}}$$
where $\sum w_i = 1.0$.

### Channel Definitions:
1. **Model Confidence ($C_{\text{model}}$)**: Raw generation confidence $p \in [0, 1]$. ($w_m = 0.25$)
2. **Retrieval Quality ($C_{\text{retrieval}}$)**: Composite of score margin and normalized entropy:
   $$C_{\text{retrieval}} = 0.60 \cdot \text{margin} + 0.40 \cdot (1.0 - \text{entropy}) \quad (w_r = 0.20)$$
3. **Grounding Support ($C_{\text{grounding}}$)**:
   $$C_{\text{grounding}} = (0.40 S_{\text{sem}} + 0.30 S_{\text{cov}} + 0.30 S_{\text{spat}}) \cdot \rho_{\text{suff}} \cdot \rho_{\text{gnd}} \quad (w_g = 0.30)$$
   where $\rho_{\text{suff}} \in \{1.0, 0.70, 0.20\}$ and $\rho_{\text{gnd}} \in \{1.0, 0.75, 0.10\}$.
4. **Visual Quality ($C_{\text{quality}}$)**:
   $$C_{\text{quality}} = Q_{\text{overall}} \cdot (1.0 - 0.50 \max(Q_{\text{blur}}, Q_{\text{noise}}, Q_{\text{skew}})) \quad (w_q = 0.25)$$

## 2. Empirical Value
As demonstrated in Ablation A1-A4:
- Model-only confidence: AURC = 0.1578, AUROC = 0.7807.
- Full multi-signal composite confidence: AURC = **0.1316**, AUROC = **0.8333**, Brier = **0.1116**.
Multi-signal fusion successfully penalizes hallucinated answers where text generation was confident but visual grounding was absent.
