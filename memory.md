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

## 20. Current Phase
PHASE 1: Completed. Awaiting authorization to begin Phase 2. Status: CONFIRMED.

## 21. Current Task
Phase 1 verification and audit sign-off complete. Status: PASS.

## 22. Next Task
PHASE 2: Baseline OCR and VLM Pipelines (B0, B1, B2). Status: PLANNED.

## 23. Paper Status
Section I (Intro) and Section II (Related Work) drafted in `literature/related_work_notes.md`. Ingestion and normalization pipeline methodology documented in `reports/phase1/ingestion_validation.md`. Status: IN_PROGRESS.

## 24. Reproducibility Status
Full reproducibility suite implemented in `src/evaluation/reproducibility.py` (seed_everything, env capture, JSON run manifests, zero-leakage split validator). 39 automated unit tests pass in `tests/`. Status: CONFIRMED.

---

### Environment Facts
- Python: 3.14.6 — CONFIRMED
- GPU: NVIDIA RTX 3050 6GB Laptop GPU — CONFIRMED
- Driver: NVIDIA 581.95 (Supports CUDA 13.0 API) — CONFIRMED
- PyTorch: 2.14.1+cpu — CONFIRMED
- CUDA Runtime (PyTorch): NOT_AVAILABLE (CPU-only PyTorch active in Python 3.14 .venv) — CONFIRMED
- OS: Windows 11 AMD64 (Windows-11-10.0.26200-SP0) — CONFIRMED
- Git: Initialized (Commit bde2b53) — CONFIRMED
- Virtual Environment: `.venv` created and populated with dependencies — CONFIRMED
- Unit Tests: 39 passed in 3.5s — CONFIRMED
