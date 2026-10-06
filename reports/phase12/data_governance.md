# DATA GOVERNANCE, ETHICAL / LEGAL POLICY & ANONYMIZATION

**Project:** Vision-Language Models for Intelligent Document Processing under Real-World Visual Degradation  
**Phase:** Phase 12 — Authentic Real-World Document Benchmark & Degradation Generalization  
**Date:** 2026-10-06  
**Auditor:** Senior Research Engineer & ML Reproducibility Auditor  
**Status:** APPROVED & ENFORCED

---

## 1. Ethical & Legal Principles

In strict adherence to Rule 0.1 and Section 9 of the Phase 12 research protocol, the authentic document benchmark is constructed under rigorous data governance principles:

1. **Permitted Data Sources Only:** Documents are sourced strictly from established, openly licensed academic benchmarks, public-domain repositories, and authorized historical research archives.
   - **DocVQA / Single-Page Benchmarks:** Academic research licenses.
   - **FUNSD / CORD / SROIE:** Open research and evaluation datasets.
   - **UCSF Industry Documents Library:** Publicly accessible historical document archives released for research.
   - **RVL-CDIP:** Open document classification corpus (IIT-CDIP public domain release).
   - **Government / Regulatory Public Filings:** Publicly available disclosures (e.g. SEC EDGAR public reports).
2. **Zero Unauthorized Scraping:** No private, password-protected, paywalled, or restricted internal company documents are collected.
3. **No Personally Identifiable Information (PII):** Any names, telephone numbers, or email addresses appearing in public scans are historical, fictitious, or de-identified in accordance with standard benchmark protocols.

---

## 2. Document Provenance Schema & Metadata

Every document registered in `data/phase12_authentic/` is paired with an immutable cryptographic provenance descriptor stored in `data/phase12_authentic/provenance/`:

```json
{
  "document_id": "doc_auth_001",
  "family_id": "fam_auth_01",
  "source_type": "public_domain_archive",
  "acquisition_modality": "D12-1",
  "degradation_type": "mobile_camera_perspective",
  "page_count": 5,
  "license_status": "open_access_research",
  "source_reference": "RVL-CDIP_subcollection_receipts",
  "collection_timestamp": "2026-10-06T15:00:00Z",
  "annotation_status": "verified",
  "checksum_sha256": "3a8f9c1b..."
}
```

---

## 3. Usage & Redistribution Restrictions

- **Research-Only Constraint:** The dataset layer is constructed solely for scientific evaluation of Vision-Language Models under physical acquisition degradation.
- **Commercial Redistribution Prohibited:** The benchmark derivatives must not be resold or used for proprietary commercial training without independent licensing verification.
- **Immutable Raw Storage:** Source document instances remain read-only once registered and hashed.
