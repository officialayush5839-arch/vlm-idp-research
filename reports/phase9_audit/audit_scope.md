# Phase 9 Scientific Audit Scope & Charter

**Date:** 2026-10-06  
**Auditor:** Senior Scientific ML Reliability Auditor  
**Repository:** `vlm-idp-research`  
**Audited Commit:** `209d7eb`  
**Audited Phase:** Phase 9 — Uncertainty-Aware Reliability, Abstention & Failure-Safety Evaluation  

---

## 1. Mandate & Standards
This audit establishes whether the implementation, experimental artifacts, statistical tests, and scientific reporting of Phase 9 adhere to strict IEEE publication standards:
1. Complete cryptographic provenance and absence of data fabrication.
2. Absolute test-set partition isolation during calibration and threshold selection.
3. Strict information boundary: uncertainty estimation must consume solely observable runtime features.
4. Mathematical verification of selective prediction metrics, risk-coverage trade-offs, and Area Under Risk-Coverage (AURC).
5. Uncompromised reporting of hypothesis testing outcomes (specifically preserving negative findings for Hypothesis H9).
6. Non-regression of historical phases (Phases 0 through 8).
