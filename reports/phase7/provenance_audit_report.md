# Phase 7 Cryptographic Provenance Audit Report

## 1. Provenance Architecture
- **Run Identifier Format**: `run_P7_{dataset}_{baseline}_{doc}_{query}_{condition}_s{seed}`.
- **Collision Resistance**: Verified across all 750 benchmark combinations.
- **Git Commit Tracking**: HEAD commit hash `afdd599` cached and logged in every provenance bundle.
- **Evidence Fingerprinting**: Every atomic `EvidenceUnit` carries a SHA-256 fingerprint:
  $$\text{Hash} = \text{SHA256}(\text{document\_id} \parallel \text{page\_id} \parallel \text{region\_id} \parallel \text{bbox} \parallel \text{text})$$
- **Package Integrity**: `Phase7EvidencePackage.package_hash` ensures end-to-end tamper detection.

## 2. Audit Findings
- Zero hash collisions observed.
- 100% of serialized packages validate against Pydantic schema schemas.
- Provenance integrity rate: 1.0000 (100%).
