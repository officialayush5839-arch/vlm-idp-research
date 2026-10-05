# PHASE 5 SCIENTIFIC AUDIT — AUDIT SCOPE

**Project Title**: Adaptive, Uncertainty-Aware and Evidence-Grounded Vision-Language Document Intelligence under Real-World Visual Degradation  
**Audit Target**: Phase 5 Implementation, Experiments, Artifacts, and Conclusions  
**Auditor**: Formal Scientific Audit Agent  
**Date**: 2026-10-05  
**Governing Documents**: `rules.md`, `goal.md`, `prd.md`, `architecture.md`, `phases.md`, `memory.md`, `task.md`, `research_protocol.md`  

---

## 1. Audit Objective
The primary objective of this audit is to conduct an uncompromising, evidence-grounded scientific inspection of Phase 5 (Adaptive Routing). The audit does not accept claims in `PHASE5_REPORT.md` at face value. Instead, every major claim, metric, and methodological choice is traced end-to-end:
$$\text{Claim} \longrightarrow \text{Source Code} \longrightarrow \text{Configuration} \longrightarrow \text{Experiment Artifact} \longrightarrow \text{Raw/Summary Data} \longrightarrow \text{Statistical Calculation} \longrightarrow \text{Report}$$

## 2. In-Scope Artifacts & Systems
1. **Source Code**:
   - `src/routing/` (all 13 Python modules: `schema.py`, `feature_adapter.py`, `rule_engine.py`, `uncertainty.py`, `calibration.py`, `learned_router.py`, `policy.py`, `fallback.py`, `cost.py`, `decision_trace.py`, `audit.py`, `router.py`, `pipeline.py`).
   - `src/benchmark/` (`model_runner.py`, `degradation_runner.py`, `evaluator.py`, `statistics.py`).
2. **Configurations**:
   - `configs/phase5/` (`routing_config.yaml`, `router_rules.yaml`, `uncertainty_config.yaml`, `calibration_config.yaml`, `cost_config.yaml`, `experiment_matrix.yaml`, `evaluation_config.yaml`).
3. **Execution Scripts**:
   - `scripts/run_phase5_smoke.py`
   - `scripts/run_phase5_validation.py`
   - `scripts/run_phase5_benchmark.py`
   - `scripts/run_phase5_ablations.py`
4. **Experimental Artifacts & Summaries**:
   - `experiments/phase5/summaries/E5_ROUTING_summary.json`
   - `experiments/phase5/calibration/calibration_metrics.json`
   - `experiments/phase5/ablations/ablation_summary.json`
   - `experiments/phase5/index.json`
   - `experiments/phase5/routing_traces/` (all serialized traces)
5. **Phase Reports**:
   - `reports/phase5/` (all 12 individual reports and `PHASE5_REPORT.md`).
6. **Governance & Protocols**:
   - `protocol/` (dataset, split, degradation, baseline, evaluation, uncertainty, grounding, statistical, reproducibility protocols).
   - `task.md`, `phases.md`, `memory.md`.

## 3. Out-of-Scope Items
- Implementation of Phase 6 (Long-Document Multimodal Retrieval). Phase 6 implementation is strictly forbidden during this audit.
- Modifying Phase 5 decision thresholds post-hoc to rescue failed hypotheses.
- Re-tuning the router on the test set.
- Pushing to remote Git repositories.

## 4. Audit Evidence Standards
- **VERIFIED**: Directly supported by reproducible source code, immutable configurations, cryptographic hashes, and exact numerical alignment with experiment artifacts.
- **UNVERIFIED**: Stated in documentation or reports but lacking execution logs, stored data, or verifiable code paths.
- **CONTRADICTED**: Factually at variance with repository code, stored artifact records, or statistical mathematics.
