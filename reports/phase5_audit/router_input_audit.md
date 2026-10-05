# PHASE 5 SCIENTIFIC AUDIT — ROUTER INPUT & FEATURE AUDIT

**Audit Item**: Inference-Time Observability and Input Leakage Analysis  
**Audit Status**: PARTIAL LEAKAGE DETECTED (P1 — Uncertainty Vector Label Contamination)  

---

## 1. Input Observability Audit Table

| Candidate Input | Permitted at Inference? | Actually Used by Router? | Policy Impacted | Leakage Risk / Finding |
|:---|:---:|:---:|:---:|:---|
| **Raw Degraded Image** | YES | YES | All | None. Input to Phase 3 feature extractor. |
| **Document/Page ID** | YES | YES (Metadata) | All | None. Used only for trace logging. |
| **Dataset Name** | YES | YES (Metadata) | All | None. Used for trace logging. |
| **10 Quality Features** | YES | YES | R2, R4, R5 | **LEAKAGE-FREE**. Extracted purely via image signal processing. |
| **Ground Truth Answers** | **NO** | **NO** | None | **VERIFIED CLEAN**. 0 access detected. |
| **Ground Truth Bounding Boxes** | **NO** | **NO** | None | **VERIFIED CLEAN**. 0 access detected. |
| **Evaluator Scores (ANLS/F1/EM)** | **NO** | **NO** | None | **VERIFIED CLEAN**. Evaluator called after routing. |
| **Oracle Candidate Scores** | **NO** | R0 Only | R0 (Oracle) | **LEAKAGE-FREE**. R0 is non-deployable upper bound; never passed to R1–R5. |
| **Synthetic Degradation Severity ($S_0 \dots S_4$)** | **NO** | **YES** | **R3, R5** | **CONTAMINATION DETECTED**. Leaked into `uncertainty_vector` in `pipeline.py`. |
| **Degradation Family Label** | **NO** | **YES** | **R3, R5** | **CONTAMINATION DETECTED**. Leaked into `uncertainty_vector` in `pipeline.py`. |

---

## 2. Detailed Code Inspection of Input Contamination

In `src/routing/pipeline.py` (lines 80–90):
```python
# 2. Assemble Inference-Time Uncertainty Vector
# Use observable quality score Q and baseline execution priors
q_score = 1.0 - (condition.severity * 0.20 if condition else 0.0)
uncertainty_vector = self.router.policy_manager.uncertainty_adapter.assemble_vector(
    vlm_confidence=q_score,
    ocr_confidence=q_score if (condition and condition.family not in ["skew_rotation", "perspective_distortion"]) else 0.20,
    retrieval_score=1.0,
    grounding_score=q_score,
    visual_quality_score=q_score,
    ocr_vlm_agreement=q_score,
)
```

### Analysis:
1. `condition.severity` and `condition.family` are synthetic metadata properties belonging to the benchmark harness (`DegradationCondition`), not properties observable at deployment inference time.
2. In Phase 5, downstream Phase 6 (retrieval), Phase 7 (grounding), and Phase 8 (probabilistic calibration) have not yet been built. The developer created a heuristic proxy for `uncertainty_vector` by referencing `condition.severity` and `condition.family`.
3. **Policies Contaminated**:
   - **R3 (Uncertainty-Directed)**: Consumes `uncertainty_vector` directly.
   - **R5 (Composite)**: Consumes `uncertainty_vector` for uncertainty escalation checks.
4. **Policies Uncontaminated**:
   - **R1 (Fixed Best - B2)**: Unconditional dispatch to B2. Does not read `uncertainty_vector`.
   - **R2 (Rule-Based Quality Router)**: Reads only `quality_features` (Laplacian blur, high-frequency noise, Radon skew, Michelson contrast, DCT compression, illumination, connected-component occlusion, quadrilateral perspective). Does not read `uncertainty_vector`.
   - **R4 (Learned Router)**: Reads only `quality_features`.

---

## 3. Impact on Hypothesis H2
Hypothesis H2 compares the pre-specified treatment **R2 (Rule-Based Quality Router)** against the control **R1 (Fixed Best Baseline)**.
Because R2 relies solely on image-derived visual features from Phase 3 and is 100% free of `condition.severity` and `condition.family` leakage, **the test of Hypothesis H2 remains scientifically valid and uncontaminated**.

However, R3 and R5 cannot be presented as valid deployable inference policies in the IEEE paper without correcting `uncertainty_vector` assembly to derive purely from observable image and model outputs.
