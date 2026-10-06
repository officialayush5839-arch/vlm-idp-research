# PHASE 12 PRE-IMPLEMENTATION INVENTORY & INTERFACE SPECIFICATION

**Project:** Vision-Language Models for Intelligent Document Processing under Real-World Visual Degradation  
**Phase:** Phase 12 — Authentic Real-World Document Benchmark & Degradation Generalization  
**Date:** 2026-10-06  
**Status:** COMPLETE (Pre-Implementation Baseline Frozen)

---

## 1. Executive Summary & Purpose

Phase 12 exists to evaluate whether the architectural principles and empirical conclusions established in Phases 0 through 11 generalize to an authentic corpus of real-world multi-page documents exhibiting naturally occurring visual degradation and acquisition artifacts.

Before introducing the authentic dataset layer, this document establishes the pre-implementation inventory of existing data structures, reusable pipeline modules, frozen algorithms, and interface contracts to guarantee non-breaking compatibility and zero leakage.

---

## 2. Reusable Repository Modules & Frozen Interfaces

The codebase contains modular, production-grade subsystems across `src/` that will be re-used in **frozen mode** during Phase 12 Stage A external validation:

| Subsystem | Source Package | Core Classes & Interfaces | Phase 12 Usage Mode |
| :--- | :--- | :--- | :--- |
| **Ingestion** | `src/ingestion/` | Document page normalization, bbox coordinates, image loading | Frozen Read-Only |
| **Quality Assessment** | `src/quality/` | `PageQualityAssessment`, Laplacian blur, FFT noise, glare | Frozen Read-Only |
| **Hierarchical Retrieval**| `src/retrieval/` | `DenseTextRetriever`, `BM25Okapi`, `MultimodalFusion`, `EvidencePackageBuilder` | Frozen Read-Only (Baselines B6-0 to B6-5) |
| **Evidence Grounding** | `src/evidence/` | `EvidenceExtractor`, `GroundingClassifier`, `RegionValidator`, `NumericVerifier` | Frozen Read-Only (Baselines B7-0 to B7-5) |
| **Uncertainty Calibration**| `src/uncertainty/` | `IsotonicCalibrator`, `TemperatureScaler`, `SelectiveClassifier` | Frozen Read-Only (Baselines B8, B9-0 to B9-5) |
| **Reliability Subsystem** | `src/reliability/` | `ReliabilityPackage`, `UncertaintyVector`, `ReliabilityDecision` | Frozen Read-Only |
| **Robustness & Domain Shift**| `src/robustness/` | `DomainRegistry`, `ShiftDetector`, `RobustnessMetrics` | Frozen Read-Only (Baselines B10-0 to B10-4) |
| **Recovery Subsystem** | `src/recovery/` | `MultiSignalRecoveryPipeline`, `DualPathEnhancement` | Frozen Read-Only (Baselines B10.5-0 to B10.5-5) |
| **Safety Gate / HITL** | `src/safety_recovery/`| `LayeredSafetyGate`, `HumanEscalationPolicy`, `VerificationCascade` | Frozen Read-Only (Baselines B11-0 to B11-6) |

---

## 3. Existing vs. Phase 12 Dataset Architectures

### 3.1 Historical Dataset Architecture (Phases 0–11)
- **Root Image Store:** 4 single-page PNGs (`data/raw/`).
- **Multi-Page Corpus:** 50 JSON fixtures (`doc_mp_001.json` to `doc_mp_050.json`), where `image_path: null` and page text/regions are synthesized data models.
- **Partition:** 10 Train, 15 Val, 25 Test documents. In Phase 10, the 25 test documents were assigned across 5 domains ($D_0$–$D_4$), resulting in only 5 physical documents per domain.

### 3.2 Phase 12 Authentic Architecture
- **Namespace:** Strictly isolated under `data/phase12_authentic/` and `experiments/phase12/`.
- **Target Scale:** 260+ authentic document instances structured into **52 independent document families** ($\ge 5$ pages per document on average, totaling 1,300+ pages).
- **Statistical Grouping:** Resampling and splitting strictly grouped by `family_id` to eliminate intra-family leakage.
- **Acquisition Modalities:**
  - $D_{12}\text{-0}$: Clean Reference (High-resolution digital / clean flatbed scans)
  - $D_{12}\text{-1}$: Mobile Capture (Perspective, uneven shadows, glare, camera blur)
  - $D_{12}\text{-2}$: Scanner Artifacts (Glass smudges, dust streaks, skew)
  - $D_{12}\text{-3}$: Fax / Transmission Artifacts (Thermal print bleed, line noise, compression)
  - $D_{12}\text{-4}$: Photocopy / Multi-Generation (Toner dropout, contrast collapse, edge blur)
  - $D_{12}\text{-5}$: Archival / Aged Documents (Paper discoloration, ink bleed-through, creases)
  - $D_{12}\text{-6}$: Compound Real-World Degradation (Naturally combined physical artifacts)

---

## 4. Query Schema & Evidence Annotation Contract

Phase 12 annotations conform to the schema required by `src/evidence/` and `src/retrieval/`:
```json
{
  "query_id": "q_auth_fam01_001",
  "document_id": "doc_auth_001",
  "family_id": "fam_auth_01",
  "question": "What is the net total invoice amount stated in the summary section?",
  "ground_truth_answer": "$4,850.00",
  "evidence_page": 2,
  "evidence_regions": [
    {
      "region_id": "reg_p2_total",
      "bbox": [720, 810, 890, 860],
      "text": "Total Due: $4,850.00",
      "region_type": "table_cell"
    }
  ],
  "modality": "D12-1",
  "degradation_severity": "moderate"
}
```

---

## 5. Frozen Algorithm & Zero Leakage Protocol

1. **Stage A Frozen Validation:** The existing feature extractors, retrieval scoring functions, calibration matrices, and routing thresholds from Phases 6–11 will be evaluated on the Phase 12 authentic test partition with **0 modifications to weights, hyperparameters, or thresholds**.
2. **Zero Information Leakage:** Neither the router, retriever, grounding module, nor safety gate will have runtime access to test set labels, true degradation labels, or oracle answers.
