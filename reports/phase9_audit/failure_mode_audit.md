# Failure Mode Taxonomy & Diagnostics Audit

**Audited Commit:** `209d7eb`  
**Status:** PASS  

---

## 1. Structured 8-Class Taxonomy Definitions
The failure classification engine in `src/reliability/failure_modes.py` implements:

| Class | Identifier | Primary Input Feature | Trigger Condition |
|---|---|---|---|
| $F_{01}$ | `F01_RETRIEVAL_FAILURE` | $u_{\text{retrieval}}$ | Retrieval score gap $\ge 0.40$ |
| $F_{02}$ | `F02_VISUAL_DEGRADATION` | $u_{\text{quality}}$ | Quality degradation $\ge 0.40$ |
| $F_{03}$ | `F03_INSUFFICIENT_EVIDENCE`| $u_{\text{sufficiency}}$ | Grounding sufficiency score $< 0.60$ |
| $F_{04}$ | `F04_NUMERIC_CONFLICT` | $u_{\text{numeric}}$ | Numeric discrepancy $\ge 0.40$ |
| $F_{05}$ | `F05_TABLE_ALIGNMENT_FAILURE` | $u_{\text{table}}$ | Table alignment $< 0.60$ |
| $F_{06}$ | `F06_SPATIAL_GROUNDING_FAILURE` | $u_{\text{spatial}}$ | Spatial overlap ambiguity $\ge 0.40$ |
| $F_{07}$ | `F07_CROSS_PAGE_CONFLICT` | $u_{\text{semantic}}$ | Multi-page semantic dissonance $\ge 0.40$ |
| $F_{08}$ | `F08_MODEL_DISAGREEMENT` | $u_{\text{agreement}}$ | Cross-modal disagreement $\ge 0.40$ |

---

## 2. Multi-Failure Precedence & Exhaustiveness
- **Exhaustiveness:** Any query exhibiting uncertainty above threshold receives a primary diagnosis, with secondary diagnosis assigned if a second modality exceeds 0.35.
- **Precedence:** Highest uncertainty score takes precedence.
- **Independence from Ground Truth:** The diagnostic routine operates strictly on observable uncertainty features; no gold labels are consumed.
