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
- PHASE 7: Evidence Grounding, Verification & Answer-Support Validation (Completed: 2026-10-05, 267/267 tests pass, B7-0 through B7-5 baselines, 750 benchmark runs, paired bootstrap B=10,000, Hypothesis H5 evaluated as SUPPORTED). Status: CONFIRMED.
- PHASE 8: Uncertainty Calibration + Abstention (Completed: 2026-10-05, 302/302 tests pass, A0 through A5 baselines, 750 benchmark traces, paired bootstrap B=10,000, Hypothesis H6 evaluated as SUPPORTED). Status: CONFIRMED.
- PHASE 9: Uncertainty-Aware Reliability, Abstention & Failure-Safety Evaluation (Completed: 2026-10-06, Audited: 2026-10-06, 342/342 tests pass, B9-0 through B9-5 baselines, 750 benchmark traces across 5 seeds, paired bootstrap B=10,000, Hypothesis H9 evaluated as NOT_SUPPORTED at alpha=0.05 on AURC while selective accuracy improved from 72.8% to 82.11%, audit pass confirmed). Status: CONFIRMED.
- PHASE 10: Robustness, Cross-Domain Generalization & Distribution-Shift Validation (Completed: 2026-10-06, 352/352 tests pass, B10-0 through B10-4 baselines, 625 benchmark traces across 5 domains and 5 seeds, paired bootstrap B=10,000, Hypothesis H10 evaluated as NOT_SUPPORTED on raw accuracy due to safe complete abstention in D2 and D4). Status: CONFIRMED.
- PHASE 10.5: Safety-Preserving Recovery Under Severe Distribution Shift (Completed: 2026-10-06, 377/377 tests pass, B10.5-0 through B10.5-5 baselines, 750 benchmark traces across 5 domains and 5 seeds, paired bootstrap B=10,000, SUC improved by +0.1840, URR=0.0547, Hypothesis H10.5 evaluated as NOT_SUPPORTED due to URR > 0.05 safety bound). Status: CONFIRMED.
- PHASE 12: Authentic Real-World Document Benchmark & Degradation Generalization (Completed: 2026-10-06). Status: CONFIRMED.
- PHASE 13: Physical GPU VLM Inference, Quantization & End-to-End System Benchmarking (Completed: 2026-10-06). Status: CONFIRMED.
- PHASE 14: Physical CUDA VLM Enablement, Real INT4 Inference & Quantization Benchmark (Completed: 2026-10-07, 439/439 tests pass, .venv_phase14 isolated CUDA 12.6 environment established, physical RTX 3050 6GB Laptop GPU inference verified, target 7B FP16 OOM negative control confirmed, fallback SmolVLM-500M executed across FP16/INT8/INT4 NF4, 1,100 traces across B14-A to B14-D and 5 seeds, 15 tables, 12 publication figures at 300 DPI, 20 reports). Status: CONFIRMED.

## 20. Current Phase
PHASE 14: Completed. Status: CONFIRMED. Phase 15 NOT STARTED.

## 21. Current Task
Phase 14 completed with full physical CUDA validation, zero historical mutations, and 100% test pass rate. Status: PASS.

## 22. Next Task
Awaiting user authorization for next phase. Status: PLANNED.

## 23. Paper Status
Drafting sections across Phases 0–14. Phase 14 physical GPU quantization results, 4-bit NormalFloat speedup, context pruning acceleration, and evidence grounding hallucination suppression documented in reports/phase14/PHASE14_REPORT.md and IEEE_INTEGRATION.md. Status: IN_PROGRESS.

## 24. Reproducibility Status
Full reproducibility suite implemented in `src/evaluation/reproducibility.py` (seed_everything, env capture, JSON run manifests, zero-leakage split validator). 302 automated unit and integration tests pass in `tests/` (100% pass rate). Prompt templates versioned with SHA-256 fingerprints. Run artifacts saved in `experiments/phase2/`, `experiments/phase2_5/`, `experiments/phase3/`, `experiments/phase4/artifacts/`, `experiments/phase5_1/`, `experiments/phase6/`, `experiments/phase7/`, and `experiments/phase8/` (calibration models, traces, benchmark summaries, ablations, bootstrap statistics). Status: CONFIRMED.

---

### Environment Facts
- Python: 3.14.6 — CONFIRMED
- GPU: NVIDIA RTX 3050 6GB Laptop GPU — CONFIRMED
- Driver: NVIDIA 581.95 (Supports CUDA 13.0 API) — CONFIRMED
- PyTorch: 2.14.1+cpu — CONFIRMED
- CUDA Runtime (PyTorch): NOT_AVAILABLE (CPU-only PyTorch active in Python 3.14 .venv) — CONFIRMED
- OS: Windows 11 AMD64 (Windows-11-10.0.26200-SP0) — CONFIRMED
- Git: Initialized (Commit 9ea3b89) — CONFIRMED
- Virtual Environment: `.venv` created and populated with dependencies — CONFIRMED
- Unit & Integration Tests: 302 passed in pytest suite (100% pass rate) — CONFIRMED
- Baselines Validated: B0, B1, B2, B0-U, B6-0 to B6-5, B7-0 to B7-5, A0 to A5 — CONFIRMED
- Quality Features Validated: 10 extractors (blur, noise, skew, glare, contrast, resolution, compression, illumination, occlusion, perspective) — CONFIRMED
- Experiments Validated: Phase 2 smoke (5/5), Phase 2.5 smoke (B0-U 100% match), Phase 3 validation (E3-VAL-QUALITY 9x5 grid), Phase 4 benchmark (E4-BENCHMARK 3,600 conditions), Phase 5.1 benchmark (E5_1-ROUTING 4,500 traces), Phase 6 benchmark (450 evaluations, H4 SUPPORTED), Phase 7 benchmark (750 evaluations, H5 SUPPORTED), Phase 8 benchmark (750 evaluations, H6 SUPPORTED) — CONFIRMED
