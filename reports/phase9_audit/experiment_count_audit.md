# Phase 9 Experiment Cardinality & Accounting Audit

**Audited Commit:** `209d7eb`  
**Status:** PASS (100% Cardinality Match)  

---

## 1. Mathematical Formulation of Expected Runs
Under Phase 9 specification:
- Test documents in `corpus_manifest.json`: $N_{\text{doc}} = 25$
- Test queries: $N_{\text{query}} = 25$
- Random seeds: $S = [42, 123, 456, 789, 101112]$ ($|S| = 5$)
- Systems evaluated: 6 baselines (B9-0, B9-1, B9-2, B9-3, B9-4, B9-5)

$$\text{Expected Traces per Baseline} = 25 \times 5 = 125$$
$$\text{Expected Total Traces} = 6 \times 125 = 750$$

---

## 2. Empirical Verification
- **Observed Trace Files on Disk:** 750
- **Traces by Baseline:**
  - B9-0: 125
  - B9-1: 125
  - B9-2: 125
  - B9-3: 125
  - B9-4: 125
  - B9-5: 125
- **Collision Count:** 0
- **Duplicate Count:** 0
- **Missing Count:** 0
- **Classification:** **PASS**
