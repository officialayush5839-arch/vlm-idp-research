# PHASE 5 SCIENTIFIC AUDIT — UNCERTAINTY VECTOR AUDIT

**Audit Item**: Multi-Signal Uncertainty Formulation, Extraction, and Heuristic Proxies  
**Audit Status**: HEURISTIC PROXY DETECTED (P1 — Pre-Implementation Synthetic Signals)  

---

## 1. Frozen Formulation Check
Per `protocol/uncertainty_protocol.md`, the uncertainty vector is defined as:
$$\mathbf{u} = [u_{\text{vlm}}, u_{\text{ocr}}, u_{\text{ret}}, u_{\text{gnd}}, u_{\text{qual}}, u_{\text{agr}}] \in [0, 1]^6$$
- $u_{\text{vlm}}$: VLM generation consistency / predictive entropy
- $u_{\text{ocr}}$: Mean OCR token confidence score
- $u_{\text{ret}}$: Top-$k$ retrieval similarity margin
- $u_{\text{gnd}}$: Evidence grounding overlap / coverage
- $u_{\text{qual}}$: Document quality score from Phase 3
- $u_{\text{agr}}$: Semantic agreement between OCR text and VLM output

The data structure `UncertaintyVector` in `src/routing/schema.py` strictly satisfies this schema definition.

---

## 2. Signal Derivation Inspection in Phase 5

Because Phase 5 is an intermediate milestone preceding Phase 6 (Retrieval), Phase 7 (Grounding), and Phase 8 (Uncertainty Calibration & Abstention), genuine runtime signals for $u_{\text{ret}}$, $u_{\text{gnd}}$, and $u_{\text{vlm}}$ did not yet exist.

Inspection of `src/routing/pipeline.py` (lines 80–90) revealed that the uncertainty vector was populated using synthetic heuristics:
```python
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

### Audit Findings:
1. **$u_{\text{ret}}$ (Retrieval)**: Injected as a constant dummy value ($1.0$).
2. **$u_{\text{vlm}}, u_{\text{gnd}}, u_{\text{qual}}, u_{\text{agr}}$**: Computed directly from synthetic severity ($1.0 - s \cdot 0.2$).
3. **$u_{\text{ocr}}$**: Hardcoded conditional check against string labels `"skew_rotation"` and `"perspective_distortion"`.
4. **Leakage**: This introduced synthetic severity and degradation family metadata directly into the uncertainty vector.
5. **Scientific Nature**: The signals used in Phase 5 are **synthetic heuristic proxies**, NOT genuinely measured Bayesian predictive entropy or calibrated token logprobs.

---

## 3. Recommendations for IEEE Publication
1. **Scope Boundaries**: In the IEEE manuscript, Phase 5 must be clearly presented as focusing on **Visual Quality Feature Routing (R2)**, with the multi-signal uncertainty subsystem explicitly identified as a preliminary architectural scaffold pending Phase 8 integration.
2. **Do Not Claim Empirical Uncertainty Superiority**: The paper must state that end-to-end multi-signal uncertainty becomes operational upon completion of Phases 6, 7, and 8.
