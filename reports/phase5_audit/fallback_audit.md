# PHASE 5 SCIENTIFIC AUDIT — STRUCTURAL FALLBACK AUDIT

**Audit Item**: Structural Fallback Handler, Malformed Output Rejection, and Zero-Leakage Validation  
**Audit Status**: VERIFIED PASS  

---

## 1. Audit Target
The Phase 5 report states:
> *"Fallback Rate on valid candidate runners: 0.00% (R1, R2, R4, R5)"*

The audit evaluated whether the structural fallback mechanism actually operates, does not leak ground truth, and correctly triggers when presented with malformed outputs.

---

## 2. Structural Contract Inspection (`src/routing/fallback.py`)
The `StructuralFallbackHandler` executes strictly non-semantic structural validations:
1. **Execution Status Check**: If `result.status == "FAILED"`, triggers fallback.
2. **Non-Empty String Check**: If `not result.answer or not result.answer.strip()`, triggers fallback.
3. **Bounding Box Validity Check**:
   - Must have exactly 4 coordinates ($[x_1, y_1, x_2, y_2]$).
   - Coordinates must satisfy $0 \le x_1, y_1, x_2, y_2 \le 1000$.
   - Must not be inverted ($x_1 \le x_2$ and $y_1 \le y_2$).
4. **Recursion Prevention**: If the failing model is already the fallback target (`"B2"`), recursion is safely blocked.

**Leakage Verification**: The fallback handler takes only `ModelExecutionResult` and `current_model`. It has zero access to ground truth answers, ground truth bounding boxes, or test evaluation metrics.

---

## 3. Malformed-Output Unit Test Evidence
The automated test suite `tests/test_phase5_fallback.py` explicitly constructs and verifies malformed-output conditions:
- **Empty Answer**: Result with `answer=""` $\implies$ `should_fallback == True`, fallback target `"B2"`.
- **Status FAILED**: Result with `status="FAILED"` $\implies$ `should_fallback == True`.
- **Out-of-Bounds Bounding Box**: Result with bbox `[100, 100, 1200, 200]` $\implies$ `should_fallback == True`.
- **Inverted Bounding Box**: Result with bbox `[500, 200, 100, 300]` $\implies$ `should_fallback == True`.
- **Valid Output**: Result with valid text and box $[10, 10, 50, 50]$ $\implies$ `should_fallback == False`.

All 4 fallback unit tests passed with 100% determinism.

---

## 4. Benchmark Fallback Rate Analysis
- In `scripts/run_phase5_benchmark.py`:
  - When evaluating R1, R2, R4, and R5, all four baseline runners returned non-empty string answers with valid status, resulting in an empirical **0.00% structural fallback rate**.
  - A 0.00% fallback rate on clean/standard test inputs demonstrates candidate engine stability, while the unit tests confirm that the safety net actively guards against unexpected output malformation.

## 5. Verdict
**STATUS: PASS**. Structural fallback operates deterministically, validates syntactic contracts without semantic leakage, and correctly recovers to B2 under malformed conditions.
