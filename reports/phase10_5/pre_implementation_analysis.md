# Phase 10.5 Forensic Pre-Implementation Analysis: Severe Distribution Shift & Recovery Mechanisms

**Date:** 2026-10-06  
**Audited Parent Commit:** `e27f1f8` (Phase 10 Complete & Frozen)  
**Status:** COMPLETE & VERIFIED  

---

## 1. Executive Forensic Summary
In Phase 10, the VLM-IDP multimodal document intelligence pipeline was evaluated under distribution shift across five distinct domains:
- $D_0$: In-Domain Control
- $D_1$: Layout Shift (Dense Tabular)
- $D_2$: Visual Style Shift (Severe Blur, Contrast, Noise)
- $D_3$: Structure Shift (Complex Semi-Structured Forms)
- $D_4$: Combined Stress (Severe Degradation + Dense Structure)

Under unconditional answering ($B10\text{-}0$), severe degradation caused dramatic performance collapse:
- In $D_2$, unconditional accuracy plummeted from 92.00% to 40.00%, generating an unsupported error rate of 60.00%.
- In $D_4$, unconditional accuracy dropped to 52.00% with a 48.00% unsupported error rate.

The Phase 9 / Phase 10 multi-signal reliability and safety mechanism ($B10\text{-}4$) reacted to this distribution shift with strict defensive gating:
- In $D_2$: Quality score dropped to 0.35, resulting in 100% abstention ($\text{Coverage} = 0.00\%$, $\text{Abstention F1} = 0.7500$, $\text{Unsupported Error Rate} = 0.00\%$).
- In $D_4$: Quality and retrieval scores dropped below safety cutoffs, producing 100% abstention ($\text{Coverage} = 0.00\%$, $\text{Abstention F1} = 0.6486$, $\text{Unsupported Error Rate} = 0.00\%$).

While this demonstrated total safety (zero hallucinations delivered to users), the mathematical consequence was complete loss of utility in severe conditions.

---

## 2. Root Cause Analysis of 100% Abstention in $D_2$ and $D_4$

1. **Monolithic Abstention Decision:**
   Phase 10 uses a binary outcome on utility: either an answer is emitted (`ACCEPT` / `ACCEPT_WITH_WARNING`) or no answer is emitted (`ESCALATE` / `ABSTAIN`). It does not distinguish between queries where visual enhancement or partial evidence extraction could yield a safe, verifiable answer versus queries that are genuinely irrecoverable.

2. **Absence of Observable Recovery Pathway:**
   When the Phase 3 visual quality score drops below $\tau_{\text{quality}} \approx 0.65$, or retrieval score drops below $\tau_{\text{retrieval}} \approx 0.70$, the pipeline halts. No secondary restoration loop (e.g., contrast normalization, edge sharpening) or partial evidence extraction pathway is attempted.

3. **All-or-Nothing Evidence Verification:**
   Queries often contain multi-part information. When complete document reasoning fails due to localized visual noise, partial grounding (e.g., extracting verified high-confidence subfields with strict citation support) can provide high-value utility while preserving zero-error guarantees.

---

## 3. Scientific Formulation of Phase 10.5 Recovery

### 3.1 Research Question (RQ10.5)
*When the Phase 9 reliability layer flags an input for abstention under severe distribution shift ($D_2, D_4$), can a controlled, observable recovery pathway convert a subset of abstentions into safe, evidence-supported partial or complete answers while maintaining an unsupported-answer rate ($\text{URR}$) at or below the predefined safety tolerance ($\alpha_{\text{tol}} \le 0.05$)?*

### 3.2 Hypothesis (H10.5)
*Under severe visual degradation and combined distribution shifts, a safety-preserving recovery pathway achieves significantly higher Safe Useful Coverage ($\text{SUC}$) than the Phase 10 reference policy ($B10.5\text{-}0$), with an Unsafe Recovery Rate ($\text{URR}$) that does not exceed the predefined safety bound ($\text{URR} \le 0.05$).*

### 3.3 Recovery Taxonomy
Phase 10.5 formalizes a 6-state recovery taxonomy:
1. `R0 = SAFE_COMPLETE`: Full verified answer with complete spatial & citation support.
2. `R1 = SAFE_PARTIAL`: Grounded partial answer; unverifiable components cleanly redacted or scoped.
3. `R2 = RECOVERABLE_WITH_RESTORATION`: Document recovered via observable visual preprocessing / OCR retry.
4. `R3 = HUMAN_ESCALATION`: High-uncertainty query formatted with bounding-box inspection cues for human review.
5. `R4 = UNSAFE_TO_ANSWER`: Visual signals too corrupted; answering would risk hallucination.
6. `R5 = IRRECOVERABLE`: Zero evidence retrievable; definitive rejection.

### 3.4 Zero-Leakage Invariant
Recovery eligibility $G_{\text{recovery}}(x) \in \{0, 1\}$ and strategy selection depend strictly on observable features:
- Visual quality vector ($u_{\text{quality}}$, blur, noise, contrast)
- Multimodal retrieval margin and fusion score
- Extracted token confidence and OCR character confidence
- Grounding sufficiency score and spatial alignment

Gold answers, ground truth strings, test labels, and evaluation metrics are strictly forbidden from the recovery pathway.

---

## 4. Hash Invariant Audit
All 845 pre-existing source, configuration, and reporting files across Phases 0–10 have been cryptographically hashed into `reports/phase10_5/pre_implementation_hash_manifest.json` under commit `e27f1f8`.
Phase 10.5 is strictly additive and read-only with respect to historical parent phases.
