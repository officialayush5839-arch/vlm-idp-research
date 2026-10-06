"""src/robustness/statistical_tests.py
Statistical hypothesis testing (paired bootstrap B=10,000, seed=42) and Holm-Bonferroni correction.
"""

from typing import List, Dict, Any, Tuple
import numpy as np


class RobustnessStatisticalTester:
    """Executes paired bootstrap tests and multiple-comparison control for Phase 10."""

    @staticmethod
    def paired_bootstrap_test(
        scores_a: List[float],
        scores_b: List[float],
        replications: int = 10000,
        random_seed: int = 42,
    ) -> Dict[str, Any]:
        """Tests H0: diff <= 0 (where scores_a is proposed and scores_b is baseline)."""
        arr_a = np.array(scores_a, dtype=float)
        arr_b = np.array(scores_b, dtype=float)
        diff = arr_a - arr_b
        observed_mean_diff = float(np.mean(diff))

        rng = np.random.RandomState(random_seed)
        n = len(diff)
        boot_means = []
        for _ in range(replications):
            idx = rng.randint(0, n, size=n)
            boot_means.append(float(np.mean(diff[idx])))

        boot_means = np.array(boot_means)
        p_val = float(np.mean(boot_means <= 0.0))
        ci_lower = float(np.percentile(boot_means, 2.5))
        ci_upper = float(np.percentile(boot_means, 97.5))

        # Cohen's d effect size
        std_diff = np.std(diff, ddof=1) if np.std(diff, ddof=1) > 0 else 1e-6
        effect_size = float(observed_mean_diff / std_diff)

        conclusion = "SUPPORTED" if (p_val < 0.05 and observed_mean_diff > 0) else "NOT_SUPPORTED"

        return {
            "observed_diff": round(observed_mean_diff, 4),
            "p_value": round(p_val, 5),
            "ci_95": [round(ci_lower, 4), round(ci_upper, 4)],
            "effect_size_d": round(effect_size, 4),
            "replications": replications,
            "conclusion": conclusion,
        }

    @staticmethod
    def holm_bonferroni_correction(p_values: List[float], alpha: float = 0.05) -> List[bool]:
        """Applies Holm-Bonferroni step-down procedure."""
        m = len(p_values)
        sorted_indices = np.argsort(p_values)
        reject = [False] * m

        for rank, idx in enumerate(sorted_indices):
            thresh = alpha / (m - rank)
            if p_values[idx] <= thresh:
                reject[idx] = True
            else:
                break
        return reject
