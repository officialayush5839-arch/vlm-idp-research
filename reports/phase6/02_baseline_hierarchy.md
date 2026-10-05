# Phase 6 Report 02: Baseline Retrieval Hierarchy (B6-0 to B6-5)

## 1. Overview
Phase 6 establishes a rigorous comparative baseline hierarchy to isolate the specific performance contributions of lexical matching, dense semantic projections, visual layout representations, hybrid fusion, and hierarchical reranking.

## 2. Baseline Definitions

### Baseline B6-0: Random Page Retrieval
- **Mechanism**: Uniform random sampling of $K$ pages from the document without content inspection.
- **Role**: Establishes the empirical lower bound and controls for chance hit probability as document length scales.
- **Mathematical Form**:
  $$P(\text{select } p) = \frac{1}{N_{\text{total}}}$$

### Baseline B6-1: BM25 Lexical Text Retrieval
- **Mechanism**: Classical inverted index over OCR-extracted page text with Robertson-Spärck Jones IDF smoothing ($k_1=1.5, b=0.75$).
- **Role**: Measures the effectiveness and degradation vulnerability of standard keyword-based IR.

### Baseline B6-2: Dense Text Retrieval
- **Mechanism**: Unsupervised semantic text embedding using sublinear TF-IDF projected through TruncatedSVD with unit L2 normalization and cosine similarity ranking.
- **Role**: Captures semantic document relevance without reliance on exact token identity.

### Baseline B6-3: Visual Feature Retrieval
- **Mechanism**: Multi-scale spatial pyramid color/intensity descriptors and layout bounding-box distribution vectors mapped to query layout concepts (tables, figures, forms).
- **Role**: Isolates layout/visual cues independent of OCR character recognition quality.

### Baseline B6-4: Multimodal Hybrid Retrieval
- **Mechanism**: Normalized linear interpolation of lexical and visual scores:
  $$S_{\text{hybrid}} = \alpha \cdot S^{\text{norm}}_{\text{text}} + (1 - \alpha) \cdot S^{\text{norm}}_{\text{visual}}$$
  with $\alpha = 0.60$ configured strictly prior to evaluation.
- **Role**: Evaluates the synergy of combining text and visual modalities at the page level.

### Baseline B6-5: Proposed Hierarchical Multimodal Retrieval
- **Mechanism**: Full pipeline comprising:
  1. Coarse multimodal score fusion across all document pages.
  2. Cross-modal structural reranker incorporating layout affinity and region density bonuses.
  3. Fine-grained sub-page region retrieval localization ($[0, 1000]$ normalized bounding boxes).
  4. Standardized `EvidencePackage` formulation with complete cryptographic provenance.
- **Role**: Proposed research system for long-document IDP.
