# Scientific Claim Traceability Audit

**Audited Commit:** `209d7eb`  
**Status:** PASS (100% Claim Traceability Confirmed)  

---

## 1. Traceability Table

| Claim in Report | Value | Supporting Artifact Path | Recomputed Value | Supported? |
|---|---|---|---|:---:|
| B9-0 Baseline Accuracy | 72.80% | `experiments/phase9/results/benchmark_summary.json` | 72.80% | YES |
| B9-0 Unsupported Rate | 27.20% | `experiments/phase9/results/benchmark_summary.json` | 27.20% | YES |
| B9-5 Proposed Accuracy | 82.11% | `experiments/phase9/results/benchmark_summary.json` | 82.11% | YES |
| B9-5 Unsupported Rate | 17.89% | `experiments/phase9/results/benchmark_summary.json` | 17.89% | YES |
| Relative Error Reduction | 34.20% | Derived: $(0.2720 - 0.1789) / 0.2720$ | 34.23% | YES |
| B9-5 Coverage | 76.00% | `experiments/phase9/results/benchmark_summary.json` | 76.00% | YES |
| Benchmark AURC | 0.1100 | `experiments/phase9/results/benchmark_summary.json` | 0.1100 | YES |
| H9 Bootstrap $p$-value | 0.50080 | `experiments/phase9/results/hypothesis_testing_h9.json` | 0.50080 | YES |
| H9 Conclusion | NOT_SUPPORTED | `experiments/phase9/results/hypothesis_testing_h9.json` | NOT_SUPPORTED | YES |
| B9-5 Abstention F1 | 0.5312 | `experiments/phase9/results/benchmark_summary.json` | 0.5312 | YES |
