# Phase 6 Report 07: Cross-Modal Structural Reranker

## 1. Purpose & Pipeline Position
The Cross-Modal Reranker (`src/retrieval/reranker.py`) operates as Stage 3 of the retrieval pipeline. It takes coarse candidate pages ($K \ge 5$) from multimodal fusion and produces an evidence-dense subset ($M=3$) for downstream processing.

## 2. Reranking Scoring Formulation
For candidate page $p$ with coarse score $S_{\text{coarse}}(p)$:

$$S_{\text{rerank}}(p) = S_{\text{coarse}}(p) + w_{\text{align}} \cdot \left(\text{Bonus}_{\text{density}} + \text{Bonus}_{\text{type}}\right) - \text{Penalty}_{\text{diversity}}$$

where:
- $w_{\text{align}} = 0.35$ (structural alignment weight)
- $\text{Bonus}_{\text{density}} = \min(0.10, N_{\text{regions}} \cdot 0.02)$ (rewards pages with structured content)
- $\text{Bonus}_{\text{type}} = 0.15$ if candidate page contains target structural entity (e.g., table for table queries)
- $\text{Penalty}_{\text{diversity}} = 0.05$ if adjacent to already selected top candidate

## 3. Empirical Results
Ablation A4 evaluated the reranker:
- Both with and without the reranker, top candidate Recall@3 remained 100.0%.
- The reranker provided fine-grained score separation and prioritized structured evidence pages with tables and figures over plain text narrative pages.
