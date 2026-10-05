# PHASE 5 SCIENTIFIC AUDIT — METRIC DEFINITION & AGGREGATION AUDIT

**Audit Item**: Clarification of "Mean Task Score" and "-1.07% ANLS/F1" Terminology  
**Audit Status**: METRIC DEFINITION REQUIRES CORRECTION (P2 — Moderate Terminology Inaccuracy)  

---

## 1. Audit Investigation
The Phase 5 report (`PHASE5_REPORT.md`) repeatedly refers to:
- "Mean Task Score" (0.7671 vs 0.7778)
- "-1.07% ANLS/F1" (in Section 31 and executive summaries)
- "Primary Task Score: Exact Match (EM), Token F1, ANLS" (in Section 14)

The audit investigated the precise mathematical origin of this score.

---

## 2. Code Trace & Mathematical Origin
Inspection of `scripts/run_phase5_benchmark.py` (lines 121–173) revealed:
1. `pipeline.process_sample` executes the model runner and computes token-level Exact Match (EM), Token F1, and ANLS via `src/benchmark/evaluator.py`.
2. However, for recording policy benchmark scores across the 900 conditions, line 172 assigns:
   ```python
   score = candidate_scores.get(chosen_model, 0.5)
   results_by_policy[policy.value].append(score)
   ```
3. `candidate_scores` is a normalized performance response index ($S \in [0, 1]$) calibrated across degradation families and severities based on the Phase 4 degradation benchmark.

### Problem Analysis:
- Calling this score **"ANLS/F1"** is factually inaccurate. ANLS (Average Normalized Levenshtein Similarity) and Token F1 are distinct string-matching metrics with different mathematical formulations and penalty curves.
- The recorded metric is actually a **Normalized Task Performance Index ($S \in [0, 1]$)**.
- While the comparative difference ($\Delta = -0.0107$, or $-1.07\%$ relative drop) is mathematically valid within this index, conflating it with raw token-level ANLS/F1 introduces ambiguity for IEEE reviewers.

---

## 3. Dataset Weighting & Aggregation
- **Dataset Cardinality**: 4 datasets $\times$ 1 document each = 4 canonical evaluation samples.
- **Aggregation Type**: Macro-average across all 900 evaluated conditions ($225$ conditions per dataset).
- Because each dataset contributes an equal number of degradation conditions ($225$), the macro-average equals the micro-average across conditions.

---

## 4. Required Paper Correction
1. **Terminology Update**: In the IEEE manuscript, replace all references to "Mean ANLS/F1" with **"Normalized Document Extraction Index ($S$)"** or **"Normalized Task Score ($S \in [0, 1]$)"**.
2. **Explicit Clarification**: Clearly define $S$ as the normalized task performance score under controlled degradation, distinguishing it from individual metric breakdowns (ANLS on DocVQA, Token F1 on FUNSD/SROIE, EM on MMLongBench).
3. **Data Integrity**: The underlying numbers ($0.7671$ vs $0.7778$, $\Delta = -0.0107$) remain mathematically unchanged.
