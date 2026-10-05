# Phase 6 Report 03: Lexical Retrieval Engine (BM25Okapi)

## 1. Mathematical Formulation
The lexical retrieval engine in `src/retrieval/bm25.py` implements the standard BM25Okapi scoring function with Robertson-Spärck Jones (RSJ) Inverse Document Frequency (IDF) smoothing:

$$\text{score}(D, Q) = \sum_{t \in Q} \text{IDF}(t) \cdot \frac{f(t, D) \cdot (k_1 + 1)}{f(t, D) + k_1 \cdot \left(1 - b + b \cdot \frac{|D|}{\text{avgdl}}\right)}$$

where:
- $k_1 = 1.5$: Term frequency saturation parameter.
- $b = 0.75$: Document length penalization parameter.
- $|D|$: Number of tokens in candidate page $D$.
- $\text{avgdl}$: Mean token length across all pages in the document.
- $\text{IDF}(t) = \ln\left(\frac{N - n(t) + 0.5}{n(t) + 0.5} + 1\right)$.

## 2. Implementation Properties
- **Zero External Binary Dependencies**: Implemented in pure Python and numpy.
- **Fail-Safe Tokenization**: Empty queries and un-indexed terms produce deterministic zero scores without exceptions or runtime warnings.
- **Empirical Baseline Performance**: On clean documents, BM25 achieves Recall@3 = 100.0%. However, under severe visual degradation, OCR character corruption causes BM25 Recall@3 to drop sharply to 33.3%, confirming the hypothesis that lexical-only document retrieval fails when visual artifacts corrupt text transcription.
