# Phase 5 — Routing Policy Specifications

## 1. Overview of Routing Policies
Six distinct routing paradigms are formalized and benchmarked in Phase 5:

| Policy ID | Policy Name | Paradigm | Input Data | Target Model | Deployable |
|:---|:---|:---|:---|:---|:---:|
| **R0** | Oracle Upper Bound | Retrospective Max | Ground-truth candidate scores | $\arg\max_m \text{Score}(m)$ | **NO** (Upper Bound Only) |
| **R1** | Fixed Best Baseline | Monolithic Default | None | B2 (`Qwen2.5-VL-7B`) | **YES** |
| **R2** | Rule-Based Quality Router | Deterministic Boundaries | Phase 3 Quality Vector (10 dims) | B0 / B1 / B2 / B0-U | **YES** |
| **R3** | Uncertainty-Directed Router | Confidence Gating | 6-Signal Uncertainty Vector $\mathbf{u}$ | B0 / B1 / B2 | **YES** |
| **R4** | Lightweight Learned Router | Logistic Regression | 10 Quality Dimensions | B0 / B1 / B2 / B0-U | **YES** |
| **R5** | Composite Router | Quality Rules + Escalation | Quality Vector + Uncertainty $\mathbf{u}$ | B0 / B1 / B2 / B0-U | **YES** |

---

## 2. Policy Specifications

### R0: Oracle Upper Bound (NON-DEPLOYABLE)
- **Mathematical Definition**: $m^* = \arg\max_{m \in \{B0, B1, B2, B0-U\}} S(m, x)$
- **Purpose**: Establishes the theoretical performance ceiling achievable if routing were perfectly prescient.
- **Protocol Constraint**: Strictly prohibited from running at inference time without explicit retrospective simulation. Raises `ValueError` if invoked without candidate evaluation outcomes.

### R1: Fixed Best Baseline
- **Mathematical Definition**: $m^* = \text{B2}$
- **Purpose**: Represents the current standard in document intelligence: routing all queries to the most capable multimodal model unconditionally.

### R2: Rule-Based Quality Router (Primary Contribution)
- **Inputs**: $\mathbf{q} = [q_{\text{blur}}, q_{\text{noise}}, q_{\text{skew}}, q_{\text{glare}}, q_{\text{contrast}}, q_{\text{res}}, q_{\text{comp}}, q_{\text{illum}}, q_{\text{occ}}, q_{\text{persp}}]$
- **Rules**:
  1. If $q_{\text{skew}} \ge 0.25$ or $q_{\text{persp}} \ge 0.25 \implies \text{B2}$ (geometric resilience)
  2. If $q_{\text{blur}} \ge 0.40$ or $q_{\text{noise}} \ge 0.40 \implies \text{B2}$ (heavy token corruption)
  3. If $q_{\text{comp}} \ge 0.50$ or $q_{\text{illum}} \ge 0.50$ or $q_{\text{glare}} \ge 0.45 \implies \text{B0-U}$ (multimodal compression robustness)
  4. If $q_{\text{occ}} \ge 0.30 \implies \text{B2}$ (contextual reasoning over cutoffs)
  5. If clean boundary satisfied across all dimensions $\implies \text{B0}$ (efficiency on pristine documents)
  6. Default fallback $\implies \text{B2}$

### R3: Uncertainty-Directed Router
- **Inputs**: Composite confidence $c = \sum_{i=1}^6 w_i u_i$
- **Rules**:
  - $c \ge \tau_{\text{accept}} (0.75) \implies \text{B0}$
  - $\tau_{\text{review}} (0.40) \le c < \tau_{\text{accept}} \implies \text{B1}$
  - $c < \tau_{\text{review}} \implies \text{B2}$

### R4: Lightweight Learned Router
- **Inputs**: 10-dimensional quality vector.
- **Model**: Regularized Logistic Regression ($L_2, C=1.0$) trained on validation split model selections.

### R5: Composite Quality + Uncertainty Policy
- **Logic**: Evaluates R2 rule boundaries. If R2 proposes a lightweight model (B0 or B1) but the composite uncertainty confidence $c < \tau_{\text{review}} (0.40)$, the policy automatically escalates to the robust native VLM B2.
