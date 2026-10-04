# rules.md — NON-NEGOTIABLE PROJECT CONSTITUTION

PROJECT TITLE: Adaptive, Uncertainty-Aware and Evidence-Grounded Vision-Language Document Intelligence under Real-World Visual Degradation

This is the supreme governing document. It overrides ALL other files when conflicts exist.

## 1. Research Integrity Rules
- Never fabricate data, model performance, dataset results, citations
- Never claim a result before executing the experiment
- Never claim IEEE acceptance is guaranteed
- Never call the system 'state of the art' without evidence
- Every claimed contribution requires an ablation
- Every major conclusion requires experimental evidence
- Negative results must not be hidden
- Failed experiments must be recorded
- Synthetic degradation must never be presented as equivalent to real degradation

## 2. Dataset Integrity Rules
- Never leak test documents into training
- Keep original documents immutable
- Derived degradation variants inherit the source split (if clean doc is in test, ALL degraded variants of that doc are in test)
- Record dataset versions and hashes

## 3. Experiment Integrity Rules
- Never tune on test data
- Freeze final evaluation protocol before final test
- Store every configuration
- Record seeds (minimum 3, preferably 5)
- Record model versions
- Record prompt versions
- Report: mean, standard deviation, 95% CI, effect size
- Use paired bootstrap or justified statistical test
- Do not report only p-values

## 4. Engineering Integrity Rules
- No hard-coded paths
- No silent failures
- No hidden preprocessing
- No undocumented model changes
- No deleting experiment outputs without a record
- No overwriting original data
- Configuration files for all parameters

## 5. Anti-Fabrication Rules
NEVER invent: accuracy, F1, mAP, IoU, ECE, Brier score, latency, GPU usage, dataset size, number of samples, number of pages, statistical significance, p-values, confidence intervals — unless actually measured.

Use provenance statuses:
- `NOT_RUN` — experiment not executed
- `NOT_AVAILABLE` — data not available
- `DERIVED` — value inferred from other data
- `DECLARED` — manually specified project requirement
- `CONFLICT` — conflicting sources exist
- `PLANNED` — scheduled but not started
- `IN_PROGRESS` — currently being worked on
- `PASS` / `FAIL` — verified result
- `BLOCKED` — cannot proceed
- `UNVERIFIED` — exists but not validated
- `CONFIRMED` — validated and verified

## 6. Agent Behavior Protocol
Before modifying code:
1. Read rules.md
2. Read goal.md
3. Read memory.md
4. Read relevant section of architecture.md
5. Read current task.md
6. Determine current phase from phases.md

After completing work:
1. Update task.md
2. Update memory.md
3. Record experiment/config changes
4. Run relevant tests
5. Report what changed
6. Report what remains

## 7. File Hierarchy & Conflict Resolution
If two files conflict:
1. `rules.md` wins (constitution)
2. Then `goal.md` (direction)
3. Then `prd.md` (requirements)
4. Then `architecture.md` (design)
5. Then `phases.md` (roadmap)
6. Then `task.md` (execution)
7. `memory.md` records actual state, never overrides requirements

If a conflict is discovered: record it, do NOT silently resolve.

## 8. Scope Control
Software-only project. Do NOT introduce: hardware sensors, IoT, robotics, physical scanners, embedded systems, camera hardware. Scope: Software, AI/ML, VLM, OCR, document processing, retrieval, grounding, uncertainty, robustness, experimentation, IEEE research.

## 9. Research Direction Changes
Never silently change: research direction, primary model, datasets, metrics, evaluation methodology. If a change is necessary:
1. Explain why
2. Record the decision
3. Update the appropriate MD file
4. Record the previous decision
5. Record the new decision
6. Explain impact on reproducibility
