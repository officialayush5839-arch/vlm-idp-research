# Uncertainty Information Boundary Audit

**Audited Commit:** `209d7eb`  
**Status:** PASS (Strict Observable Runtime Input Compliance)  

---

## 1. Uncertainty Vector Construction Inspection
The 8-dimensional observable uncertainty vector:
$$U = [u_{\text{retrieval}}, u_{\text{semantic}}, u_{\text{spatial}}, u_{\text{numeric}}, u_{\text{table}}, u_{\text{sufficiency}}, u_{\text{quality}}, u_{\text{agreement}}] \in [0, 1]^8$$
is computed strictly via `SignalExtractor.extract()` and `UncertaintyCalculator.compute_uncertainty_vector()`.

---

## 2. Feature-by-Feature Boundary Audit Table

| Signal | Upstream Source | Observable at Inference? | Uses Ground Truth? | Uses Gold Answers? | Uses Condition Metadata? | Status |
|---|---|:---:|:---:|:---:|:---:|:---:|
| $u_{\text{retrieval}}$ | Phase 6 (Retrieval score / top-1 margin) | YES | NO | NO | NO | PASS |
| $u_{\text{semantic}}$ | Phase 7 (Context-query semantic similarity) | YES | NO | NO | NO | PASS |
| $u_{\text{spatial}}$ | Phase 7 (Bounding box overlap / dispersion) | YES | NO | NO | NO | PASS |
| $u_{\text{numeric}}$ | Phase 7 (OCR vs VLM numeric discrepancy) | YES | NO | NO | NO | PASS |
| $u_{\text{table}}$ | Phase 7 (Table alignment score) | YES | NO | NO | NO | PASS |
| $u_{\text{sufficiency}}$ | Phase 7 (Evidence sufficiency score) | YES | NO | NO | NO | PASS |
| $u_{\text{quality}}$ | Phase 3 (Visual quality score $Q$) | YES | NO | NO | NO | PASS |
| $u_{\text{agreement}}$ | Phase 8 (Cross-modal agreement score) | YES | NO | NO | NO | PASS |

---

## 3. Findings
- No references to gold annotations, test split labels, or oracle bounding boxes exist in `src/reliability/signals.py`, `src/reliability/uncertainty.py`, `src/reliability/confidence.py`, or `src/reliability/pipeline.py`.
- Static AST inspection and runtime adversarial injection tests confirm zero information leakage.
