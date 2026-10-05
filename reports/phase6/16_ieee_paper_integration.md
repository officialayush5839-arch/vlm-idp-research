# Phase 6 Report 16: IEEE Paper Integration Plan

## 1. Mapping to IEEE Manuscript Sections

### Section IV: Methodology
- **Subsection IV-C: Hierarchical Multimodal Retrieval for Long Documents**
  - Formulation of coarse-to-fine indexing (`src/retrieval/page_index.py`).
  - Robertson-Spärck Jones BM25 with text-visual score fusion ($\alpha=0.60$).
  - Structural cross-modal reranker and fine-grained region localization in normalized $[0, 1000]$ integer coordinate space.
  - Mathematical formalization of VLM Page Reduction Ratio ($1 - N_{\text{VLM}}/N_{\text{total}}$).

### Section V: Experimental Setup
- **Subsection V-B: Retrieval Baselines & Benchmark Corpus**
  - Formal definitions of B6-0 through B6-5.
  - Multi-page document collection with varying lengths (5, 10, 20, 50 pages) and degradation levels.
  - Paired bootstrap hypothesis testing ($B=10,000$) with 95% confidence intervals and Cohen's $d$.

### Section VI: Empirical Results & Evaluation
- **Subsection VI-C: Long-Document Retrieval & VLM Compute Reduction**
  - Table of Recall@K, MRR, nDCG@10, Region Recall, and Page Reduction.
  - Evidence of degradation robustness: +66.7% recall advantage over BM25 on severely degraded documents.
  - Formal validation of Hypothesis H4 ($p = 0.0486$ vs BM25, $p < 0.0001$ vs Random).

### Section VII: Ablation Studies
- Presentation of Ablations A1 through A8 showing the impact of modality fusion, cutoff $K$, and scaling to 50 pages (94% page reduction).
