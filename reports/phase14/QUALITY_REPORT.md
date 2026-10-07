# Phase 14 Extraction Quality Report

## 1. Quality Metrics Overview

Evaluation was conducted across 5 seeds on the authentic test document corpus (55 unique queries over multi-page authentic document families), generating 1,100 evaluated traces.
The primary quality metric is Exact Match (EM) accuracy on ground-truth target tokens.

---

## 2. Extraction Accuracy by Architecture Condition (`table_08_quality.csv`)

| Condition ID | Pipeline Configuration | Exact Match (Mean) | Exact Match (Std) | $\Delta$ vs Baseline |
| :--- | :--- | :---: | :---: | :---: |
| **B14-A** | Full-Document VLM (5 Pages) | 0.7273 | 0.0268 | Baseline |
| **B14-B** | Retrieval-Pruned VLM (Top-2 Pages) | 0.8109 | 0.0236 | **+0.0836** |
| **B14-C** | Retrieval + Grounding Verification | 0.8618 | 0.0209 | **+0.1345** |
| **B14-D** | Proposed (Uncertainty Abstention Gate) | 0.8909 | 0.0188 | **+0.1636** |

---

## 3. Analysis of Quality Progression

1. **Context Distraction in B14-A**: Feeding all 5 document pages directly into the VLM introduces extraneous textual and layout noise ("lost-in-the-middle" effect), depressing extraction accuracy to 72.7%.
2. **Focus via Retrieval in B14-B**: Eliminating 60% of irrelevant pages boosts accuracy by **+8.36 percentage points** (81.09%).
3. **Grounding Alignment in B14-C**: Conditioning generation on localized bounding-box visual crops further increases accuracy to **86.18%**.
4. **Selective Abstention in B14-D**: Gating low-confidence and ungrounded candidate outputs elevates effective task accuracy to **89.09%**.
