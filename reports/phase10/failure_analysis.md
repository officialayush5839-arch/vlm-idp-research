# Phase 10 Failure Analysis under Distribution Shift

**Audited Phase:** Phase 10  
**Status:** COMPLETE  

---

## 1. Domain-Specific Failure Modes

1. **$D_1$ Layout Shift (Dense Tabular):**  
   - Main failure mode: Numeric misalignment and table column fragmentation.  
   - Abstention coverage remained high (100%), but accuracy decreased from 92% to 84% due to subtle multi-column misattributions.
2. **$D_2$ Visual Style Shift (Heavy Scan Blur / Noise):**  
   - Main failure mode: Visual token distortion and OCR illegibility.  
   - Safe failure behavior: The 8D uncertainty vector detected high visual quality degradation ($u_{\text{quality}} > 0.65$), triggering 100% abstention/escalation and preventing hallucinated answers.
3. **$D_3$ Structure Shift (Complex Form Layout):**  
   - Main failure mode: Spatial bounding box dispersion across sparse fields.  
   - Accuracy degraded to 68% (gap of +0.24).
4. **$D_4$ Combined Shift:**  
   - Severe stress compounding blur and structural fragmentation.  
   - Triggered 100% safe abstention in Proposed B10-4.
