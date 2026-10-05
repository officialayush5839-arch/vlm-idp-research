# Phase 6 Interface Audit for Phase 7 Evidence Grounding

**Audit Date:** 2026-10-05  
**Auditor:** Antigravity Research Agent  
**Status:** **PASS / IMMUTABLE BASELINE CONFIRMED**  
**Target Repository:** `vlm-idp-research`  
**Referenced Phase 6 Commit:** `afdd599`  

---

## 1. Executive Summary
This audit inspects the frozen Phase 6 retrieval subsystem to establish exact programmatic interfaces, coordinate conventions, schema structures, and data flows before implementing Phase 7 Evidence Grounding. In accordance with Section 3.1, Phase 6 modules (`src/retrieval/`, `experiments/phase6/`, `reports/phase6/`, and `tests/test_phase6_*`) are frozen and immutable. All Phase 7 capabilities will reside in `src/evidence/` and consume Phase 6 outputs through non-invasive adapters.

---

## 2. Interface Specifications

### 2.1 `EvidencePackage` (Phase 6 Schema)
Located in `src/retrieval/schema.py`:
- `package_id: str` (e.g. `pkg_run_P6_synthetic_multipage_b6_5_doc_mp_001_q_doc_mp_001_s42`)
- `document_id: str`
- `query_id: str`
- `retrieval_method: str` (`B6-0` through `B6-5`)
- `top_k_pages_requested: int`
- `top_m_regions_requested: int`
- `total_document_pages: int`
- `selected_pages: List[PageRetrievalResult]`
- `selected_regions: List[RegionRetrievalResult]`
- `vlm_page_reduction_ratio: float`
- `provenance: Dict[str, Any]`

### 2.2 `PageRetrievalResult`
- `page_number: int` (1-indexed)
- `score: float`
- `text_score: float`
- `visual_score: float`
- `rank: int` (1-indexed)
- `metadata: Dict[str, Any]`

### 2.3 `RegionRetrievalResult`
- `region_id: str`
- `page_number: int` (1-indexed)
- `bbox: Tuple[int, int, int, int]` in $[0, 1000]$ normalized coordinate space
- `region_type: str` (`text`, `table`, `figure`, `form`, `header`, `footer`, `mixed`)
- `score: float`
- `rank: int`
- `snippet: str`

### 2.4 `DocumentPageRecord` and `DocumentRegionRecord`
- Page records include `document_id`, `page_number`, `split`, `raw_text`, `clean_text`, `quality_score`, `degradation_level`, `regions`.
- Region records strictly validate coordinates: $0 \le x_{\min} \le x_{\max} \le 1000$, $0 \le y_{\min} \le y_{\max} \le 1000$.

---

## 3. Coordinate System & Normalization Convention
- All bounding box coordinates throughout Phase 6 and Phase 7 use the **normalized integer $[0, 1000]$ coordinate space**:
  $$\text{bbox} = (x_{\min}, y_{\min}, x_{\max}, y_{\max})$$
- Conversion to pixel space:
  $$x_{\text{pixel}} = \text{round}\left(x_{1000} \cdot \frac{W_{\text{pixel}}}{1000}\right), \quad y_{\text{pixel}} = \text{round}\left(y_{1000} \cdot \frac{H_{\text{pixel}}}{1000}\right)$$
- Spatial overlap is evaluated via Intersection-over-Union (IoU) directly in this coordinate space.

---

## 4. Cryptographic Provenance & Trace Format
- Phase 6 trace format: `run_P6_{dataset}_{method}_{doc}_{query}_s{seed}`
- Phase 7 trace format: `run_P7_{dataset}_{baseline}_{doc}_{query}_{condition}_s{seed}`
- SHA-256 hashes track document contents, queries, configuration payloads, and git commit history.

---

## 5. Benchmark Corpus & Partition Integrity
- Ingestion corpus: `experiments/phase6/indexes/` (50 documents, 50 queries, document lengths: 5, 10, 20, 50 pages).
- Partitions: 10 `train`, 15 `val`, 25 `test`.
- Invariant: Partition splits are inherited by all child pages and evidence units. Zero cross-split contamination.

---

## 6. Audit Conclusion & Phase 7 Readiness Gate
The Phase 6 interface is fully documented, statically validated, and frozen. The repository is ready for Phase 7 implementation under `src/evidence/`.
