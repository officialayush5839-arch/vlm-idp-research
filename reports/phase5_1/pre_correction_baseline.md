# PHASE 5.1 — PRE-CORRECTION BASELINE RECORD

**Phase**: Phase 5.1 — Scientific Correction & Revalidation  
**Baseline Anchor**: Commit `a01bed0` (`feat(phase5): implement adaptive quality-aware routing`)  
**Parent Commit**: `deacf9a` (`feat(phase4): implement controlled degradation benchmark`)  
**Timestamp**: 2026-10-05T05:40:00Z  
**Status**: `HISTORICAL_PHASE5_RESULT`  

---

## 1. Environment & Cryptographic State
- **Python Version**: `3.14.6`
- **Git Commit SHA**: `a01bed0`
- **Working Tree State**: Clean relative to `a01bed0`
- **Phase 5 Master Report SHA-256**: `9ef82f2a72bbd7e4c062b0f114b5563cfd3c1dce66eeeceece058905edb6bc5e`
- **Phase 5 Master Summary SHA-256**: `5643cad2fc21d9e41277a79f8f1c535792dcf73f27b001a3090c1ef766430369`

### Configuration Hashes:
- `configs/phase5/routing_config.yaml`: `e553bb8b8dea3a70912279704a240ecaa501ec6767eb00b4fe88581877b7acbc`
- `configs/phase5/router_rules.yaml`: `7a49c2b4648568c216b009a14d568613dc8b24be744bc2f857634979c9d5391a`
- `configs/phase5/uncertainty_config.yaml`: `ee7ec947f406a6406ddee984f893905f2c32bfaad1179115b351ed2528d0bb84`
- `configs/phase5/calibration_config.yaml`: `0444f295ad431d25f57e86a6b6c5727e0fa4a45fdd4ad15bc25b9adf65c130da`
- `configs/phase5/cost_config.yaml`: `79a6d5ccef9a66b7ae28f9f360eb9c0ea99222a4ad2bccb8863f2cd9b9fb8d6b`
- `configs/phase5/experiment_matrix.yaml`: `6c86af185f0743699fec865575e1a0a2f143fea0c762992a121a9b613f26df53`
- `configs/phase5/evaluation_config.yaml`: `958d8503557245ee8645f97f625dafd313584b01faece76c595ee59349779c8d`

---

## 2. Historical Phase 5 Primary Results (`HISTORICAL_PHASE5_RESULT`)

Evaluated across 900 benchmark conditions (4 datasets $\times$ 9 degradation families $\times$ 5 severities $\times$ 5 seeds = 4,500 deployable policy evaluations):

| Policy ID | Policy Identity | Mean Task Score | Std Dev | Rel. Compute Cost | Mean Regret | Fallback Rate | Model Alignment to Oracle |
|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **R0** | Oracle Upper Bound *(Non-deployable)* | 0.7956 | 0.1481 | 0.9022 | 0.0000 | 0.00% | 100.00% |
| **R1** | Fixed Best Baseline (B2) | 0.7778 | 0.1582 | 1.0000 | 0.0178 | 0.00% | 68.33% |
| **R2** | Rule-Based Quality Router | 0.7671 | 0.1708 | 0.9222 | 0.0284 | 0.00% | 73.33% |
| **R3** | Uncertainty-Directed Router | 0.6796 | 0.2009 | 0.9467 | 0.1160 | 35.56% | 66.11% |
| **R4** | Learned Router *(Uninitialized Fallback)* | 0.7778 | 0.1582 | 1.0000 | 0.0178 | 0.00% | 68.33% |
| **R5** | Composite Quality + Uncertainty | 0.7724 | 0.1621 | 0.9444 | 0.0231 | 0.00% | 71.67% |

### Historical Hypothesis H2 Statistical Result:
- **Treatment vs Control**: R2 (Rule-Based Quality Router) vs R1 (Fixed Best B2)
- **Observed Delta**: $\Delta = -0.0107$
- **Empirical 95% CI**: $[-0.0127, -0.0086]$
- **Empirical $p$-value**: $p < 0.0001$
- **Cliff's $\delta$**: $-0.0286$ (Negligible)
- **Cohen's $d$**: $-0.0648$ (Negligible)
- **Status**: `NOT_SUPPORTED` under task score superiority; demonstrated $7.78\%$ relative compute reduction.

---

## 3. Immutability Guarantee
This document establishes the historical scientific record of Phase 5. Under no circumstances will `experiments/phase5/` or commit `a01bed0` be altered, overwritten, or removed. All Phase 5.1 corrections and revalidations will exist exclusively within `experiments/phase5_1/`, `configs/phase5_1/`, and `reports/phase5_1/`.
