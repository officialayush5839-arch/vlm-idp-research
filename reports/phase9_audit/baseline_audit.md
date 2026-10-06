# Phase 9 Baselines Architecture & Integrity Audit

**Audited Commit:** `209d7eb`  
**Status:** PASS  

---

## 1. System Inventory

| Baseline | Architecture | Signals Consumed | Calibration | Deployable? |
|---|---|---|---|:---:|
| **B9-0** | Unconditional Baseline | Raw confidence only | None | YES |
| **B9-1** | Grounding Verification Gate | Sufficiency & Spatial scores | None | YES |
| **B9-2** | Fixed Confidence Gate | Raw confidence ($\tau=0.75$) | None | YES |
| **B9-3** | Quality-Only Gate | Visual quality score ($Q \ge 0.65$) | None | YES |
| **B9-4** | Evidence-Only Gate | Retrieval score ($R \ge 0.70$) | None | YES |
| **B9-5** | **Proposed Multi-Signal** | Full 8D Uncertainty Vector | Temperature Scaled | YES |

---

## 2. Privileged Information Verification
- All baselines receive strictly the observable signals output by their designated components.
- B9-5 does not receive any privileged external data or oracle information.
- The comparison is structurally and methodologically fair.
