# Phase 5.1 Historical Lineage & Provenance Comparison Report

**Project**: Vision-Language Models for Intelligent Document Processing under Real-World Visual Degradation  
**Phase**: 5.1 — Scientific Correction & Revalidation  
**Date**: 2026-10-05  

---

## 1. Project Research Lifecycle & Commit Lineage

The authoritative project commit lineage is established as follows:

```text
e38c12d
feat(governance): initialize research control system and repository scaffold

bde2b53
feat(phase0): freeze scientific research protocol, literature foundation, and experimental specifications

609ac2d
feat(phase1): implement document ingestion pipeline and zero-leakage split manager

1caa4b0
feat(phase3): implement document quality and degradation assessment

a01bed0
feat(phase5): implement adaptive routing policies, cost model, and calibration

[PHASE 5 FORMAL SCIENTIFIC AUDIT]
Audit Result: PASS WITH CORRECTIONS REQUIRED (P1-01, P1-02, P1-03 identified)

[PHASE 5.1 CURRENT COMMIT]
fix(phase5.1): correct routing leakage, trace persistence, and learned-router deployment
```

---

## 2. Immutability Guarantee

As mandated by Phase 0 Governance and Rules:
1. **Commit `a01bed0` is Frozen**: Historical commit records remain intact in git history.
2. **`experiments/phase5/` is Frozen**: All original Phase 5 artifacts (102 traces, `index.json`, calibration metrics, summary files) remain untouched on disk.
3. **Independent Lineage**: All corrected outputs are created exclusively under:
   - `configs/phase5_1/`
   - `experiments/phase5_1/`
   - `reports/phase5_1/`

---

## 3. Comparison of Core Characteristics

| Attribute | Phase 5 (Historical) | Phase 5.1 (Corrected) |
|---|---|---|
| Configuration Master | `configs/phase5/routing_config.yaml` | `configs/phase5_1/routing_config.yaml` |
| Trace Artifacts Directory | `experiments/phase5/routing_traces/` | `experiments/phase5_1/routing_traces/` |
| Trace Cardinality | 102 files (Defective overwrite) | **4,500 files (Complete)** |
| Trace Overwrite Protection | None | Cryptographic Hash Collision Detection |
| Uncertainty Feature Input | `condition.severity`, `condition.family` | Observable visual features only |
| Learned Router Deployment | In-memory only (unfitted fallback to B2) | **Joblib serialized (`learned_router.joblib`)** |
| Total Tests | 163 passed | **178 passed** (+10 new test suites) |
| Hypothesis H2 Result | NOT_SUPPORTED ($\Delta = -0.0107, p=0.0000$) | **NOT_SUPPORTED** ($\Delta = -0.0107, p=0.0000$) |
| Scientific Conclusion | Robust native VLM dominates naive routing | Robust native VLM dominates naive routing; learned router offers 16.6% compute reduction |

---

## 4. Archival and Audit Trail

Every file created in Phase 5.1 carries explicit provenance headers, linking back to the audit findings. The before-and-after results confirm that fixing the engineering defects validates the original scientific finding while eliminating all data integrity compromises.
