# Phase 7 Scientific Grounding Protocol

## 1. Overview and Objectives
Phase 7 establishes the formal Evidence Grounding and Answer-Support Verification subsystem of the VLM-IDP research project. The objective is to verify whether evidence retrieved across long documents and degraded conditions provides valid, semantically supportive, and sufficient evidence to answer document intelligence questions.

## 2. Experimental Coordinate Space
- **Coordinate System**: Normalized integer coordinates in the range $[0, 1000]$ where $(0, 0)$ is top-left and $(1000, 1000)$ is bottom-right.
- **Conversion to Pixel Space**:
  $$x_{\text{pixel}} = \left\lfloor \frac{x_{1000}}{1000} \times W \right\rceil, \quad y_{\text{pixel}} = \left\lfloor \frac{y_{1000}}{1000} \times H \right\rceil$$
- **IoU Thresholds**:
  - Relaxed IoU: $\text{IoU} \ge 0.50$
  - Strict IoU: $\text{IoU} \ge 0.75$

## 3. Four-State Decision State Machine
The evidence grounding decision tree maps evidence packages to four mutually exclusive states:
1. `INSUFFICIENT_EVIDENCE`: Retrieved evidence lacks sufficient query entities or is completely empty.
2. `NOT_SUPPORTED`: Evidence fails spatial overlap against ground truth or fails semantic/numeric verification.
3. `PARTIALLY_SUPPORTED`: Evidence satisfies basic query requirements and spatial bounds, but exhibits partial semantic overlap or entity coverage.
4. `SUPPORTED`: Complete spatial alignment ($\text{IoU} \ge 0.75$), exact semantic/numeric verification, and complete query entity coverage.

## 4. Anti-Fabrication & Zero-Leakage Governance
- No oracle answer labels or ground-truth bounding boxes are accessed at runtime.
- Static AST audit continuously verifies that runtime modules never query gold targets.
- All evaluation thresholds are pre-configured in `configs/phase7/*.yaml` without test-set tuning.
