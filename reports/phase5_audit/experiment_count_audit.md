# PHASE 5 SCIENTIFIC AUDIT — EXPERIMENT COUNT & CARDINALITY AUDIT

**Audit Item**: Verification of Experiment Cardinality, Conditions, Runs, and Persistence  
**Audit Status**: DISCREPANCY DETECTED (P1 — Major Persistence / Trace Naming Defect)  

---

## 1. Reported Cardinality vs Actual Execution Cardinality

The Phase 5 report states:
> "Evaluated over 900 test conditions per policy (4 samples $\times$ 9 degradation families $\times$ 5 severity tiers $\times$ 5 seeds = 4,500 total policy evaluations)"

### Cardinality Breakdown:
- **Evaluation Corpus Samples**: $N = 4$ canonical document samples (1 each from DocVQA, FUNSD, SROIE, MMLongBench-Doc).
- **Degradation Families**: $K = 9$ (gaussian_blur, gaussian_noise, skew_rotation, jpeg_compression, illumination, occlusion, resolution_reduction, perspective_distortion, mixed_degradation).
- **Severity Tiers**: $S = 5$ ($S_0, S_1, S_2, S_3, S_4$).
- **Deterministic Seeds**: $R = 5$ ($42, 123, 456, 789, 101112$).
- **Benchmark Conditions**:
  $$\text{Conditions} = 4 \times 9 \times 5 \times 5 = 900 \text{ unique degradation conditions}$$
- **Deployable Routing Policies**: 5 policies (R1: Fixed Best, R2: Rule-Based, R3: Uncertainty, R4: Learned, R5: Composite).
  $$\text{Deployable Policy Evaluations} = 900 \times 5 = 4,500 \text{ evaluations}$$
- **Oracle Upper Bound (R0)**: Evaluated retrospectively across the 900 conditions = 900 evaluations.
- **Total In-Memory Policy Evaluations**: $4,500 + 900 = 5,400$ total evaluations.

The mathematical counting of conditions ($900$) and deployable evaluations ($4,500$) is **VERIFIED**.

---

## 2. Artifact Persistence Discrepancy (File Overwriting Defect)

Inspection of `experiments/phase5/` revealed a major discrepancy between the reported run count and the physical files stored on disk:
- `experiments/phase5/index.json` records **4,500 artifact references**.
- However, `experiments/phase5/routing_traces/` contains only **102 files on disk**.

### Root Cause Analysis:
In `src/routing/pipeline.py` (lines 69–70):
```python
seed = condition.seed if condition else 42
run_id = f"run_P5_{sample.dataset}_{policy.value}_{sample.sample_id}_s{seed}"
```
The `run_id` template includes `dataset`, `policy`, `sample_id`, and `seed`, but **omits `condition.family` and `condition.severity`**.
Consequently, for each (sample, policy, seed) tuple, the inner loop iterated through 9 degradation families $\times$ 5 severities = 45 degradation conditions. At every iteration, `decision_tracer.save_trace(trace)` wrote to:
`experiments/phase5/routing_traces/{run_id}_trace.json`
overwriting the file from the preceding degradation condition!

### Empirical Proof:
- Total unique (sample $\times$ policy $\times$ seed) tuples:
  $$4 \text{ samples} \times 5 \text{ policies} \times 5 \text{ seeds} = 100 \text{ unique IDs}$$
- Plus 2 initial smoke test traces = 102 physical files on disk.
- In `experiments/phase5/index.json`:
  - Total entries: 4,500
  - Unique IDs: exactly 100 (each repeated 45 times).

### Impact Assessment:
- **In-Memory Summary Integrity**: Unaffected. The in-memory Python script accumulated all 900 scores and costs into `results_by_policy` arrays and serialized `E5_ROUTING_summary.json` containing the true 900-condition aggregate.
- **On-Disk Auditability**: Compromised for individual condition traces. On-disk trace files reflect only the final executed condition (`mixed_degradation`, severity 4) for each sample and seed.
- **Severity Level**: **P1 (Major)**. Must be resolved before archiving or publication by incorporating `{family}` and `sev{severity}` into the `run_id` format.
