# agents.md — AGENT OPERATING MANUAL

PROJECT TITLE: Adaptive, Uncertainty-Aware and Evidence-Grounded Vision-Language Document Intelligence under Real-World Visual Degradation

This file tells future coding/research agents how to operate under the seven control files.

## 1. Project Context
- This is an IEEE research project, NOT a generic app
- Research domain: VLM-based Intelligent Document Processing
- Primary novelty: Intersection of degradation-aware processing + evidence grounding + uncertainty estimation

## 2. Control File System
The project is governed by 7 control files, ordered by hierarchy:
1. `rules.md`: The non-negotiable constitution and ultimate source of truth.
2. `goal.md`: The research direction and objectives.
3. `prd.md`: Specific project requirements and specifications.
4. `architecture.md`: Technical design and structure.
5. `phases.md`: The roadmap and current progress.
6. `task.md`: Execution plan for the current objective.
7. `memory.md`: Records actual state (never overrides requirements).

If a conflict is discovered between files, record it and refer to the hierarchy above. Do NOT silently resolve conflicts.

## 3. Mandatory Pre-Modification Procedure
Before modifying any code, agents MUST:
1. Read `rules.md`
2. Read `goal.md`
3. Read `memory.md`
4. Read relevant section of `architecture.md`
5. Read current `task.md`
6. Determine current phase from `phases.md`

## 4. Mandatory Post-Modification Procedure
After completing work, agents MUST:
1. Update `task.md`
2. Update `memory.md`
3. Record experiment/config changes
4. Run relevant tests
5. Report what changed
6. Report what remains

## 5. Anti-Fabrication Policy
Agents must NEVER invent or fabricate data, metrics, or results. All values must be explicitly measured or derived. 
Use the mandatory provenance statuses:
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

## 6. Phase Gate Requirements
- Phases have strict acceptance criteria and exit criteria.
- No phase can be marked complete without explicit verification of all exit criteria.

## 7. Experiment Protocol
- Experiment records must include: seeds (3-5), model versions, prompt versions, and configurations.
- Statistical reporting must include: mean, standard deviation, 95% CI, and effect size.
- Use paired bootstrap or justified statistical tests. Never report only p-values.
- Never tune on test data.
- Freeze evaluation protocols before testing.

## 8. Architecture Principles
- Refer to `architecture.md` for full technical details.
- Guiding principles: Modularity, Configuration-driven design, Reproducibility, Fail-safe execution.

## 9. What This Project Is NOT
- NOT a document chatbot
- NOT a production system
- NOT a demo app
- NOT hardware/IoT
