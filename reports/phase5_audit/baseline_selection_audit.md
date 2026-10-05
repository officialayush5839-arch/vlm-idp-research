# PHASE 5 SCIENTIFIC AUDIT — FIXED BASELINE SELECTION (R1) AUDIT

**Audit Item**: Selection Protocol and Pre-Specification of R1 (Fixed Best Baseline = B2)  
**Audit Status**: VERIFIED PASS  

---

## 1. Audit Objective
The audit investigated whether selecting **B2 (Qwen2.5-VL 7B Vision-Only)** as the control baseline ($R_1$) involved test-set model selection leakage or retrospective post-hoc cherry-picking after observing Phase 5 test results.

---

## 2. Selection Lineage & Provenance
1. **Phase 2 & Phase 2.5 Baselines**:
   - Initialized B0 (Conventional OCR: PaddleOCR/Tesseract), B1 (OCR+VLM), B2 (VLM-only), and B0-U (Unlimited-OCR).
2. **Phase 4 Controlled Degradation Benchmark**:
   - Evaluated all 4 baselines across 3,600 conditions.
   - Empirical findings in `reports/phase4/PHASE4_REPORT.md` (Section 15, Table 3) demonstrated that:
     - B0 collapses under geometric corruptions (skew $\Delta = -0.55$, perspective $\Delta = -0.58$) and severe blur.
     - B1 suffers from OCR error propagation under noise and blur.
     - **B2 demonstrated the highest overall robustness floor** across the complete 9-family degradation spectrum.
3. **Phase 5 Pre-Specification**:
   - `configs/phase5/routing_config.yaml` explicitly codified B2 prior to running Phase 5:
     ```yaml
     default_fixed_baseline: "B2"
     ```
   - Git log verification confirms that `configs/phase5/routing_config.yaml` was authored and staged prior to running `scripts/run_phase5_benchmark.py`.

---

## 3. Retrospective Validation on Test Set
Retrospective analysis on Phase 5 test data confirms that B2 was indeed the single highest-scoring unconditional fixed candidate:
- Unconditional B0 Mean Score: 0.4289
- Unconditional B1 Mean Score: 0.5178
- Unconditional B0-U Mean Score: 0.6356
- **Unconditional B2 Mean Score: 0.7778**

Because B2 was the actual single best fixed system, comparing R2 against R1 represents a rigorous and honest control, avoiding "strawman" baseline comparisons.

## 4. Verdict
**STATUS: PASS**. Selection of B2 as the fixed baseline was pre-specified from Phase 4 experimental evidence, documented in frozen configuration, and represents a scientifically sound control baseline.
