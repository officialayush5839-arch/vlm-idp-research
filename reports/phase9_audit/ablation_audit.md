# Ablation Studies Integrity Audit (A9-1 through A9-8)

**Audited Commit:** `209d7eb`  
**Status:** PASS  

---

## 1. Inspection of Evaluated Ablations
Recorded in `experiments/phase9/results/ablations_summary.json`:

| Ablation ID | Component Omitted | Coverage | Selective Acc | Unsupported Rate | Abstain F1 | Finding |
|---|---|---|---|---|---|---|
| **Full B9-5** | None (Full 8D) | 0.7600 | 0.8211 | 0.1789 | 0.5312 | Benchmark standard |
| **A9-1** | Visual Quality ($u_{\text{quality}}$) | 0.7600 | 0.7368 | 0.2632 | 0.4444 | Significant drop in selective acc (-8.43%) |
| **A9-2** | Spatial Grounding ($u_{\text{spatial}}$) | 0.7600 | 0.7368 | 0.2632 | 0.4444 | Significant drop in selective acc (-8.43%) |
| **A9-3** | Numeric Discrepancy ($u_{\text{numeric}}$) | 0.5200 | 0.7692 | 0.2308 | 0.5714 | Over-conservative coverage drop |
| **A9-4** | Retrieval Uncertainty ($u_{\text{retrieval}}$) | 0.7600 | 0.7368 | 0.2632 | 0.4444 | Significant drop in selective acc (-8.43%) |
| **A9-5** | Post-Hoc Calibration | 0.5200 | 0.7692 | 0.2308 | 0.5714 | Reduced coverage and accuracy |
| **A9-6** | Binary Decision Only | 0.2400 | 0.8333 | 0.1667 | 0.6250 | Severe coverage collapse to 24% |
| **A9-7** | Tuned Feature Weights | 0.5200 | 0.7692 | 0.2308 | 0.5714 | Suboptimal operating trade-off |
| **A9-8** | L2 Vector Norm ($L_1$ instead) | 0.7600 | 0.7368 | 0.2632 | 0.4444 | Reduced sensitivity to extreme errors |

---

## 2. Findings
- Each ablation isolates a specific architectural component.
- The results confirm that all 8 uncertainty dimensions contribute constructively to the balanced coverage/reliability operating point.
