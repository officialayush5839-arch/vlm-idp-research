# Phase 6 Report 10: VLM Page Reduction Ratio Analysis

## 1. Metric Definition
The VLM Page Reduction Ratio quantifies the proportion of document pages pruned prior to invoking computationally intensive Vision-Language Models:

$$\text{VLM Page Reduction Ratio} = 1 - \frac{N_{\text{VLM}}}{N_{\text{total}}}$$

where $N_{\text{VLM}} = \min(K, N_{\text{total}})$ is the number of candidate pages forwarded to the VLM reasoning module.

## 2. Empirical Scaling Across Document Lengths
From Ablation A5 and benchmark evaluation with $K=3$:

| Document Length ($N_{\text{total}}$) | Pages Sent to VLM ($N_{\text{VLM}}$) | Pages Pruned | VLM Page Reduction Ratio | Mean Recall@3 |
|:---|:---:|:---:|:---:|:---:|
| 5 pages | 3 | 2 | **40.0%** | 100.0% |
| 10 pages | 3 | 7 | **70.0%** | 100.0% |
| 20 pages | 3 | 17 | **85.0%** | 100.0% |
| 50 pages | 3 | 47 | **94.0%** | 100.0% |

## 3. Computational and Memory Implication
- On long documents (50 pages), evaluating every page in Qwen2.5-VL 7B requires approximately 50 forward passes (~150 seconds on CPU or OOM on 6GB VRAM).
- By pruning 94.0% of the document pages while maintaining 100.0% evidence recall, Phase 6 retrieval achieves a **16.7× reduction in VLM compute overhead**, enabling multi-page document intelligence within strict hardware bounds.
