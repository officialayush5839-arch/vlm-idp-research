# PHASE 5 SCIENTIFIC AUDIT — IEEE PUBLICATION READINESS

**Audit Item**: Multi-Dimensional Assessment for IEEE Manuscript Integration  
**Audit Status**: CONDITIONALLY READY  

---

## 1. Ten-Dimension Scientific Evaluation (0–10 Scale)

| Dimension | Score (0–10) | Evaluation & Justification |
|:---|:---:|:---|
| **1. Novelty** | 8.5 / 10 | Integrating visual degradation quality assessment directly with multimodal routing is highly relevant to IEEE Transactions / CVPR document intelligence. |
| **2. Experimental Rigor** | 8.0 / 10 | 900 benchmark conditions evaluated over 4 datasets, 9 families, 5 severities, and 5 seeds. Bounded by simulation response function rather than full 7B decoding. |
| **3. Leakage Control** | 7.5 / 10 | Test/train/validation split boundaries are strictly respected. R1, R2, and R4 are leakage-free. However, `condition.severity` leaked into the heuristic `uncertainty_vector` for R3/R5. |
| **4. Statistical Rigor** | 9.5 / 10 | Paired non-parametric bootstrap resampling ($B=10,000$), exact confidence intervals, empirical $p$-values, Cliff's $\delta$, and Cohen's $d$ correctly applied. |
| **5. Reproducibility** | 9.0 / 10 | 100% deterministic recomputation down to the 6th decimal place across all 900 conditions and 4,500 evaluations. |
| **6. Baseline Fairness** | 9.0 / 10 | Compared against the strongest single monolithic baseline (B2: Qwen2.5-VL 7B), avoiding strawman comparisons. |
| **7. Metric Clarity** | 7.0 / 10 | Editorial ambiguity in calling the primary score "-1.07% ANLS/F1" when it is a normalized performance response index ($S$). Requires terminology correction. |
| **8. Cost Measurement Validity** | 7.5 / 10 | Computation reduction (7.78%) is derived from a defined architectural weight model rather than direct physical watt-hour measurements. Must be clearly qualified. |
| **9. Negative-Result Credibility** | 10.0 / 10 | Exemplary research integrity. Honest reporting of $H2 = \text{NOT\_SUPPORTED}$ without post-hoc threshold tweaking or publication bias. |
| **10. Claim/Evidence Alignment** | 8.0 / 10 | R2 rule routing and oracle headroom claims are 100% aligned. Claims regarding learned router R4 and uncertainty vector require qualification due to implementation state. |

---

## 2. Overall Scientific Readiness Score

$$\text{Scientific Readiness Score} = 8.5 + 8.0 + 7.5 + 9.5 + 9.0 + 9.0 + 7.0 + 7.5 + 10.0 + 8.0 = \mathbf{82.0} \, / \, 100$$

---

## 3. IEEE Readiness Classification

**CLASSIFICATION: `CONDITIONALLY_READY`**

### Pre-Requisites for Full Manuscript Integration:
1. **P1 — Run ID Path Template**: Correct `run_id` template in `src/routing/pipeline.py` to include degradation family and severity so all 4,500 individual traces persist without overwriting.
2. **P1 — Uncertainty Assembly**: Remove `condition.severity` and `condition.family` from `uncertainty_vector` assembly in `pipeline.py`, grounding uncertainty solely in image and model features.
3. **P1 — Learned Router Persistence**: Serialize fitted weights for `LearnedQualityRouter` so R4 executes as a genuine ML router rather than defaulting to B2.
4. **P2 — Metric Nomenclature**: Clarify in prose that the metric is a "Normalized Document Extraction Index ($S$)" rather than raw ANLS/Token F1 distance.
5. **P2 — Cost Model Disclosure**: State explicitly that the 7.78% compute savings reflects a normalized architectural cost model ($w_{\text{B0}}=0.1, w_{\text{B0-U}}=0.5, w_{\text{B1}}=0.8, w_{\text{B2}}=1.0$).
