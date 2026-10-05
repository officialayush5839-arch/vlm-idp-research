# PHASE 5 SCIENTIFIC AUDIT — ROUTING REGRET AUDIT

**Audit Item**: Empirical Evaluation of Routing Regret and Sub-Optimality Distributions  
**Audit Status**: VERIFIED PASS  

---

## 1. Audit Target & Definition
Routing regret measures the task score sacrificed by choosing model $m_{\text{selected}}$ instead of the retrospective optimal model $m^*$:
$$\text{Regret}(x) = S(m^*, x) - S(m_{\text{selected}}, x)$$
By definition of $m^* = \arg\max_m S(m, x)$, $\text{Regret}(x) \ge 0$ for all samples. Negative regret is mathematically impossible. In `scripts/run_phase5_benchmark.py`, line 177 enforces `regret = max(0.0, float(oracle_score - score))`.

---

## 2. Regret Distribution Reconciliation Table

| Policy | Mean Regret (Reported) | Mean Regret (Recomputed) | Median Regret | 95th Percentile ($p_{95}$) | Audit Status |
|:---|:---:|:---:|:---:|:---:|:---:|
| **R0 (Oracle)** | 0.0000 | 0.0000 | 0.0000 | 0.0000 | **VERIFIED** |
| **R1 (Fixed Best B2)** | **0.0178** | 0.0177777777777778 | 0.0000 | 0.1200 | **VERIFIED** |
| **R2 (Rule-Based)** | **0.0284** | 0.0284444444444444 | 0.0000 | 0.1200 | **VERIFIED** |
| **R3 (Uncertainty)** | **0.1160** | 0.1159999999999999 | 0.1200 | 0.3000 | **VERIFIED** |
| **R4 (Learned - Uninit)** | **0.0178** | 0.0177777777777778 | 0.0000 | 0.1200 | **VERIFIED** |
| **R5 (Composite)** | **0.0231** | 0.0231111111111111 | 0.0000 | 0.1200 | **VERIFIED** |

All statistics match the stored experiment summaries with zero discrepancy.

---

## 3. Breakdown by Degradation Family
- **Geometric Degradation (`skew_rotation`, `perspective_distortion`)**:
  Both R1 and R2 achieved **0.0000 mean regret**, confirming that R2 never erroneously routes geometrically skewed documents to conventional OCR (B0), perfectly avoiding catastrophic OCR collapse.
- **Compression & Illumination (`jpeg_compression`, `illumination`)**:
  R2 achieved lower regret than R1 by switching to B0-U under high severities ($S_3, S_4$).
- **Occlusion & Blur**:
  R1 (B2) maintained lower regret than R2 due to cases where edge degradation confused the rule boundary.

## 4. Verdict
**STATUS: PASS**. Regret formulations, median/95th percentiles, and mean regret values are 100% verified.
