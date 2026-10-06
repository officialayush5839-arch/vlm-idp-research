# Abstention Decision Policy Audit

**Audited Commit:** `209d7eb`  
**Status:** PASS  

---

## 1. Decision Logic Structure
The decision engine in `src/reliability/abstention.py` implements a 4-tier cascaded policy:
1. **`ACCEPT`**: $\text{Confidence} \ge \tau_{\text{accept}} \land \text{Uncertainty} \le u_{\text{max\_accept}}$
2. **`ACCEPT_WITH_WARNING`**: $\text{Confidence} \ge \tau_{\text{warning}} \land \text{Uncertainty} \le u_{\text{max\_warning}}$
3. **`ESCALATE`**: $\text{Confidence} \ge \tau_{\text{escalate}} \land \text{Uncertainty} \le u_{\text{max\_escalate}}$
4. **`ABSTAIN`**: All other conditions.

---

## 2. Decision Distribution on Benchmark (750 Traces)
- **B9-0 (No Abstention):** 100% `ACCEPT` (125/125 runs)
- **B9-1 (Grounding Gate):** 52% `ACCEPT`, 48% `ABSTAIN`
- **B9-5 (Proposed Multi-Signal):** 76% `ACCEPT` / `ACCEPT_WITH_WARNING`, 24% `ESCALATE` / `ABSTAIN`

The decision boundaries demonstrate clear selective behavior, effectively downgrading degraded documents into escalation/abstention states.
