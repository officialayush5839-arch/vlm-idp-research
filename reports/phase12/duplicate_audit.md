# DUPLICATE AUDIT & PARTITION INTEGRITY REPORT

**Project:** Vision-Language Models for Intelligent Document Processing under Real-World Visual Degradation  
**Phase:** Phase 12 — Authentic Real-World Document Benchmark & Degradation Generalization  
**Date:** 2026-10-06  
**Auditor:** Senior Research Engineer & ML Reproducibility Auditor  
**Status:** PASS (Zero Leakage, Zero Duplicate Collisions)

---

## 1. Duplicate Detection Audit

A multi-tiered duplicate audit was executed across all 260 documents in `data/phase12_authentic/`:
1. **Cryptographic Checksum Collision Audit (SHA-256):**
   - Unique hashes evaluated: 260 / 260.
   - Hash collisions detected: **0**.
   - Exact duplicates found: **0**.
2. **Textual Jaccard Similarity Audit:**
   - Evaluated 33,670 pairwise document text combinations.
   - Cross-family exact duplicates: **0**.
   - Intra-family variant similarity: Controlled variation in nominal values and dates across document instances.

---

## 2. Family-Grouped Partition Integrity

To prevent cross-partition leakage, splitting was performed strictly at the **family level** rather than random page or document splitting:

| Partition | Family Count ($N_{\text{fam}}$) | Family Percentage | Document Count ($N_{\text{doc}}$) | Page Count ($N_{\text{page}}$) | Query Count ($N_{\text{query}}$) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Train** | 31 | $59.6\%$ | 155 | 775 | 155 |
| **Validation** | 10 | $19.2\%$ | 50 | 250 | 50 |
| **Test** | 11 | $21.2\%$ | 55 | 275 | 55 |
| **Total** | **52** | **100.0%** | **260** | **1,300** | **260** |

### Disjointness Verification:
- $\text{Train} \cap \text{Validation} = \emptyset$ (Disjointness: **CONFIRMED**)
- $\text{Train} \cap \text{Test} = \emptyset$ (Disjointness: **CONFIRMED**)
- $\text{Validation} \cap \text{Test} = \emptyset$ (Disjointness: **CONFIRMED**)
- **Zero Cross-Split Contamination:** No test family appears in development or validation sets.
