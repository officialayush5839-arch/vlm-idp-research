# Phase 14 Neural Inference Latency & Profiling Report

## 1. Timing Methodology & Synchronization

All timing in Phase 14 was conducted via `src.phase14.timing.PhysicalStageProfiler`.
To avoid asynchronous kernel launch distortion on CUDA, explicit hardware synchronizations (`torch.cuda.synchronize()`) were enforced before and after every measured forward pass and generation stage.

```python
torch.cuda.synchronize()
t_start = time.perf_counter()
output_ids = model.generate(**inputs, max_new_tokens=24, do_sample=False)
torch.cuda.synchronize()
t_end = time.perf_counter()
latency = t_end - t_start
```

---

## 2. Latency Across Precision Levels

- **FP16 Mean Latency**: $0.8629 \pm 0.041 \text{ s}$ ($27.81 \text{ tok/s}$)
- **INT8 Mean Latency**: $2.8021 \pm 0.112 \text{ s}$ ($8.57 \text{ tok/s}$)
- **INT4 Mean Latency**: $1.4551 \pm 0.068 \text{ s}$ ($16.49 \text{ tok/s}$)

---

## 3. End-to-End Pipeline Latency Scaling (`table_11_retrieval_efficiency.csv`)

| Architecture Condition | Average Pages Processed | Mean Pipeline Latency (s) | Relative Latency vs Unpruned Baseline |
| :--- | :---: | :---: | :---: |
| **B14-A (Full-Doc Unpruned)** | 5.0 pages | 7.485 s | 100.0% (Baseline) |
| **B14-B (Retrieval-Pruned)** | 2.0 pages | 3.752 s | **50.1% (-49.9% reduction)** |
| **B14-C (Retrieval + Grounding)** | 2.0 pages | 3.751 s | **50.1% (-49.9% reduction)** |
| **B14-D (Full Proposed)** | 2.0 pages | 3.749 s | **50.1% (-49.9% reduction)** |

### Key Insight:
Pruning irrelevant pages via multimodal retrieval reduces input token length from $\sim 390$ tokens to $\sim 156$ tokens, cutting end-to-end neural forward time in half ($7.485\text{s} \to 3.750\text{s}$). Grounding verification and uncertainty score computation introduce negligible overhead ($< 2 \text{ ms}$) relative to autoregressive token generation.
