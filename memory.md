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
PHASE 0: Literature Freeze + Research Protocol (Completed: 2026-10-04). Status: CONFIRMED.

## 20. Current Phase
PHASE 1: Repository + Environment + Infrastructure & Ingestion. Status: IN_PROGRESS.

## 21. Current Task
T002: Create environment specification (`pyproject.toml`, `.venv`). Status: IN_PROGRESS.

## 22. Next Task
T003: Create requirements/dependency lock files. Status: PLANNED.

## 23. Paper Status
Section I (Intro) and Section II (Related Work) drafted in `literature/related_work_notes.md`. Status: IN_PROGRESS.

## 24. Reproducibility Status
Reproducibility protocol locked in `protocol/reproducibility_protocol.md` (seed policy, JSON run schema, Git commit tracking). Status: CONFIRMED.

---

### Environment Facts
- Python: 3.14.6 — CONFIRMED
- GPU: NVIDIA RTX 3050 6GB Laptop GPU — CONFIRMED
- CUDA: NOT_AVAILABLE (CPU-only PyTorch installed)
- OS: Windows — CONFIRMED
- Git: Initialized — CONFIRMED
- Virtual Environment: Not created — PLANNED
