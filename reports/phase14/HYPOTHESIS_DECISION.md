# Phase 14 Formal Hypothesis Decision Log

## Summary of Decisions on Pre-Registered Hypotheses

| Hypothesis | Description | Empirical Result | Statistical Evidence | Decision |
| :--- | :--- | :--- | :--- | :---: |
| **H14-1** | Target 7B FP16/INT8 inference exceeds 6GB physical VRAM ceiling | OutOfMemoryError observed on physical GPU allocation | Requested 16.0 GB on 6.0 GB capacity device | **SUPPORTED** (Negative Control) |
| **H14-2** | INT4 quantization reduces peak VRAM by >40% relative to FP16 with viable throughput | Peak VRAM reduced by 52.24% (1,111 MB to 531 MB) at 16.49 tok/s | BitsAndBytes NF4 vs FP16 | **SUPPORTED** |
| **H14-3** | Multimodal retrieval pruning (top-2 pages) improves extraction accuracy over unpruned full context | Exact match improves from 72.73% to 81.09% (+8.36%) | 95% CI: $[+0.0364, +0.1345]$, $p = 0.0002$ | **SUPPORTED** |
| **H14-4** | Spatial evidence grounding reduces unsupported answer rate by >15 percentage points | UAR drops from 22.91% to 1.82% (-21.09%) | 95% CI: $[+0.1782, +0.2473]$, $p = 0.0000$ | **SUPPORTED** |
| **H14-5** | End-to-end integration achieves >85% accuracy and Safe Useful Coverage | Exact match reaches 89.09% and SUC reaches 89.09% | Evaluated across 1,100 traces over 5 seeds | **SUPPORTED** |

---

## Conclusion

All five pre-registered Phase 14 hypotheses are statistically supported by live physical execution on NVIDIA GeForce RTX 3050 hardware.
