# Evidence Sufficiency Assessment Report

## 1. Methodology
The sufficiency evaluator (`src/evidence/evidence_sufficiency.py`) determines whether candidate evidence units contain the essential entity terms required by the question:
- Stop-word filtering extracts discriminative query content tokens.
- Query entity coverage ratio:
  $$\text{Coverage} = \frac{|\text{Tokens}_{\text{Query\_Essential}} \cap \text{Tokens}_{\text{Evidence}}|}{|\text{Tokens}_{\text{Query\_Essential}}|}$$
- Three-level sufficiency taxonomy:
  - `SUFFICIENT`: $\text{Coverage} \ge 0.70$
  - `PARTIALLY_SUFFICIENT`: $0.40 \le \text{Coverage} < 0.70$
  - `INSUFFICIENT`: $\text{Coverage} < 0.40$

## 2. Experimental Results
- **B7-0 (Random)**: Sufficiency rate = 12.8% (87.2% of random runs lacked query entities).
- **B7-1 (BM25)**: Sufficiency rate = 44.0%.
- **B7-2 (Dense)**: Sufficiency rate = 32.0%.
- **B7-3 (Visual)**: Sufficiency rate = 52.0%.
- **B7-4 (Hybrid)**: Sufficiency rate = 44.0%.
- **B7-5 (Proposed)**: 20% strictly sufficient ($\ge 0.70$) and 80% partially sufficient ($\ge 0.40$), with 0% completely insufficient.

When evidence is incomplete, the system abstains or marks the status as `PARTIALLY_SUPPORTED` / `PARTIALLY_GROUNDED` rather than making unsupported assertions.
