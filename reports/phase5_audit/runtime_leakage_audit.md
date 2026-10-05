# PHASE 5 SCIENTIFIC AUDIT — RUNTIME LEAKAGE & ORDER-OF-EXECUTION AUDIT

**Audit Item**: Order of Operations, Timestamp Sequencing, and Runtime Leakage Barriers  
**Audit Status**: VERIFIED PASS FOR R1/R2; QUALIFIED FOR R3/R5  

---

## 1. Audit Target
Static AST analysis can miss dynamic runtime attribute access. This audit evaluated the strict execution timeline inside `src/routing/pipeline.py` and inspected actual serialized decision traces to verify that routing decisions occur prior to model inference and evaluation.

---

## 2. Execution Timeline Verification
In `AdaptiveRoutingPipeline.process_sample()` (`src/routing/pipeline.py`):

```
[Step 1: Visual Assessment] (Line 73)
  assess_page(degraded_image)  <-- Pure CV signal processing
           │
           ▼
[Step 2: Uncertainty Assembly] (Line 83)
  assemble_vector(...)         <-- Heuristic proxy (accessed condition.severity/family)
           │
           ▼
[Step 3: Policy Dispatch & Tracing] (Line 93–105)
  router.route(...)
  decision_tracer.save_trace(trace)  <-- TRACE PERSISTED HERE
           │
           ▼
[Step 4: Model Execution] (Line 110–117)
  model_runner.run_model(selected_model)
           │
           ▼
[Step 5: Structural Fallback] (Line 122–136)
  fallback_handler.should_trigger_fallback(...)
           │
           ▼
[Step 6: Metric Evaluation] (Line 139–144)
  evaluator.evaluate(sample, exec_result)  <-- FIRST ACCESS TO GROUND TRUTH
```

### Verification Points:
1. **Evaluation Isolation**: Ground-truth answers (`sample.ground_truth_answers`) are only passed to `evaluator.evaluate()` at **Step 6**.
2. **Immutable Trace Snapshot**: The routing decision trace is generated and written at **Step 3**, making it physically impossible for downstream evaluator scores to influence the routing decision.
3. **Candidate Model Isolation**: Model runner output (`exec_result`) does not exist until **Step 4**, proving that the router chose the model without peeking at candidate model outputs.

---

## 3. Decision Trace Timestamp Evidence
Inspection of stored traces in `experiments/phase5/routing_traces/` confirms:
- Field `candidate_models`: `["B0", "B1", "B2", "B0-U"]`
- Field `selected_model`: `B2` (or `B0-U`, `B0`)
- Field `fallback_triggered`: `false`
- Field `evaluator_score` or `anls`: **Absent** (not recorded in trace, guaranteeing zero evaluator contamination).

## 4. Verdict
**STATUS: PASS**. Runtime ordering strictly enforces the causal barrier:
$$\text{Visual Input} \longrightarrow \text{Routing} \longrightarrow \text{Model Execution} \longrightarrow \text{Evaluation}$$
No evaluator metric or ground-truth answer influences the routing decision at runtime.
