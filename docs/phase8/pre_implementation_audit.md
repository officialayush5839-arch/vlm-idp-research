# Phase 8 Pre-Implementation Forensic Audit & Interface Inspection

**Date**: 2026-10-05  
**Stage**: Step 0 Pre-Implementation Forensic Inspection  
**Repository**: `vlm-idp-research`  
**Current Git HEAD**: `9ea3b89` (`feat(phase7): implement evidence grounding and verification`)

---

## 1. Repository State & Frozen Phase Boundaries
The repository is at a clean, verified state:
- **Phase 0 (Protocol Freeze)**: Frozen at commit `e38c12d`.
- **Phase 1 (Repository Infrastructure)**: Frozen at commit `49bbd7b`.
- **Phase 2 / 2.5 (Baselines & Unlimited-OCR)**: Frozen at commits `159dfc9` and `446ee2d`.
- **Phase 3 (Quality Assessment)**: Frozen at commit `1caa4b0`.
- **Phase 4 (Controlled Degradation Benchmark)**: Frozen at commit `deacf9a`.
- **Phase 5 (Adaptive Routing)**: Historical commit `a01bed0`.
- **Phase 5.1 (Routing Correction & Revalidation)**: Frozen at commit `3dfa2a2`.
- **Phase 6 (Long-Document Multimodal Retrieval)**: Frozen at commit `afdd599`.
- **Phase 7 (Evidence Grounding & Verification)**: Frozen at commit `9ea3b89`.

All 267 repository tests pass (100% pass rate).

---

## 2. Reusable Interfaces

### A. Phase 3 Quality Assessment (`src/quality/`)
- `PageQualityAssessment`: provides inference-observable visual feature scores:
  `blur`, `noise`, `skew`, `glare`, `contrast`, `resolution`, `compression`, `illumination`, `occlusion`, `perspective`, and `overall_quality`.
- Strictly observable from document pixel buffers without access to ground truth.

### B. Phase 5.1 Routing Context (`src/routing/`)
- `UncertaintyAdapter`: provides historical multi-signal formulation `[u_vlm, u_ocr, u_ret, u_gnd, u_qual, u_agr]`.
- In Phase 5.1, retrieval (`u_ret`) and grounding (`u_gnd`) were proxy constants because Phases 6 and 7 were not yet built.
- In Phase 8, these signals are replaced by genuine observable features from Phase 6 and Phase 7!

### C. Phase 6 Retrieval (`src/retrieval/`)
- `EvidencePackage`: provides retrieval scores, page-level scores, region scores, top-1 vs top-k score margin, score entropy, and VLM page reduction ratio.

### D. Phase 7 Evidence Grounding (`src/evidence/`)
- `Phase7EvidencePackage`: provides observable verification outcomes:
  - `support_result.semantic_score`: heuristic semantic support score.
  - `support_result.spatial_score`: candidate region geometric validity.
  - `support_result.coverage_score`: query entity coverage.
  - `support_result.support_status`: `SUPPORTED`, `PARTIALLY_SUPPORTED`, `NOT_SUPPORTED`, `INSUFFICIENT_EVIDENCE`.
  - `grounding_result.grounding_status`: `GROUNDED`, `PARTIALLY_GROUNDED`, `UNSUPPORTED`.
  - `grounding_result.evidence_sufficiency_status`: `SUFFICIENT`, `PARTIALLY_SUFFICIENT`, `INSUFFICIENT`.
  - `citations`: list of cryptographically hashed evidence citations.

---

## 3. Critical Information Boundary & Prohibited Inputs

### Prohibited at Runtime (Strictly Forbidden):
- Exact gold/ground-truth answers (`gold_answer`, `target_answer`, `ground_truth_answer`).
- Gold evidence regions / target bounding boxes (`ground_truth_pages`, `ground_truth_regions`, `ground_truth_bboxes`).
- Degradation metadata (`condition.family`, `condition.severity`, `degradation_level`).
- Oracle model correctness (`is_correct`, `oracle_decision`).

### Permitted at Runtime (Observable at Inference Time):
- Model confidence and prediction entropy.
- Retrieval score statistics (top-1 score, score margin $\Delta = s_1 - s_2$, retrieval entropy).
- Evidence grounding signals (semantic support score, query entity coverage, sufficiency status enum, grounding status enum, number of citations).
- Document visual quality vector (10 quality features and overall quality score from Phase 3).
- Document length / page count.

---

## 4. Evaluation Partitions
Per `protocol/split_protocol.md` and `experiments/phase6/indexes/corpus_manifest.json`:
- **Calibration Partition (`split == "val"`)**: 15 multi-page documents (15 queries) across degradation tiers.
  *Used exclusively for fitting calibration models (temperature scaling, isotonic regression) and selecting abstention thresholds.*
- **Test Partition (`split == "test"`)**: 25 multi-page documents (25 queries) across degradation tiers.
  *Frozen; evaluated only once with frozen calibration artifacts.*
- **Training Partition (`split == "train"`)**: 10 documents (isolated).

---

## 5. Existing vs Missing Components
- **Existing**:
  - Phase 3 visual quality extractors.
  - Phase 6 multimodal retriever.
  - Phase 7 spatial/semantic grounding pipeline and evidence packages.
  - Partition manifests and evaluation splits.
- **Missing (To be created in Phase 8 under `src/uncertainty/`)**:
  - `schema.py`: Domain models for uncertainty vectors, calibration artifacts, and abstention decisions.
  - `signals.py`: Ingests Phase 3, Phase 6, and Phase 7 observable signals into a unified feature representation.
  - `temperature.py`: Temperature scaling calibrator.
  - `isotonic.py`: Non-parametric Isotonic regression calibrator.
  - `calibration.py`: Unified calibration manager and artifact persistence.
  - `abstention.py`: Threshold-based selective prediction decision engine (`ANSWER` vs `ABSTAIN`).
  - `metrics.py`: ECE, MCE, Brier score, selective risk, coverage, AURC.
  - `provenance.py`: Unique run ID generation (`run_P8_...`) and SHA-256 artifact hashing.
  - `audit.py`: Static AST zero-leakage validator.
  - `pipeline.py`: Master `UncertaintyCalibrationPipeline`.

---

## 6. Implementation Plan Summary
1. Configurations (`configs/phase8/*.yaml`).
2. Schemas & Domain Models (`src/uncertainty/schema.py`).
3. Signal Ingestion & Feature Engineering (`src/uncertainty/signals.py`, `features.py`).
4. Calibration Engines (`src/uncertainty/temperature.py`, `isotonic.py`, `calibration.py`).
5. Selective Prediction & Abstention (`src/uncertainty/abstention.py`, `selective.py`).
6. Metrics & Statistical Validation (`src/uncertainty/metrics.py`).
7. Provenance & Zero-Leakage AST Auditor (`src/uncertainty/provenance.py`, `audit.py`).
8. Master Pipeline (`src/uncertainty/pipeline.py`).
9. Dedicated Test Suites (`tests/test_phase8_*.py`).
10. Execution Scripts (`scripts/run_phase8_*.py`).
11. Reports & Master Documentation (`reports/phase8/*.md`).
12. Verification & Local Commit.
