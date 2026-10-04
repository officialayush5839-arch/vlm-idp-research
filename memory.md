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
No experiments run. Status: NOT_RUN.

## 11. Failed Experiments
None yet. Status: NOT_AVAILABLE.

## 12. Model Versions
None installed. Status: NOT_AVAILABLE.

## 13. Prompt Versions
None created. Status: NOT_AVAILABLE.

## 14. Configuration Decisions
pyproject.toml + hatchling, .venv, YAML configs in `configs/phase0/`. Status: CONFIRMED.

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

## 20. Current Phase
PHASE 2: Completed. Awaiting authorization to begin Phase 3 (Document Quality/Degradation Module). Status: CONFIRMED.

## 21. Current Task
Phase 2 verification, baseline establishment, and audit sign-off complete. Status: PASS.

## 22. Next Task
PHASE 3: Document Quality/Degradation Assessment Module. Status: PLANNED.

## 23. Paper Status
Section I (Intro) and Section II (Related Work) drafted in `literature/related_work_notes.md`. Ingestion and normalization pipeline methodology documented in `reports/phase1/ingestion_validation.md`. Baseline architectures and fairness specifications documented in `reports/phase2/baseline_registry.md`. Status: IN_PROGRESS.

## 24. Reproducibility Status
Full reproducibility suite implemented in `src/evaluation/reproducibility.py` (seed_everything, env capture, JSON run manifests, zero-leakage split validator). 59 automated unit tests pass in `tests/`. Prompt templates versioned with SHA-256 fingerprints. Run artifacts saved in `experiments/phase2/artifacts/`. Status: CONFIRMED.

---

### Environment Facts
- Python: 3.14.6 — CONFIRMED
- GPU: NVIDIA RTX 3050 6GB Laptop GPU — CONFIRMED
- Driver: NVIDIA 581.95 (Supports CUDA 13.0 API) — CONFIRMED
- PyTorch: 2.14.1+cpu — CONFIRMED
- CUDA Runtime (PyTorch): NOT_AVAILABLE (CPU-only PyTorch active in Python 3.14 .venv) — CONFIRMED
- OS: Windows 11 AMD64 (Windows-11-10.0.26200-SP0) — CONFIRMED
- Git: Initialized (Commit 609ac2d) — CONFIRMED
- Virtual Environment: `.venv` created and populated with dependencies — CONFIRMED
- Unit Tests: 59 passed in 50.5s — CONFIRMED
- Smoke Experiments: E2-SMOKE-B0 (5/5), E2-SMOKE-B1 (5/5), E2-SMOKE-B2 (5/5), E2-REPRO-B0 (100% repeatability) — CONFIRMED
