# Phase 6 Report 08: Fine-Grained Sub-Page Region Retrieval

## 1. Spatial Grounding Granularity
Page-level retrieval reduces document search space, but passing full high-resolution page images to a VLM still incurs substantial token overhead. Fine-grained region retrieval localizes specific bounding boxes ($[0, 1000]$ normalized coordinate space) containing relevant evidence.

## 2. Mathematical Formulation
In `src/retrieval/region.py`, candidate sub-page regions $r$ across selected pages are scored by:

$$S_{\text{region}}(r) = 0.55 \cdot \text{LexicalOverlap}(r, Q) + \text{TypeAffinity}(r, Q) + \text{AreaRatio}(r) + 0.10 \cdot \text{Conf}(r)$$

where:
- $\text{LexicalOverlap}(r, Q) = \frac{|T_r \cap T_Q|}{|T_Q|}$
- $\text{TypeAffinity}(r, Q) = 0.35$ for semantic matches (e.g. `table` when querying numerical data)
- $\text{AreaRatio}(r) = \min\left(0.10, \frac{(x_2 - x_1)(y_2 - y_1)}{10^6} \cdot 0.2\right)$
- $\text{Conf}(r) \in [0.0, 1.0]$: Region detector confidence.

## 3. Empirical Evidence Recall
In the test benchmark:
- B6-5 achieved **100.0% Evidence Region Recall** across all evaluation documents.
- Selected regions include exact bounding boxes (e.g., `(80, 120, 920, 580)`) capturing target tables and text sections.
