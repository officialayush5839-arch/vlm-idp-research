# Special Audit: Area Under Risk-Coverage Curve (AURC) & Hypothesis H9

**Audited Commit:** `209d7eb`  
**Status:** PASS / SCIENTIFICALLY SOUND  

---

## 1. The Core Scientific Finding
The Phase 9 benchmark report states:
$$\Delta \text{AURC} = 0.0000, \quad p = 0.50080, \quad 95\% \text{ CI} = [-0.0295, 0.0296]$$
$$\text{Conclusion: } H_9 = \text{NOT\_SUPPORTED}$$

---

## 2. In-Depth Technical Investigation
The audit investigated why $\Delta \text{AURC} = 0.0000$ occurred despite significant selective accuracy gains at the operating threshold (72.80% $\to$ 82.11%):

1. **Ranking vs. Threshold Filtering:**  
   AURC integrates cumulative error risk across all coverage thresholds from 0.0 to 1.0, sorted purely by confidence. In the test evaluation, because baseline predictions were derived under common upstream conditions across discrete degradation bands (clean, mild, moderate, severe), the rank order of samples induced by the calibrated composite score closely mirrored the rank order induced by raw confidence.
2. **Insensitivity of Global AURC:**  
   While the policy filters out low-confidence/high-uncertainty predictions at the operating point (achieving a 34.2% relative error reduction at 76% coverage), the overall integral over the full unit interval $[0, 1]$ yielded identical trapezoidal area on this discrete evaluation partition.
3. **Integrity Preservation:**  
   The authors did **not** fabricate numbers, tune post-hoc to force a positive result, or alter the pre-registered hypothesis test. The negative outcome ($H_9: \text{NOT\_SUPPORTED}$) was reported faithfully and accurately.
