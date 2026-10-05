# Phase 6 Report 11: Comprehensive Retrieval Metrics Breakdown

## 1. Metric Suite
Evaluation in Phase 6 adheres strictly to frozen information retrieval definitions across cutoffs $K \in \{1, 3, 5, 10, 20\}$:
- **Recall@K**: Proportion of ground-truth evidence pages present within top-$K$ candidates.
- **MRR (Mean Reciprocal Rank)**: Reciprocal rank ($1/\text{rank}$) of the first retrieved ground-truth page.
- **nDCG@10**: Normalized Discounted Cumulative Gain at rank 10 with binary relevance.
- **Evidence Region Recall**: Fraction of target sub-page bounding box regions localized.
- **VLM Page Reduction Ratio**: Proportion of total document pages pruned before VLM inference.

## 2. Benchmark Summary Table (Test Partition, $N=25$ docs, 3 Seeds, Total $N_{\text{runs}}=450$)

| Baseline ID | Baseline Name | Recall@1 | Recall@3 | Recall@5 | Recall@10 | MRR | nDCG@10 | Region Recall | VLM Reduction | Avg Latency (ms) |
|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **B6-0** | Random Page Retrieval | 0.0800 | 0.2133 | 0.3600 | 0.5867 | 0.1533 | 0.2415 | 0.0000 | 72.2% | 0.04 |
| **B6-1** | BM25 Lexical Text Retrieval | 0.8400 | 0.8400 | 0.8400 | 0.8400 | 0.8400 | 0.8400 | 0.0000 | 72.2% | 1.15 |
| **B6-2** | Dense Text Retrieval | 0.7600 | 0.7600 | 0.7600 | 0.7600 | 0.7600 | 0.7600 | 0.0000 | 72.2% | 2.80 |
| **B6-3** | Visual Feature Retrieval | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 72.2% | 1.45 |
| **B6-4** | Multimodal Hybrid Retrieval | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 72.2% | 3.20 |
| **B6-5** | Hierarchical Multimodal (Proposed) | **1.0000** | **1.0000** | **1.0000** | **1.0000** | **1.0000** | **1.0000** | **1.0000** | **72.2%** | 4.85 |

## 3. Observations
1. **Random Lower Bound**: B6-0 achieves only 21.3% Recall@3, confirming that retrieval performance is non-trivial.
2. **Lexical & Dense Degradation**: BM25 (84.0%) and Dense (76.0%) fail to retrieve evidence on severely degraded documents where OCR text is corrupted.
3. **Multimodal Robustness**: B6-4 and B6-5 leverage visual layout features to achieve 100.0% page recall across all conditions.
4. **Fine-Grained Advantage**: Only B6-5 achieves 100.0% Region Recall, delivering localized spatial bounding boxes directly to the VLM.
