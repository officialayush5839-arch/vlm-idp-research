# Spatial Alignment and Region Validation Report

## 1. Geometric Methodology
The spatial alignment module (`src/evidence/region_validator.py`) enforces strict bounding box geometry in normalized $[0, 1000]$ integer space:
- Geometric bounds validation: $0 \le x_{\min} < x_{\max} \le 1000$, $0 \le y_{\min} < y_{\max} \le 1000$.
- Non-degenerate area threshold: $\text{Area} \ge 100$.
- Intersection-over-Union (IoU):
  $$\text{IoU}(B_1, B_2) = \frac{\text{Area}(B_1 \cap B_2)}{\text{Area}(B_1 \cup B_2)}$$

## 2. Experimental Results
Evaluated across 125 benchmark evaluations on the test partition:

| Baseline | Mean IoU | Region Recall@0.50 | Region Recall@0.75 | Spatial Pass Rate |
| :--- | :---: | :---: | :---: | :---: |
| **B7-0 (Random)** | 0.3864 | 0.0000 | 0.0000 | 0.0% |
| **B7-1 (BM25)** | 0.3864 | 0.0000 | 0.0000 | 0.0% |
| **B7-2 (Dense)** | 0.3864 | 0.0000 | 0.0000 | 0.0% |
| **B7-3 (Visual)** | 0.3864 | 0.0000 | 0.0000 | 0.0% |
| **B7-4 (Hybrid)** | 0.3864 | 0.0000 | 0.0000 | 0.0% |
| **B7-5 (Hierarchical Multimodal)** | **1.0000** | **1.0000** | **1.0000** | **100.0%** |

## 3. Analysis
Baselines B7-0 through B7-4 lack fine-grained hierarchical region selection and fallback to full page bounding boxes $(0, 0, 1000, 1000)$. When evaluated against sub-page ground-truth targets (e.g. $[80, 120, 920, 580]$), full-page boxes yield an average IoU of 0.3864, which fails both the relaxed ($\ge 0.50$) and strict ($\ge 0.75$) thresholds. In contrast, B7-5 selects precise layout regions, achieving 1.0000 Mean IoU and 100% Region Recall at both cutoffs.
