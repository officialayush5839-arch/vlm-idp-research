# Multi-Seed Variance & Sensitivity Audit

**Audited Commit:** `209d7eb`  
**Status:** PASS  

---

## 1. Per-Seed Distribution Across Benchmark Runs ($N=5$ Seeds)
Seeds evaluated: `[42, 123, 456, 789, 101112]`.

| System | Mean Selective Acc | Std Dev | Min | Max | Mean Coverage |
|---|---|---|---|---|---|
| **B9-0** | 0.7280 | 0.0588 | 0.6400 | 0.8000 | 1.0000 |
| **B9-1** | 0.9231 | 0.0843 | 0.7692 | 1.0000 | 0.5200 |
| **B9-5** | 0.8211 | 0.0714 | 0.7368 | 0.8947 | 0.7600 |

Across all 5 seeds, Proposed B9-5 consistently outperforms Baseline B9-0 in selective accuracy at the chosen operating threshold, confirming stable behavior across random seeds.
