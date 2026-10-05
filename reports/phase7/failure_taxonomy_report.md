# Grounding Failure Taxonomy and Error Distribution Report

## 1. Failure Categories
1. `RETRIEVAL_MISS`: No candidate page or region retrieved containing the target information.
2. `SPATIAL_BOUNDARY_MISS`: Target page retrieved, but bounding box fails relaxed IoU ($\text{IoU} < 0.50$).
3. `SEMANTIC_SUPPORT_FAILURE`: Region retrieved, but text snippet fails lexical/semantic support ($\text{Score} < 0.50$).
4. `NUMERIC_MISMATCH`: Answer numeric figure or unit differs from evidence snippet.
5. `INSUFFICIENT_EVIDENCE`: Supporting evidence lacks essential query entities.
6. `SUCCESS_GROUNDED`: Fully grounded with passing spatial, semantic, and sufficiency checks.

## 2. Quantitative Distribution across Baselines

| Failure Category | B7-0 (Random) | B7-1 (BM25) | B7-2 (Dense) | B7-3 (Visual) | B7-4 (Hybrid) | B7-5 (Proposed) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **RETRIEVAL_MISS** | 0 | 0 | 0 | 0 | 0 | 0 |
| **INSUFFICIENT_EVIDENCE** | 109 | 70 | 85 | 60 | 70 | 0 |
| **SPATIAL_BOUNDARY_MISS** | 16 | 55 | 40 | 65 | 55 | 0 |
| **SEMANTIC_SUPPORT_FAILURE** | 0 | 0 | 0 | 0 | 0 | 0 |
| **NUMERIC_MISMATCH** | 0 | 0 | 0 | 0 | 0 | 0 |
| **SUCCESS_GROUNDED** | 0 | 0 | 0 | 0 | 0 | **125 (100%)** |

## 3. Findings
Baselines B7-0 through B7-4 fail predominantly due to either missing query entities in the retrieved snippets (`INSUFFICIENT_EVIDENCE`) or falling back to full-page boxes that miss sub-page boundaries (`SPATIAL_BOUNDARY_MISS`). B7-5 completely eliminates both failure modes.
