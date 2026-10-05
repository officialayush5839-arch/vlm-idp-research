# Phase 7: Evidence Grounding, Verification & Answer-Support Validation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement a scientifically validated, zero-leakage, deterministic Evidence Grounding subsystem on top of the frozen Phase 6 retrieval architecture to verify whether retrieved pages and regions provide spatially valid, semantically supportive, and sufficient evidence to answer document intelligence queries across clean and visually degraded conditions.

**Architecture:** A multi-stage evidence grounding pipeline residing in `src/evidence/` that consumes Phase 6 `EvidencePackage` structures, converts candidate regions into normalized `EvidenceUnit` objects, executes rigorous spatial overlap (IoU $\ge 0.50, 0.75$) and semantic/numeric/table verification, evaluates evidence sufficiency, maps decisions through a strict four-state decision tree (`SUPPORTED`, `PARTIALLY_SUPPORTED`, `NOT_SUPPORTED`, `INSUFFICIENT_EVIDENCE`), attaches SHA-256 cryptographic citations, and performs paired bootstrap hypothesis testing ($B=10,000$) for Hypothesis H5.

**Tech Stack:** Python 3.14.6, PyTorch (CPU-only), scikit-learn, numpy, pydantic v2, Pillow, PyYAML, pytest.

**Spec:** PRD (`prd.md`), Architecture (`architecture.md`), Rules (`rules.md`), Phases (`phases.md`), Research Protocol (`research_protocol.md`), and Master Implementation Prompt for Phase 7.

## Global Constraints
- Preserve Phase 0 through Phase 6 scientific immutability (Phase 6 commit `afdd599`, Phase 5.1 commit `3dfa2a2`).
- DO NOT modify `src/retrieval/`, `experiments/phase6/`, `reports/phase6/`, or `tests/test_phase6_*`.
- Strict anti-fabrication: Never invent answers, evidence snippets, bounding boxes, or confidence probabilities. Emit `INSUFFICIENT_EVIDENCE` when unsupported.
- Zero runtime label leakage: Runtime code must operate only on observable evidence without accessing oracle answers, target page/region annotations, or degradation ground truths.
- Configuration-driven thresholds: All thresholds must be loaded from `configs/phase7/*.yaml` without test-set tuning.
- Local commit only: `feat(phase7): implement evidence grounding and verification`. DO NOT push to remote. DO NOT execute Phase 8.

## Review Focus
1. Spatial coordinate bounds: Enforce normalized bounds $[0, 1000]$ with $[x_{\min}, y_{\min}, x_{\max}, y_{\max}]$; reject degenerate or out-of-bounds boxes.
2. Numeric & Unit precision: Ensure numeric queries verify exact numeric tokens, signs, units, and decimal places (e.g. $48.7M vs 487).
3. Table cell alignment: Ensure values occurring on the page match row/column tabular context rather than accidental page occurrences.
4. Multi-page aggregation: Seamlessly combine evidence units originating from distinct pages with individual provenance IDs.
5. Trace collision prevention: Ensure `run_P7_...` run IDs are unique across all baselines, seeds, and conditions.

---

### Task 1: Phase 7 Configuration System (`configs/phase7/`)
- Create: `configs/phase7/evidence_config.yaml`
- Create: `configs/phase7/grounding_config.yaml`
- Create: `configs/phase7/spatial_config.yaml`
- Create: `configs/phase7/semantic_config.yaml`
- Create: `configs/phase7/sufficiency_config.yaml`
- Create: `configs/phase7/provenance_config.yaml`
- Create: `configs/phase7/experiment_matrix.yaml`
- Create: `configs/phase7/evaluation_config.yaml`

### Task 2: Evidence Domain Model & Schemas (`src/evidence/schema.py`)
- Pydantic models: `EvidenceUnit`, `EvidenceSupportResult`, `GroundingResult`, `Phase7EvidencePackage`, `GroundingMetricsResult`, `CitationRecord`.

### Task 3: Evidence Extraction & Region Validation (`src/evidence/extractor.py`, `src/evidence/region_validator.py`)
- Ingest Phase 6 candidate packages and map to standardized `EvidenceUnit` records. Compute IoU in $[0, 1000]$ space.

### Task 4: Semantic, Numeric & Table Verification (`src/evidence/semantic_support.py`, `src/evidence/numeric_verifier.py`, `src/evidence/table_verifier.py`)
- Observable lexical overlap, numeric precision matching (value, unit, decimal), and tabular row/column alignment.

### Task 5: Multi-Page Aggregation, Sufficiency & Grounding State Machine (`src/evidence/multipage_aggregator.py`, `src/evidence/evidence_sufficiency.py`, `src/evidence/grounding_classifier.py`)
- Cross-page evidence collection, sufficiency classification, and four-state decision tree.

### Task 6: Cryptographic Provenance, Citation & Audit Layer (`src/evidence/provenance.py`, `src/evidence/citation.py`, `src/evidence/audit.py`)
- SHA-256 citation hashes, tamper detection, trace IDs (`run_P7_...`), and AST zero-leakage audit.

### Task 7: Metrics, Baselines & Master Pipeline (`src/evidence/metrics.py`, `src/evidence/baselines.py`, `src/evidence/pipeline.py`)
- IR/grounding metrics, B7-0 to B7-5 baseline adapters, and end-to-end pipeline.

### Task 8: Comprehensive Test Suites (`tests/test_phase7_*.py`)
- 19 test suites covering schema, extraction, spatial, semantic, numeric, table, multipage, sufficiency, grounding, provenance, citations, metrics, determinism, trace identity, cardinality, leakage, partition integrity, statistics, ablations.

### Task 9: Experiment Execution (`scripts/run_phase7_*.py`)
- Smoke test, validation calibration, full benchmark (B7-0 to B7-5 across 5 seeds), ablations (A1–A8), and bootstrap hypothesis testing for H5.

### Task 10: Research Reports & Governance Sign-Off (`reports/phase7/`, `task.md`, `phases.md`, `memory.md`)
- 20 detailed reports including `PHASE7_REPORT.md` (all 28 sections), governance updates, and clean local commit.
