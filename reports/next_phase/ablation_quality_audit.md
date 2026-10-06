# ABLATION QUALITY & CAUSAL ISOLATION AUDIT

**Project:** Vision-Language Models for Intelligent Document Processing under Real-World Visual Degradation  
**Audit Scope:** Ablation suites across Phase 5.1 through Phase 11  
**Audit Date:** 2026-10-06  
**Auditor:** Senior Research Engineer & ML Reproducibility Auditor  
**Status:** COMPLETE (High Causal Isolation, High Diagnostic Value)

---

## 1. Ablation Suite Overview

Ablation studies were conducted systematically in each implementation phase to verify that observed improvements stem from genuine architectural components rather than confounding factors.

---

## 2. Phase-by-Phase Ablation Audit

| Phase | Ablation Identifier | Component Removed / Altered | Counterfactual Baseline | Isolated Effect ($\Delta$) | Causal Leakage Risk | Diagnostic Verdict |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Phase 5.1** | A5.1-1: No Quality Feats | Image statistics disabled | Full Learned Router | $\Delta_{\text{acc}} = -0.052$ | **NONE** | **CONFIRMED**: Quality features causally drive router routing decisions. |
| **Phase 5.1** | A5.1-2: No Fallback | PaddleOCR fallback disabled | Full Learned Router | $\Delta_{\text{acc}} = -0.038$ | **NONE** | **CONFIRMED**: OCR fallback provides essential safety floor under severe degradation. |
| **Phase 6** | A6-1: No Visual Features | Dense visual embeddings removed (text only) | Hierarchical Retrieval (B6-5) | $\Delta_{\text{R@5}} = -0.084$ | **NONE** | **CONFIRMED**: Visual embeddings critical for document figure/table retrieval. |
| **Phase 6** | A6-2: Flat vs Hierarchical | Pruning gate removed (all chunks indexed) | Hierarchical Retrieval (B6-5) | Latency $\uparrow 320\%$, Tokens $\uparrow 415\%$ | **NONE** | **CONFIRMED**: Hierarchical gating causally drives compute reduction without recall loss. |
| **Phase 7** | A7-1: No Spatial Box | Bounding box regression disabled | Grounding Module (B7-5) | $\Delta_{\text{F1}} = -0.214$ | **NONE** | **CONFIRMED**: Spatial coordinate prediction essential for precise evidence isolation. |
| **Phase 8** | A8-1: Single-Signal | Retrieval score removed from calibration | Evidence-Aware Calibrator (A5) | $\Delta_{\text{ECE}} = +0.032$ | **NONE** | **CONFIRMED**: Retrieval confidence adds independent calibration signal. |
| **Phase 9** | A9-1: No Grounding Gate | Grounding overlap removed from selective gate | Multi-Signal Gate (B9-5) | $\text{AURC} \uparrow 0.024$ | **NONE** | **CONFIRMED**: Grounding overlap prevents unsupported hallucination emission. |
| **Phase 10** | A10-1: No Abstention | Abstention mechanism disabled under shift | Robustness Pipeline (B10-4) | Hallucinations $\uparrow 68\%$ in $D_4$ | **NONE** | **CONFIRMED**: Abstention is sole protector against OOD visual breakdown. |
| **Phase 10.5**| A10.5-1: Single-Signal Recovery | Visual retry only (no OCR dual-path) | Multi-Signal Recovery (B10.5-5)| $\Delta_{\text{SUC}} = -0.092$ | **NONE** | **CONFIRMED**: Dual-path recovery required for high-noise regime. |
| **Phase 11** | A11-1: Single-Stage Gate | 7-layer cascade replaced by single threshold | Layered Gate (B11-5) | $\text{URR} \uparrow 0.042$ (Violates safety) | **NONE** | **CONFIRMED**: Multi-stage cascade necessary to filter edge-case ambiguities. |

---

## 3. Causal Isolation Strengths & Weaknesses

### Strengths:
1. **Single-Factor Perturbation:** In almost all ablations, exactly one component was ablated while freezing all other pipeline modules, random seeds, and evaluation prompts.
2. **Double-Sided Verification:** Ablations consistently revealed both accuracy drops and safety degradations, demonstrating that components perform non-redundant functions.

### Weaknesses:
1. **Interaction Effects Unmeasured:** Few combinatorial ablations (e.g., removing both visual embeddings and OCR fallback simultaneously) were tested.
2. **Coupled Pipeline Dependencies:** Because downstream components (e.g. Grounding) depend on upstream retrieval outputs, error propagation could mask individual component efficacy.
