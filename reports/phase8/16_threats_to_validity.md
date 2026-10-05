# Report 16: Comprehensive Threats to Validity (Construct, Internal, External, Conclusion)

## 1. Construct Validity
- **Threat**: Does selective risk accurately capture the operational cost of errors in document processing?
- **Mitigation**: We report multiple complementary metrics: selective risk at standard operational thresholds (e.g. 80% coverage), Area Under Risk-Coverage (AURC), Brier score, and AUROC for correctness discrimination. Both parametric (NLL, ECE) and non-parametric ranking criteria were assessed.

## 2. Internal Validity
- **Threat**: Did test information leak into the calibrator parameters or threshold selection?
- **Mitigation**: Complete partition isolation was enforced. Calibrators and coverage thresholds were fitted exclusively on the 15-document validation partition. A static AST audit confirmed zero access to gold labels or degradation identities at test runtime. Calibration artifacts were hashed and cryptographically verified before and after evaluation.

## 3. External Validity
- **Threat**: Do synthetic degradation patterns and simulated retrieval distributions reflect real enterprise environments?
- **Mitigation**: Degradation transforms incorporate standardized physical noise models (Gaussian blur, sensor noise, illumination, skew). Future work will validate on real physical scan corpora (e.g., RVL-CDIP scanned receipts).

## 4. Conclusion Validity
- **Threat**: Are observed improvements in selective accuracy and risk reductions statistically robust or artifacts of random seed variance?
- **Mitigation**: All test evaluations were executed across five distinct protocol seeds (42, 123, 456, 789, 101112) comprising 125 full evaluation runs. Statistical significance for Hypothesis H6 was established via 10,000 paired bootstrap resamples, yielding $p < 0.0001$ with a 95% confidence interval strictly bounded away from zero.
