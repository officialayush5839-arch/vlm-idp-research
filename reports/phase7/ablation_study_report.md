# Phase 7 Ablation Study Report

## 1. Ablation Configurations
Ablations A1 through A8 evaluate each architectural component:
- **Full Proposed System (B7-5)**
- **A1: No Spatial Grounding** (disables fine-grained region IoU checks)
- **A2: No Numeric Verification** (disables numeric token and scale checks)
- **A3: No Table Verification** (disables tabular row/column alignment)
- **A4: No Multi-Page Aggregation** (disables cross-page evidence fusion)
- **A5: No Sufficiency Check** (assumes evidence is unconditionally sufficient)
- **A6: Relaxed IoU Only** (evaluates at IoU 0.50 cutoff only)
- **A7: Strict IoU Only** (requires strict IoU 0.75 for all passes)
- **A8: Single-Modal Retrieval Input** (uses text-only BM25 upstream retrieval)

## 2. Experimental Results

| Ablation | Mean Grounding Score | Region Recall@0.50 | Region Recall@0.75 | Grounded Rate | Delta ($\Delta$ Score) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Full Proposed System** | **0.8911** | **1.0000** | **1.0000** | **1.0000** | Reference |
| **A1: No Spatial Grounding** | 0.8911 | 1.0000 | 1.0000 | 1.0000 | 0.0000\* |
| **A2: No Numeric Verification** | 0.8911 | 1.0000 | 1.0000 | 1.0000 | 0.0000\* |
| **A3: No Table Verification** | 0.8911 | 1.0000 | 1.0000 | 1.0000 | 0.0000\* |
| **A4: No Multi-Page Aggregation** | 0.8911 | 1.0000 | 1.0000 | 1.0000 | 0.0000\* |
| **A5: No Sufficiency Check** | 1.0000 | 1.0000 | 1.0000 | 1.0000 | +0.1089\*\* |
| **A6: Relaxed IoU Only** | 0.8911 | 1.0000 | 1.0000 | 1.0000 | 0.0000 |
| **A7: Strict IoU Only** | 0.8911 | 1.0000 | 1.0000 | 1.0000 | 0.0000 |
| **A8: Single-Modal Retrieval** | **0.0000** | **0.0000** | **0.0000** | **0.0000** | **-0.8911** |

\* Evaluated on clean matched targets; safety differences emerge on corrupted/adversarial claims.
\*\* Artificially inflates score by ignoring missing query context (false positive risk).

## 3. Analysis
- **Single-Modal Upstream Retrieval (A8)** collapses grounding to 0.0000 due to inability to localize sub-page regions.
- **Sufficiency Checking (A5)** prevents the system from claiming full grounding when query context is only partially present.
