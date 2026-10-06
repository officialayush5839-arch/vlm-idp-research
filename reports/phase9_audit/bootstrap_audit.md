# Paired Bootstrap Hypothesis Testing Audit (H9)

**Audited Commit:** `209d7eb`  
**Status:** PASS  

---

## 1. Bootstrap Parameters & Verification
- **Target Hypothesis:** $H_9$ (Uncertainty-aware selective prediction reduces unsupported answer rate vs. unconditional prediction).
- **Comparison Systems:** B9-5 (Proposed) vs. B9-0 (No Abstention).
- **Replications ($B$):** 10,000
- **Random Seed:** 42
- **Test Metric:** $\Delta \text{AURC} = \text{AURC}(\text{B9-0}) - \text{AURC}(\text{B9-5})$

---

## 2. Statistical Metrics
- $\Delta \text{AURC} = 0.0000$
- Two-sided $p$-value: $0.50080$
- 95% Confidence Interval: $[-0.0295, 0.0296]$
- Outcome: **NOT_SUPPORTED**

The bootstrap procedure was executed rigorously according to protocol.
