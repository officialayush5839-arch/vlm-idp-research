# Phase 14 Failure-Safety & Hallucination Mitigation Report

## 1. Safety Metrics Definition

1. **Unsupported Answer Rate (UAR)**: The proportion of non-abstaining responses whose generated answer contradicts or lacks visual support in the identified source evidence.
2. **Safe Useful Coverage (SUC)**: The proportion of total queries correctly answered without incurring unsupported hallucinations:
   $$\text{SUC} = \frac{N_{\text{correct}} - N_{\text{unsupported}}}{N_{\text{total}}}$$

---

## 2. Safety Metric Results (`table_10_safety.csv`)

| Condition ID | Pipeline Configuration | Unsupported Answer Rate (UAR) | Safe Useful Coverage (SUC) |
| :--- | :--- | :---: | :---: |
| **B14-A** | Full-Document VLM | 0.2291 (22.91%) | 0.7273 (72.73%) |
| **B14-B** | Retrieval-Pruned VLM | 0.0473 (4.73%) | 0.8109 (81.09%) |
| **B14-C** | Retrieval + Grounding | 0.0182 (1.82%) | 0.8618 (86.18%) |
| **B14-D** | Full Proposed (Abstention Gate) | **0.0109 (1.09%)** | **0.8909 (89.09%)** |

---

## 3. Analysis & Safety Implications

- **The Hallucination Danger of B14-A**: Feeding raw long documents directly into a VLM without verification resulted in a **22.91% unsupported answer rate**, an unacceptable risk for enterprise compliance and document verification workflows.
- **Suppression via Grounding (B14-C)**: Enforcing that answers must bind to verified visual regions dropped UAR from 22.91% to 1.82% (**a 92.1% relative reduction in hallucinations**).
- **The Final Abstention Gate (B14-D)**: Applying the calibrated confidence and IoU threshold abstains on ambiguous edge cases, pushing UAR down to **1.09%** while elevating Safe Useful Coverage to **89.09%**.
