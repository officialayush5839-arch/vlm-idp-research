# PHASE 5 SCIENTIFIC AUDIT — LEARNED ROUTER (R4) AUDIT

**Audit Item**: Design, Training, Serialization, and Benchmark Evaluation of R4 (Learned Quality Router)  
**Audit Status**: DISCONNECTED / INVALID BENCHMARK EXECUTION (P1 — Major Implementation Defect)  

---

## 1. Design & Training Inspection
- **Source Module**: `src/routing/learned_router.py`
- **Model Class**: Scikit-Learn `LogisticRegression(C=1.0, max_iter=1000, random_state=42)`
- **Training Procedure**: Executed in `scripts/run_phase5_validation.py`.
- **Training Partition**: Explicitly restricted to `partition="val"`. Fitting on `partition="test"` is strictly blocked by a fatal `ValueError`.
- **Feature Generation**: Features were generated as $N=100$ random uniform samples in $[0, 1]^{10}$ (`np.random.uniform(0.0, 1.0, size=(100, 10))`), representing the 10 quality dimensions.
- **Target Assignment**: Targets were assigned heuristically via rule logic (if skew/perspective $> 0.40 \implies \text{B2}$; if compression $> 0.50 \implies \text{B0-U}$; if clean $\implies \text{B0}$; else B1).
- **Leakage Status**: Leakage-free (no test set data was used during fitting).

---

## 2. Serialization & Benchmark Deployment Defect

A critical defect was discovered during the audit of the deployment pipeline:
1. In `scripts/run_phase5_validation.py`, `learned_router` was fitted in memory, but **was never serialized to disk** (no pickle, joblib, or JSON weights saved).
2. In `scripts/run_phase5_benchmark.py`, `pipeline = AdaptiveRoutingPipeline.create_default()` was invoked.
3. `AdaptiveRoutingPipeline.create_default()` instantiates `RoutingPolicyManager.from_configs()`, which executes:
   ```python
   self.learned_router = learned_router or LearnedQualityRouter()
   ```
   This created a freshly instantiated, **unfitted** `LearnedQualityRouter` instance (`self.is_fitted = False`).
4. In `src/routing/learned_router.py` (lines 57–58):
   ```python
   if not self.is_fitted:
       return "B2", "Learned router uninitialized; defaulting to robust fixed baseline B2.", 0.50
   ```
5. When `R4_LEARNED` was evaluated across all 900 benchmark conditions, it hit this uninitialized fallback branch on 100% of samples!

### Conclusive Audit Proof:
- **Decision Trace Inspection**:
  Every stored R4 decision trace (e.g., `experiments/phase5/routing_traces/run_P5_DocVQA_R4_LEARNED_docvqa_s01_s42_trace.json`) explicitly logs:
  ```json
  "selected_model": "B2",
  "decision_reason": "Learned router uninitialized; defaulting to robust fixed baseline B2.",
  "router_confidence": 0.5
  ```
- **Benchmark Metrics**:
  In `experiments/phase5/summaries/E5_ROUTING_summary.json`:
  - R1 (Fixed Best B2): Mean score = **0.7778**, Std = **0.1582**, Compute = **1.0000**
  - R4 (Learned Router): Mean score = **0.7778**, Std = **0.1582**, Compute = **1.0000**
  - Model selection distribution for R4: B0=0, B1=0, B2=900, B0-U=0.

---

## 3. Scientific Evaluation & Recommendations
- **Classification**: **INVALID BENCHMARK EXECUTION**.
- **Claimed in Report**: "R4 (Learned Router): Logistic classifier trained on validation model selection outcomes."
- **Fact**: The learned model was never loaded during benchmark execution; R4 operated as an exact duplicate of R1 (Fixed Best B2).
- **Paper Impact**: The IEEE paper must NOT claim that a learned logistic router matched R1 performance through learned decision boundaries. It must either state that R4 was uninitialized or retrain and properly persist the model before final camera-ready submission.
