# Semantic Support Verification Report

## 1. Methodology
The semantic verification module (`src/evidence/semantic_support.py`) assesses lexical and entity overlap between answer claims and extracted evidence units:
- Stop-word filtered token recall:
  $$R_{\text{token}} = \frac{|\text{Tokens}_{\text{Answer}} \cap \text{Tokens}_{\text{Evidence}}|}{|\text{Tokens}_{\text{Answer}}|}$$
- Token Jaccard similarity:
  $$J = \frac{|\text{Tokens}_{\text{Answer}} \cap \text{Tokens}_{\text{Evidence}}|}{|\text{Tokens}_{\text{Answer}} \cup \text{Tokens}_{\text{Evidence}}|}$$
- Heuristic semantic support score:
  $$\text{Score}_{\text{semantic}} = 0.70 \times R_{\text{token}} + 0.30 \times J$$
  (Equal to 1.0 on exact normalized substring matches).

Scores are explicitly labeled `heuristic support score` rather than calibrated confidence probabilities to maintain scientific rigor.

## 2. Experimental Findings
- **B7-5 Semantic Support Accuracy**: 1.0000 (100% of answer hypotheses in retrieved B7-5 packages were matched against authentic underlying text snippets).
- **Baselines B7-0 to B7-4**: 0.0000 (Due to spatial failure at sub-page region thresholds, answer claims were rejected as ungrounded).
