# Phase 6 Report 09: Evidence Packaging and Cryptographic Provenance

## 1. Structured Output Schema (`EvidencePackage`)
The output of Phase 6 retrieval is encapsulated in an immutable, validated `EvidencePackage` Pydantic model (`src/retrieval/schema.py`):
```json
{
  "package_id": "pkg_run_P6_synthetic_multipage_b6_5_doc_mp_001_q_doc_mp_001_s42",
  "document_id": "doc_mp_001",
  "query_id": "q_doc_mp_001",
  "retrieval_method": "B6-5",
  "top_k_pages_requested": 3,
  "top_m_regions_requested": 3,
  "total_document_pages": 5,
  "selected_pages": [
    {"page_number": 2, "score": 1.0, "rank": 1}
  ],
  "selected_regions": [
    {"region_id": "doc_mp_001_p2_tbl1", "page_number": 2, "bbox": [80, 120, 920, 580], "region_type": "table", "score": 1.12}
  ],
  "vlm_page_reduction_ratio": 0.40,
  "provenance": {
    "run_id": "run_P6_synthetic_multipage_b6_5_doc_mp_001_q_doc_mp_001_s42",
    "phase": "6",
    "git_commit": "3dfa2a2",
    "document_hash": "a1b2c3d4...",
    "query_hash": "e5f6g7h8...",
    "config_hash": "9a0b1c2d...",
    "timestamp_utc": "2026-10-05T06:31:39.123456+00:00"
  }
}
```

## 2. Zero-Leakage & Provenance Guarantees
- **Static AST Audit**: Verified by `tests/test_phase6_no_leakage.py` that no retrieval components access test labels or ground truth.
- **Trace Uniqueness**: `run_id` format guarantees zero trace collisions across all queries, baselines, and random seeds.
- **Reproducibility**: Exact git commit hash (`3dfa2a2`) and SHA-256 parameter hashes are embedded in every output artifact.
