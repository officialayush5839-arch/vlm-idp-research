# RESEARCH IMPROVEMENT ROADMAP

**Project:** Vision-Language Models for Intelligent Document Processing under Real-World Visual Degradation  
**Document Type:** Prioritized Multi-Phase Engineering & Scientific Improvement Roadmap  
**Date:** 2026-10-06  
**Auditor:** Senior Research Engineer & ML Reproducibility Auditor  
**Status:** READY FOR STAGED EXECUTION

---

## 1. Roadmap Architecture & Strategic Progression

This roadmap outlines five sequenced research development thrusts designed to transition the VLM-IDP repository from a synthetic, fixture-based proof-of-concept into a definitive, publication-ready research landmark.

```
+-----------------------------------------------------------------------------------+
| PRIORITY 1: REAL-WORLD CORPUS SCALING & AUTHENTIC SCAN BENCHMARK (Phase Next)    |
| - 250+ Multi-Page Documents, Real Scans/Faxes, Cluster-Robust Statistical Power   |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
| PRIORITY 2: CONFORMAL RISK CONTROL & RANKING-OPTIMIZED CALIBRATION                |
| - Conformal Prediction, PAC Risk Guarantees, Solving the Invariant AURC Deficit  |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
| PRIORITY 3: BUDGET-CONSTRAINED ADAPTIVE HUMAN-IN-THE-LOOP TRIAGE                  |
| - Constrained Optimization, 15% Max Escalation Budget, Restoring Automated SUC   |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
| PRIORITY 4: END-TO-END UNIFIED MULTIMODAL EVIDENCE REPRESENTATIONS                |
| - Replacing Disjoint Cascades with Joint Vision-Text-Layout Feature Aligners      |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
| PRIORITY 5: PHYSICAL GPU INFERENCE BENCHMARKING & QUANTIZED LATENCY PROFILING     |
| - Full 7B Parameter Continuous Generation, INT4 / AWQ / FP8 Hardware Latencies    |
+-----------------------------------------------------------------------------------+
```

---

## 2. Priority 1 (Immediate Next Phase): Real-World Corpus Scaling & Authentic Scan Benchmark

### Objective:
Replace the 50 synthetic JSON fixtures with a curated corpus of **250+ authentic multi-page documents** spanning 5 distinct real-world acquisition modalities, resolving the statistical power bottleneck ($N=5$ per domain) and confirming true generalizability.

### Research Questions:
- **RQ-Next.1:** How do the performance frontiers of adaptive routing, hierarchical retrieval, and selective abstention shift when transitioning from synthetic digital noise to authentic physical document degradations?
- **RQ-Next.2:** Under cluster-robust statistical sampling of 250 independent multi-page documents, does the proposed adaptive pipeline maintain statistically significant advantages over literature baselines?

### Core Deliverables:
1. **Curated Authentic Corpus (`data/scaled_corpus/`):**
   - 250 multi-page documents (1,250+ total pages) from DocVQA, FUNSD, SROIE, RVL-CDIP, and UCSF Industry Documents Archive.
   - 5 Real-World Acquisition Categories ($D_0^{\text{real}}$ Clean Digital, $D_1^{\text{real}}$ Mobile Camera Captures, $D_2^{\text{real}}$ Multi-Generation Faxes, $D_3^{\text{real}}$ Physical Scanner Smudges/Folds, $D_4^{\text{real}}$ Historical Archival Carbon Copies).
2. **Cluster-Robust Bootstrap Resampling Suite:**
   - Resampling strictly at the independent document level ($N=250$, $B=10,000$) to eliminate pseudo-replication across seeds.
3. **End-to-End Benchmark Re-Evaluation:**
   - Execute Baselines B0–B11 on the scaled authentic corpus.

---

## 3. Priority 2: Conformal Risk Control & Ranking-Optimized Calibration

### Objective:
Overcome the Phase 9 invariant AURC bottleneck ($\Delta_{\text{AURC}} = 0.0000$) by replacing post-hoc softmax calibration with **Conformal Prediction and Distribution-Free Risk Control**.

### Core Deliverables:
1. **Conformal Risk Predictor:** Guarantee bounded user-specified risk ($\mathbb{E}[\text{Risk}] \le \epsilon$) on answer emission without relying on parametric distribution assumptions.
2. **Listwise / Pairwise Ranking Calibration:** Train calibrators directly on AUROC / AURC optimization objectives rather than Cross-Entropy / Brier Score, breaking the monotonic ranking trap of raw softmax probabilities.

---

## 4. Priority 3: Budget-Constrained Adaptive Human-in-the-Loop Triage

### Objective:
Resolve the Phase 11 coverage collapse (60% human escalation) by formulating triage as a **Constrained Knapsack Optimization Problem**.

### Core Deliverables:
1. **Budget-Constrained Policy:** Given a strict human review quota (e.g. at most $k\%$ of queries can be escalated to human operators), find the optimal subset of ambiguous queries that minimizes total system risk.
2. **Dual-Threshold Dynamic Relaxer:** Dynamically adjust verification thresholds based on incoming queue volume and measured document degradation severity.

---

## 5. Priority 4: End-to-End Unified Multimodal Representations

### Objective:
Replace the separate, uncoupled OCR, BGE text embedding, and bounding-box grounding pipelines with a **Joint Vision-Language-Layout Embedding Engine** (inspired by ColPali / LayoutLMv3 architecture), preventing cascading error propagation between retrieval and grounding stages.

---

## 6. Priority 5: Continuous Neural GPU Generation & Latency Profiling

### Objective:
Transition from CPU mock/stub evaluation to physical GPU benchmarking on NVIDIA hardware using quantized 4-bit (AWQ / GPTQ) VLM models (Qwen2.5-VL 7B), profiling real autoregressive token latency, KV-cache memory, and batch throughput.
