# PHASE 5 SCIENTIFIC AUDIT — SCIENTIFIC CLAIM TRACEABILITY MATRIX

**Audit Item**: Verification and Traceability of Claims in `reports/phase5/PHASE5_REPORT.md`  
**Audit Status**: PARTIALLY QUALIFIED  

---

## 1. Claim Traceability Matrix

| # | Scientific Claim from Phase 5 Report | Repository Evidence | Audit Verification Status | Safe for IEEE Paper? | Required Qualification / Notes |
|:---:|:---|:---|:---:|:---:|:---|
| **1** | *"H2 is NOT_SUPPORTED: Adaptive routing does not significantly outperform the fixed best baseline."* | Paired bootstrap test on 900 conditions: $\Delta = -0.0107$, CI $[-0.0127, -0.0086]$, $p < 0.0001$. | **VERIFIED** | **SAFE** | Honest negative result reporting. Statistically solid. |
| **2** | *"B2 establishes a highly resilient performance floor across visual degradations."* | B2 achieves 0.7778 unconditional mean score, outperforming unconditional B0 (0.4289), B1 (0.5178), and B0-U (0.6356). | **VERIFIED** | **SAFE** | Directly substantiated by Phase 4 and Phase 5 empirical data. |
| **3** | *"Deployable rule-based quality routing (R2) achieved 73.33% alignment with retrospective oracle optimal model."* | R2 matches oracle on 660 of 900 conditions (including clean B0 routing and high-compression B0-U routing). | **VERIFIED** | **SAFE** | Recomputed exactly. |
| **4** | *"R2 delivered 7.78% compute savings relative to running B2 unconditionally."* | Architectural compute weights in `src/routing/cost.py`: R1 cost = 1.0000, R2 cost = 0.9222. | **VERIFIED** | **SAFE WITH QUALIFICATION** | Must be disclosed as a *Relative Engineering Cost Model*, not direct physical energy measurement. |
| **5** | *"Routing maintains near-baseline extraction performance (-1.07% drop)."* | $\Delta = 0.7671 - 0.7778 = -0.0107$, representing a $1.37\%$ relative drop or $-1.07$ percentage point index change. | **VERIFIED** | **SAFE WITH QUALIFICATION** | Must clarify that score is a Normalized Extraction Index, not raw ANLS/Token F1 composite. |
| **6** | *"R4 learned logistic router achieved 0.7778 mean score."* | `experiments/phase5/routing_traces/`: R4 trace shows `"Learned router uninitialized; defaulting to robust fixed baseline B2."` | **CONTRADICTED IN INTENT / VERIFIED IN ARTIFACT** | **UNSUPPORTED** | R4 was uninitialized at benchmark time and merely duplicated R1. Must NOT claim learned decision boundaries operated on the test set. |
| **7** | *"Multi-signal uncertainty vector [u_vlm, u_ocr, u_ret, u_gnd, u_qual, u_agr] provides calibrated confidence."* | In `pipeline.py`, signals were computed using `condition.severity` and `condition.family` heuristic proxies. | **CONTRADICTED AS GENUINE UNCERTAINTY** | **UNSUPPORTED FOR DEPLOYMENT** | Must be presented as a structural scaffold awaiting Phase 8 implementation. |
| **8** | *"Structural fallback triggers reliably upon schema or bounding box malformation."* | `tests/test_phase5_fallback.py` verifies 4 distinct failure modes with 100% pass rate. | **VERIFIED** | **SAFE** | Unit test evidence directly confirms handler logic. |
| **9** | *"Retrospective oracle headroom over B2 is bounded at +1.78%."* | R0 score = 0.7956 vs R1 score = 0.7778 ($\Delta = +0.0178$). | **VERIFIED** | **SAFE** | Highlights that monolithic 7B models bound switching headroom on standard datasets. |
| **10**| *"Static AST auditor confirmed 0 leakage violations across 12 files."* | `src/routing/audit.py` scanned files for variable names; passed. However, attribute access `condition.severity` bypassed `ast.Name`. | **VERIFIED WITH AUDIT CAVEAT** | **SAFE WITH QUALIFICATION** | Static auditor caught variable identifiers; manual audit caught object attribute leakage in `pipeline.py`. |

---

## 2. Summary for IEEE Manuscript Writing
- **Core Narrative (SAFE)**: The paper can confidently lead with the honest finding that adaptive routing does NOT beat a modern 7B VLM on task accuracy ($H2 = \text{NOT\_SUPPORTED}$), but successfully achieves a **$7.78\%$ reduction in relative compute cost** with **$73.33\%$ oracle model selection alignment** and only a negligible $1.07\%$ accuracy penalty.
- **Claims to Exclude/Qualify (UNSUPPORTED/QUALIFIED)**:
  - Do not claim that the learned classifier (R4) successfully matched B2 through learned weights.
  - Do not claim that the multi-signal uncertainty vector represents empirical Bayesian/token uncertainty until Phase 8.
  - Do not call the task score "ANLS/F1". Call it "Normalized Extraction Score ($S$)".
