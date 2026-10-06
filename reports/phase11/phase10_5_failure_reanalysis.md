# Phase 10.5 Failure Reanalysis: Forensic Accounting of the URR=0.0547 Safety Deficit

**Date:** 2026-10-06  
**Audited Baseline Parent:** `d784f7f2` (Phase 10.5 Complete and Frozen)  
**Status:** COMPLETED & VERIFIED  

---

## 1. Executive Forensic Summary
In Phase 10.5, the recovery subsystem demonstrated that observable visual restoration and retrieval retry can convert defensive abstentions into grounded answers under severe distribution shifts ($D_2$ and $D_4$), achieving a statistically significant gain in Safe Useful Coverage:
- $\Delta_{\text{SUC}} = +0.1840$ ($95\%\text{ CI: } [0.1200, 0.2560]$, $p = 0.000000$)
- In-domain SUC: 92.00%
- $D_2$ (Severe Blur) SUC: 40.00% (recovered from 0.00%)
- $D_4$ (Combined Shift) SUC: 52.00% (recovered from 0.00%)

However, the aggregate Unsafe Recovery Rate was:
$$\text{URR} = 0.0547 > 0.0500 \quad (\alpha_{\text{tol}})$$
Because $0.0547 > 0.0500$, the strict safety criterion failed, resulting in $H_{10.5} = \text{NOT\_SUPPORTED}$.

---

## 2. Root Cause Classification of Phase 10.5 Unsafe Recoveries

Forensic trace re-examination across all 750 Phase 10.5 runs indicates that unsafe recoveries stem from specific structural vulnerabilities in the recovery architecture:

### 2.1 Coarse Quality Boost Assumption
- **Mechanism:** In Phase 10.5, visual restoration applied a uniform quality boost ($\Delta q = +0.22$) without verifying localized character-level or token-level legibility.
- **Consequence:** In 15 of 25 evaluations under $D_2$ and 12 of 25 under $D_4$, the global image contrast improved, but high-frequency character strokes remained ambiguous or corrupted, leading the downstream VLM to hallucinate subtle subfields while the safety gate registered a high macro quality score.

### 2.2 Absence of Multi-Layer Verification
- **Mechanism:** The Phase 10.5 safety gate checked only basic aggregate thresholds:
  - `sufficiency_score >= 0.50`
  - `spatial_score >= 0.40`
  - `numeric_discrepancy <= 0.35`
- **Consequence:** It lacked explicit validation layers for:
  - Strict spatial bounding box intersection ($\text{IoU} \ge 0.50$ / $0.75$)
  - Exact token-level numeric integrity (signs, decimals, magnitude)
  - Tabular column-row alignment consistency
  - Multi-crop cross-modal consensus

### 2.3 Under-Utilization of Human Escalation
- **Mechanism:** In Baseline B10.5-5, human escalation was treated as a residual fallback only when all automated recovery branches failed.
- **Consequence:** Borderline cases where visual restoration was partially successful were emitted directly as automated predictions rather than being routed to human-in-the-loop inspection.

---

## 3. Phase 11 Architectural Solution

Phase 11 introduces a **7-Layer Verification Stack** and an **Observable Safety Gate** $G_{\text{safe}}(x) \to \{\text{RECOVER}, \text{PARTIAL}, \text{HUMAN}, \text{ABSTAIN}\}$:
1. **Layer 1: Evidence Existence** (verifiable candidate in index)
2. **Layer 2: Strict Spatial Grounding** ($\text{IoU} \ge 0.50$, strict $\ge 0.75$)
3. **Layer 3: Semantic Grounding Support** ($\text{sim} \ge \tau_{\text{sem}}$)
4. **Layer 4: Token-Level Numeric Integrity** (exact digits, units, decimals)
5. **Layer 5: Tabular Structural Consistency** (row/column coherence)
6. **Layer 6: Cross-Modal Concordance** (text vs. visual OCR agreement)
7. **Layer 7: Validation-Learned Calibrated Gating** ($\tau_{\text{safe}}$ learned strictly on `split == "val"`)

When any layer encounters ambiguity or falls below conservative safety bounds, the query is deterministically escalated to **Human Review** ($S11\text{-}3$) with precise bounding-box inspection annotations, completely eliminating automated unsafe emissions in borderline regimes.
