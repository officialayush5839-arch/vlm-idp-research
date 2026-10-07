"""Phase 14 Cluster-Aware Statistical Testing Engine.

Implements cluster bootstrapping at the document family level (B=10,000 resamples),
calculating paired differences, empirical 95% confidence intervals, and Holm-Bonferroni
corrected p-values across pre-registered hypotheses.
"""

from typing import Dict, List, Any, Tuple
import numpy as np
import pandas as pd

def cluster_bootstrap_paired(
    df: pd.DataFrame,
    col_a: str,
    col_b: str,
    cluster_col: str = "family_id",
    n_resamples: int = 10000,
    seed: int = 42
) -> Dict[str, Any]:
    rng = np.random.RandomState(seed)
    families = df[cluster_col].unique()
    n_families = len(families)

    diff_actual = float(np.mean(df[col_b] - df[col_a]))

    boot_diffs = []
    family_groups = {fam: sub for fam, sub in df.groupby(cluster_col)}

    for _ in range(n_resamples):
        sampled_fams = rng.choice(families, size=n_families, replace=True)
        sampled_sub = pd.concat([family_groups[fam] for fam in sampled_fams], ignore_index=True)
        boot_diffs.append(float(np.mean(sampled_sub[col_b] - sampled_sub[col_a])))

    boot_diffs = np.array(boot_diffs)
    ci_lower = float(np.percentile(boot_diffs, 2.5))
    ci_upper = float(np.percentile(boot_diffs, 97.5))

    # Two-sided empirical p-value against zero
    p_val = float(2.0 * min(np.mean(boot_diffs <= 0), np.mean(boot_diffs >= 0)))
    p_val = min(1.0, max(0.0, p_val))

    return {
        "mean_diff": diff_actual,
        "ci_lower": ci_lower,
        "ci_upper": ci_upper,
        "p_value": p_val,
        "n_resamples": n_resamples,
        "n_clusters": n_families
    }

def apply_holm_bonferroni(p_values: List[float]) -> List[float]:
    n = len(p_values)
    indexed = sorted(enumerate(p_values), key=lambda x: x[1])
    adjusted = [0.0] * n
    running_max = 0.0
    for rank, (orig_idx, p) in enumerate(indexed):
        adj = (n - rank) * p
        adj = min(1.0, max(running_max, adj))
        running_max = adj
        adjusted[orig_idx] = adj
    return adjusted
