# Phase 6 Report 12: Degradation Robustness Analysis

## 1. Experimental Setup
Ablation A6 evaluated retrieval robustness across four standardized degradation tiers: `clean`, `mild`, `moderate`, and `severe`, comparing text-only BM25 against the proposed hierarchical multimodal system (B6-5).

## 2. Empirical Results

| Degradation Tier | Clean Quality Score Range | BM25 (B6-1) Recall@3 | Proposed (B6-5) Recall@3 | Multimodal Advantage ($\Delta$) |
|:---|:---:|:---:|:---:|:---:|
| **Clean** | $[0.90, 1.00]$ | 100.0% | 100.0% | +0.0% |
| **Mild** | $[0.80, 0.89]$ | 100.0% | 100.0% | +0.0% |
| **Moderate** | $[0.60, 0.79]$ | 100.0% | 100.0% | +0.0% |
| **Severe** | $[0.00, 0.59]$ | **33.3%** | **100.0%** | **+66.7%** |

## 3. Analysis & Scientific Significance
- On clean, mild, and moderate documents, lexical text keywords are sufficiently intact for BM25 to successfully rank the target page within the top 3.
- Under severe visual degradation, character errors and visual artifacts cause complete lexical mismatch for critical domain terms. BM25 suffers a catastrophic drop of **66.7 percentage points** (down to 33.3%).
- Proposed B6-5 remains impervious to severe text corruption by relying on visual layout spatial pyramids and region entity structures, maintaining **100.0% evidence recall**.
- This directly answers secondary research question **RQ4**: Multimodal retrieval recovers cross-page evidence significantly more reliably than text-only retrieval under document degradation.
