# PHASE 5 SCIENTIFIC AUDIT — COMPUTATIONAL COST MODEL AUDIT

**Audit Item**: Cost Model Methodology, Relative Weights, and 7.78% Compute Reduction Claim  
**Audit Status**: VERIFIED AS RELATIVE COST MODEL / REQUIRES EXPLICIT QUALIFICATION (P2 — Conceptual Distinction)  

---

## 1. Audit Target
The Phase 5 report states:
> *"R2 achieved an average relative compute weight of 0.9222, delivering 7.78% compute savings relative to running B2 unconditionally on all documents"*

The audit investigated whether this 7.78% figure represents physically measured energy consumption, floating-point operations (FLOPs), or an architectural cost proxy.

---

## 2. Code Trace & Cost Calculation
In `src/routing/cost.py` and `configs/phase5/cost_config.yaml`:
- Compute costs are defined via normalized relative architectural weights:
  $$\mathbf{w}_{\text{compute}} = \{ \text{B0}: 0.10, \, \text{B0-U}: 0.50, \, \text{B1}: 0.80, \, \text{B2}: 1.00 \}$$
- R1 (Fixed Best Baseline) selects B2 on 100% of conditions:
  $$\text{Cost}(\text{R1}) = 1.0000$$
- R2 (Rule-Based Quality Router) selection distribution across 900 conditions:
  - Selected B2: 760 times ($84.44\%$)
  - Selected B0-U: 140 times ($15.56\%$)
  - Selected B0: 0 times
  - Selected B1: 0 times
- Total compute units consumed by R2:
  $$\text{Total Cost}(\text{R2}) = (760 \times 1.00) + (140 \times 0.50) = 760 + 70 = 830 \text{ compute units}$$
- Mean compute cost per condition:
  $$\overline{\text{Cost}}(\text{R2}) = \frac{830}{900} = 0.922222\dots \approx \mathbf{0.9222}$$
- Relative compute reduction:
  $$\Delta_{\text{cost}} = \frac{1.0000 - 0.922222}{1.0000} = 7.7777\dots\% \approx \mathbf{7.78\%}$$

The arithmetic of the reported 7.78% savings is **100% mathematically verified**.

---

## 3. Scientific Distinction: Measured vs Modeled Cost
- **Physical FLOPs / Wattage**: NOT MEASURED. The local environment operated on CPU (`CUDA = NOT_AVAILABLE`). No hardware profiler (e.g., `nvml`, `torch.cuda.Event`, or physical power meter) was engaged.
- **Nature of the Metric**: This is a **Relative Engineering Cost Model** assigning fixed fractional weights based on model architecture parameter scale (B0: lightweight OCR $\sim 0.1\times$, B0-U: compact multimodal OCR $\sim 0.5\times$, B2: monolithic 7B parameter VLM $\equiv 1.0\times$).

## 4. IEEE Manuscript Disclosure Requirement
The IEEE paper must explicitly state:
> *"Computational savings are evaluated under a normalized architectural cost model ($w_{\text{B0}}=0.10, w_{\text{B0-U}}=0.50, w_{\text{B1}}=0.80, w_{\text{B2}}=1.00$), yielding a theoretical 7.78% reduction in computational demand, rather than direct physical energy measurements."*
