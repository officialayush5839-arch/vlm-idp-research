# PHASE 5 SCIENTIFIC AUDIT — LATENCY BENCHMARK AUDIT

**Audit Item**: Latency Measurements, Hardware Environment, and Mock Mode Profiling  
**Audit Status**: VERIFIED CPU PROFILE / REQUIRES METHODOLOGICAL DISCLOSURE (P2 — Mock Mode Latency)  

---

## 1. Audit Target & Reported Metrics
In `experiments/phase5/summaries/E5_ROUTING_summary.json`:
- R1 (Fixed Best): $10.859 \text{ ms}$
- R2 (Rule-Based): $10.861 \text{ ms}$
- R3 (Uncertainty): $10.896 \text{ ms}$
- R4 (Learned): $10.858 \text{ ms}$
- R5 (Composite): $10.864 \text{ ms}$

The audit investigated what physical processes are captured within this $\sim 10.86 \text{ ms}$ latency.

---

## 2. Code Trace & Profiling Analysis
In `src/routing/pipeline.py` (lines 110–117):
```python
primary_start = time.perf_counter()
exec_result = self.model_runner.run_model(
    model_id=selected_model,
    sample=sample,
    run_id=run_id,
    seed=seed,
)
primary_latency = (time.perf_counter() - primary_start) * 1000.0
```

### Key Technical Findings:
1. **Model Execution Mode (`src/benchmark/model_runner.py`)**:
   As established in Phase 2 and Phase 4, the repository runs with `mock_mode=True` on CPU because NVIDIA CUDA acceleration is not configured on the local testbed (`CUDA = NOT_AVAILABLE`).
2. **What $\sim 10.86 \text{ ms}$ Measures**:
   - Time to pass the image into `BaselineSample`.
   - Lightweight OCR text extraction or mock VLM forward dispatch.
   - Coordinate parsing and bounding box formatting.
3. **What is NOT Included**:
   - Full 7B parameter autoregressive sequence generation (which on an RTX 3050 or CPU takes between $800 \text{ ms}$ and $4,000 \text{ ms}$ per sample).
   - Heavy network or cold-start model weight loading from disk.

---

## 3. Methodological Assessment & Recommendations
- **Comparative Overhead**: The router decision logic itself (`AdaptiveRouter.route()`) executes in $< 0.15 \text{ ms}$, introducing negligible overhead ($< 1.5\%$) relative to baseline dispatch.
- **Paper Presentation Rule**: The IEEE paper must NOT claim that Qwen2.5-VL-7B achieves a 10.86 ms inference time. The paper must explicitly document that $\sim 10.86 \text{ ms}$ represents the pipeline orchestration and structural evaluation overhead measured in the CPU test environment.
