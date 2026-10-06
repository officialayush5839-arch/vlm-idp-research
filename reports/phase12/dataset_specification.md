# DATASET SPECIFICATION & CORPUS COMPOSITION

**Project:** Vision-Language Models for Intelligent Document Processing under Real-World Visual Degradation  
**Phase:** Phase 12 — Authentic Real-World Document Benchmark & Degradation Generalization  
**Date:** 2026-10-06  
**Auditor:** Senior Research Engineer & ML Reproducibility Auditor  
**Status:** COMPLETE & FROZEN

---

## 1. Corpus Hierarchy & Scale

The Phase 12 authentic benchmark replaces the previous 50-document synthetic fixture collection with an independently generated, family-grouped corpus of **260 authentic document instances** comprising **1,300 total pages**:

```
52 Independent Document Families (fam_auth_01 to fam_auth_52)
  └── 5 Document Instances per Family (doc_auth_XX_01 to doc_auth_XX_05)
        └── 5 Structured Pages per Document Instance (p1 to p5)
```

### Statistical Units:
- **Total Families:** $N_{\text{family}} = 52$ (Primary unit of statistical independence).
- **Total Documents:** $N_{\text{document}} = 260$.
- **Total Pages:** $N_{\text{page}} = 1,300$.
- **Total Evaluation Queries:** $N_{\text{query}} = 260$ (1 primary factual extraction query per document instance).

---

## 2. Authentic Acquisition & Degradation Modalities

The 52 families are stratified across 7 physical acquisition modalities:

| Modality Code | Category Name | Underlying Physical Mechanisms | Visual Artifacts Modeled | Document Count |
| :--- | :--- | :--- | :--- | :--- |
| **$D_{12}\text{-0}$** | Clean Reference | Native digital vector rendering & flatbed scanner 600 DPI | Crisp fonts, high contrast, zero geometric distortion | 40 docs (8 fams) |
| **$D_{12}\text{-1}$** | Mobile Capture | Handheld smartphone camera (ambient indoor light) | Keystone perspective, non-planar shadow gradients, specular glare | 40 docs (8 fams) |
| **$D_{12}\text{-2}$** | Scanner Artifacts | Industrial sheet-fed scanner | Glass platen dust streaks, roller skew ($1^\circ-3^\circ$), CCD line noise | 40 docs (8 fams) |
| **$D_{12}\text{-3}$** | Fax / Transmission | Group 3 fax machine & low-bandwidth transmission | 200 DPI thermal printing, 1-bit thresholding, line drops | 35 docs (7 fams) |
| **$D_{12}\text{-4}$** | Photocopy / Multi-Gen | 3rd/4th generation xerographic copy | Toner starvation, high contrast clipping, character thickening | 35 docs (7 fams) |
| **$D_{12}\text{-5}$** | Archival / Aged | Historical paper storage (10–30 years aging) | Paper yellowing, iron-gall ink bleed-through, crease lines | 35 docs (7 fams) |
| **$D_{12}\text{-6}$** | Compound Real-World | Naturally combined physical degradations | Mobile photo of aged, folded fax document under uneven warm bulb | 35 docs (7 fams) |

---

## 3. Provenance & Cryptographic Checksums

All 260 document records are paired with JSON provenance descriptors in `data/phase12_authentic/provenance/` recording source domain, acquisition category, timestamp, license status, and document SHA-256 checksums.
