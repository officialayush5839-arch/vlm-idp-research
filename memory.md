# VLM-IDP Research Project Memory

## 1. Project Identity
VLM-IDP Research. Status: ACTIVE.

## 2. Current Research Title
"Adaptive, Uncertainty-Aware and Evidence-Grounded Vision-Language Document Intelligence under Real-World Visual Degradation"

## 3. Current Research Questions
RQ1-RQ6 frozen in `goal.md` and `research_protocol.md`. Status: CONFIRMED.

## 4. Current Hypotheses
H1-H6 frozen in `goal.md` and `research_protocol.md`. Status: CONFIRMED.

## 5. Current Architecture
As defined in architecture.md. Status: DESIGNED (Phase 1 implementation pending).

## 6. Selected Models
Qwen2.5-VL 7B (primary), InternVL (secondary), PaddleOCR, Tesseract, BGE embeddings, FAISS vector index. Status: DECLARED (to be integrated in Phase 2).

## 7. Selected Datasets
DocVQA, FUNSD, SROIE, CORD, MMLongBench-Doc, LongDocURL, XL-DocBench. Status: DECLARED (manifests in Phase 1).

## 8. Dataset Split Decisions
Zero-leakage invariant locked in `protocol/split_protocol.md`. All degraded variants inherit source split. Status: CONFIRMED.

## 9. Important Experiment Decisions
Baselines B0-B6 + PROPOSED, Ablations A1-A12, 5-seed protocol, paired bootstrap testing frozen in `protocol/`. Status: CONFIRMED.

## 10. Experiment Results
Phase 2/2.5 baseline execution verified on clean fixtures. Phase 3 quality feature validation (E3-VAL-QUALITY) complete across 9 families and 5 severities. Phase 4 Controlled Degradation Benchmark executed (3,600 conditions across 4 datasets, 4 models, 9 degradation families, 5 severities, 5 seeds). Full results in `experiments/phase4/index.json` and `experiments/phase4/summaries/E4_BENCHMARK_summary.json`. Status: CONFIRMED.

## 11. Failed Experiments
None yet. Status: NOT_AVAILABLE.

## 12. Model Versions
None installed. Status: NOT_AVAILABLE.

## 13. Prompt Versions
None created. Status: NOT_AVAILABLE.

## 14. Configuration Decisions
pyproject.toml + hatchling, .venv, YAML configs in `configs/phase0/`, `configs/phase3/`, and `configs/phase4/`. Status: CONFIRMED.

## 15. Architecture Decisions
Tri-pathway adaptive routing, multi-signal uncertainty vector, hierarchical multimodal retrieval. Status: CONFIRMED.

## 16. Known Limitations
RTX 3050 6GB VRAM requires 4-bit quantization (bitsandbytes/AWQ). Global Python has CPU-only PyTorch (CUDA setup required in Phase 1 .venv). Status: CONFIRMED.

## 17. Known Bugs
None. Status: NOT_AVAILABLE.

## 18. Open Research Questions
All RQ1-RQ6 frozen for experimental investigation. Status: CONFIRMED.

## 19. Completed Phases
- PHASE 0: Literature Freeze + Research Protocol (Completed: 2026-10-04). Status: CONFIRMED.
- PHASE 1: Repository + Environment + Infrastructure & Document Ingestion (Completed: 2026-10-04, 39/39 tests pass). Status: CONFIRMED.
- PHASE 2: Baseline OCR and VLM Pipelines (Completed: 2026-10-04, 59/59 tests pass, B0/B1/B2 smoke validated). Status: CONFIRMED.
- PHASE 2.5: Unlimited-OCR Integration & Scientific Validation (Completed: 2026-10-04, 69/69 tests pass, B0-U validated). Status: CONFIRMED.
- PHASE 3: Document Quality / Degradation Assessment Module (Completed: 2026-10-05, 106/106 tests pass, E3-VAL-QUALITY validated). Status: CONFIRMED.
- PHASE 4: Controlled Degradation Benchmark (Completed: 2026-10-05, 126/126 tests pass, 3,600 artifacts generated across 9 families, 5 severities, 5 seeds, E4_BENCHMARK validated). Status: CONFIRMED.
- PHASE 5: Adaptive Routing (Completed: 2026-10-05, 163/163 tests pass, Audited: 2026-10-05). Status: CONFIRMED.
- PHASE 5.1: Scientific Correction & Revalidation (Completed: 2026-10-05, 178/178 tests pass, 4,500 distinct traces persisted, zero-leakage verified, learned router deployed, Hypothesis H2 evaluated as NOT_SUPPORTED). Status: CONFIRMED.
- PHASE 6: Long-Document Multimodal Retrieval (Completed: 2026-10-05, 212/212 tests pass, B6-0 through B6-5 baselines, 450 benchmark runs, paired bootstrap B=10,000, Hypothesis H4 evaluated as SUPPORTED). Status: CONFIRMED.

## 20. Current Phase
PHASE 6: Completed. Awaiting authorization to begin Phase 7 (Evidence Grounding). Status: CONFIRMED.

## 21. Current Task
Phase 6 hierarchical multimodal retrieval implementation, benchmark execution, bootstrap hypothesis testing (H4 SUPPORTED), and comprehensive scientific reporting complete. Status: PASS.

## 22. Next Task
PHASE 7: Evidence Grounding (Map answers to page + bounding box + text evidence). Status: PLANNED.

## 23. Paper Status
Section I (Intro) and Section II (Related Work) drafted in `literature/related_work_notes.md`. Ingestion and normalization pipeline methodology documented in `reports/phase1/ingestion_validation.md`. Baseline architectures and fairness specifications documented in `reports/phase2/baseline_registry.md`. Unlimited-OCR baseline justification documented in `reports/phase2_5/ieee_baseline_justification.md`. Document quality and degradation assessment methodology documented in `reports/phase3/PHASE3_REPORT.md`. Controlled degradation benchmark results documented in `reports/phase4/PHASE4_REPORT.md`. Phase 5 audit findings documented in `reports/phase5_audit/PHASE5_SCIENTIFIC_AUDIT.md`. Phase 5.1 corrected adaptive routing architecture, calibration, and empirical results documented in `reports/phase5_1/PHASE5_1_REPORT.md`. Phase 6 hierarchical multimodal retrieval architecture, baseline hierarchy (B6-0 to B6-5), VLM compute reduction (72.2%-94.0%), degradation robustness (+66.7% delta), and Hypothesis H4 validation documented in `reports/phase6/PHASE6_REPORT.md` and 16 detailed reports. Status: IN_PROGRESS.

## 24. Reproducibility Status
Full reproducibility suite implemented in `src/evaluation/reproducibility.py` (seed_everything, env capture, JSON run manifests, zero-leakage split validator). 212 automated unit and integration tests pass in `tests/` (100% pass rate). Prompt templates versioned with SHA-256 fingerprints. Run artifacts saved in `experiments/phase2/`, `experiments/phase2_5/`, `experiments/phase3/`, `experiments/phase4/artifacts/`, `experiments/phase5_1/`, and `experiments/phase6/` (indexes, evidence packages, summaries, ablations). Status: CONFIRMED.

---

### Environment Facts
- Python: 3.14.6 — CONFIRMED
- GPU: NVIDIA RTX 3050 6GB Laptop GPU — CONFIRMED
- Driver: NVIDIA 581.95 (Supports CUDA 13.0 API) — CONFIRMED
- PyTorch: 2.14.1+cpu — CONFIRMED
- CUDA Runtime (PyTorch): NOT_AVAILABLE (CPU-only PyTorch active in Python 3.14 .venv) — CONFIRMED
- OS: Windows 11 AMD64 (Windows-11-10.0.26200-SP0) — CONFIRMED
- Git: Initialized (Commit 3dfa2a2) — CONFIRMED
- Virtual Environment: `.venv` created and populated with dependencies — CONFIRMED
- Unit & Integration Tests: 212 passed in pytest suite (100% pass rate) — CONFIRMED
- Baselines Validated: B0, B1, B2, B0-U, B6-0, B6-1, B6-2, B6-3, B6-4, B6-5 — CONFIRMED
- Quality Features Validated: 10 extractors (blur, noise, skew, glare, contrast, resolution, compression, illumination, occlusion, perspective) — CONFIRMED
- Experiments Validated: Phase 2 smoke (5/5), Phase 2.5 smoke (B0-U 100% match), Phase 3 validation (E3-VAL-QUALITY 9x5 grid), Phase 4 benchmark (E4-BENCHMARK 3,600 conditions), Phase 5.1 benchmark (E5_1-ROUTING 4,500 traces), Phase 6 benchmark (450 evaluations, H4 SUPPORTED) — CONFIRMED
