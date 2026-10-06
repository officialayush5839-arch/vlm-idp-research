# Metric Definition & Mathematical Rigor Audit

**Audited Commit:** `209d7eb`  
**Status:** PASS  

---

## 1. Mathematical Formulations Verified

### Coverage
$$\text{Coverage} = \frac{|\{i : \text{Action}_i \in \{\text{ACCEPT}, \text{ACCEPT\_WITH\_WARNING}\}\}|}{N}$$

### Selective Accuracy
$$\text{Acc}_{\text{sel}} = \frac{\sum_{i \in \text{Accepted}} \mathbb{I}(\hat{y}_i = y_i)}{|\text{Accepted}|}$$

### Selective Risk (Unsupported Answer Rate)
$$\text{Risk}_{\text{sel}} = 1 - \text{Acc}_{\text{sel}}$$

### Area Under Risk-Coverage Curve (AURC)
$$\text{AURC} = \int_0^1 \text{Risk}(c) \, dc$$
Implemented via trapezoidal numerical integration over empirical coverage points:
$$\text{AURC} = \sum_{k=1}^{M-1} \frac{\text{Risk}(c_k) + \text{Risk}(c_{k+1})}{2} (c_{k+1} - c_k)$$

### Brier Score
$$\text{Brier} = \frac{1}{N} \sum_{i=1}^N (p_i - y_i)^2$$

### Expected Calibration Error (ECE)
$$\text{ECE} = \sum_{b=1}^B \frac{|B_b|}{N} |\text{acc}(B_b) - \text{conf}(B_b)|$$

All implementations in `src/reliability/risk.py` and `src/reliability/metrics.py` conform exactly to standard ML literature definitions.
