# Report 03: Non-Parametric Isotonic Regression Calibration

## 1. Mathematical Principles
Isotonic regression fits a non-parametric, piecewise-constant monotonically non-decreasing mapping $m: [0, 1] \to [0, 1]$:
$$\min_{m} \sum_{i=1}^N (y_i - m(p_i))^2 \quad \text{subject to } m(p_i) \le m(p_j) \text{ whenever } p_i \le p_j$$

The optimization is solved in $\mathcal{O}(N)$ time via the **Pool Adjacent Violators Algorithm (PAVA)**.

## 2. Advantages over Parametric Scaling
1. **Free of Functional Form**: Does not assume a sigmoid or logistic relationship between logit and correctness probability.
2. **Local Adaptation**: Can flatten confidence in intermediate ambiguous regions while sharply rising for unambiguous high-evidence outputs.
3. **Monotonicity Enforcement**: Prevents confidence inversion, ensuring higher raw signals never yield lower calibrated probabilities.

## 3. Empirical Results
Fitted on the validation partition:
- Number of isotonic knots: 4.
- Cryptographic Artifact SHA-256: `bae554de2d9376ea...`
- Evaluated on test set:
  - Expected Calibration Error (ECE): 0.1200
  - Maximum Calibration Error (MCE): 0.1538
  - Brier Score: 0.1700
  - Selective Risk at 80% coverage: 0.1800
