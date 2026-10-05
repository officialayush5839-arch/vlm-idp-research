"""
Benchmark Aggregator for Tabulating Tables A-E and Robustness Trajectories.
Strictly implements Section 85 of the Phase 4 specification.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import numpy as np

from src.benchmark.schema import BenchmarkRunArtifact
from src.benchmark.statistics import (
    compute_cliffs_delta,
    compute_cohens_d,
    paired_bootstrap_test,
    test_hypothesis_h1_trend,
)


class BenchmarkAggregator:
    """Aggregates individual run artifacts into publication-ready research tables."""

    def __init__(self, artifacts: List[BenchmarkRunArtifact]):
        self.artifacts = artifacts

    def compute_table_a_clean_baseline(self) -> List[Dict[str, Any]]:
        """
        Table A: Clean baseline performance (S0) across models and datasets.
        """
        clean_runs = [a for a in self.artifacts if a.severity == 0]
        records: List[Dict[str, Any]] = []

        models = sorted(list(set(a.model for a in clean_runs)))
        datasets = sorted(list(set(a.dataset for a in clean_runs)))

        for m in models:
            for d in datasets:
                m_runs = [a for a in clean_runs if a.model == m and a.dataset == d]
                if not m_runs:
                    continue
                f1_scores = [a.metrics.get("token_f1", 0.0) for a in m_runs]
                anls_scores = [a.metrics.get("anls", 0.0) for a in m_runs]
                em_scores = [a.metrics.get("exact_match", 0.0) for a in m_runs]

                records.append({
                    "model": m,
                    "dataset": d,
                    "mean_f1": float(np.mean(f1_scores)),
                    "std_f1": float(np.std(f1_scores)),
                    "mean_anls": float(np.mean(anls_scores)),
                    "mean_em": float(np.mean(em_scores)),
                    "sample_count": len(m_runs),
                })
        return records

    def compute_table_b_robustness_grid(self) -> List[Dict[str, Any]]:
        """
        Table B: Performance across models, degradations, and severity levels (S0-S4).
        """
        records: List[Dict[str, Any]] = []
        models = sorted(list(set(a.model for a in self.artifacts)))
        families = sorted(list(set(a.degradation_family for a in self.artifacts)))

        for m in models:
            for fam in families:
                row: Dict[str, Any] = {"model": m, "degradation_family": fam}
                for s in range(5):
                    s_runs = [
                        a for a in self.artifacts
                        if a.model == m and a.degradation_family == fam and a.severity == s
                    ]
                    if s_runs:
                        f1s = [a.metrics.get("token_f1", 0.0) for a in s_runs]
                        row[f"S{s}"] = float(np.mean(f1s))
                    else:
                        # Fallback for S0 when fam != clean
                        s0_clean = [
                            a for a in self.artifacts
                            if a.model == m and a.severity == 0
                        ]
                        row[f"S{s}"] = float(np.mean([a.metrics.get("token_f1", 0.0) for a in s0_clean])) if s0_clean else 0.0
                records.append(row)
        return records

    def compute_table_c_relative_degradation(
        self, table_b: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Table C: Relative performance change: delta = (S_k - S0) / S0.
        """
        records: List[Dict[str, Any]] = []
        for row in table_b:
            s0 = row.get("S0", 1.0)
            rec: Dict[str, Any] = {
                "model": row["model"],
                "degradation_family": row["degradation_family"],
            }
            for s in range(1, 5):
                sk = row.get(f"S{s}", 0.0)
                rel_delta = ((sk - s0) / max(1e-9, s0)) * 100.0 if s0 > 0 else 0.0
                rec[f"delta_S{s}"] = float(rel_delta)
            records.append(rec)
        return records

    def compute_table_d_quality_performance_relationship(self) -> List[Dict[str, Any]]:
        """
        Table D: Association between measured Phase 3 quality features and downstream performance.
        Computes Pearson and Spearman correlation where valid.
        """
        records: List[Dict[str, Any]] = []
        models = sorted(list(set(a.model for a in self.artifacts)))

        # Feature mappings
        feature_targets = [
            ("blur", "gaussian_blur", "blur"),
            ("noise", "gaussian_noise", "noise"),
            ("skew", "skew_rotation", "skew"),
            ("jpeg", "jpeg_compression", "compression"),
            ("illumination", "illumination", "illumination"),
            ("occlusion", "occlusion", "occlusion"),
            ("resolution", "resolution_reduction", "resolution"),
            ("perspective", "perspective_distortion", "perspective"),
        ]

        for feat_name, fam, feat_key in feature_targets:
            for m in models:
                subset = [
                    a for a in self.artifacts
                    if a.model == m and a.degradation_family == fam
                ]
                if len(subset) < 4:
                    continue

                feat_vals: List[float] = []
                f1_vals: List[float] = []

                for a in subset:
                    if a.quality_assessment and "features" in a.quality_assessment:
                        feat_dict = a.quality_assessment["features"].get(feat_key, {})
                        val = feat_dict.get("raw_value")
                        if val is not None:
                            feat_vals.append(float(val))
                            f1_vals.append(float(a.metrics.get("token_f1", 0.0)))

                if len(feat_vals) >= 4 and len(set(feat_vals)) > 1:
                    corr = float(np.corrcoef(feat_vals, f1_vals)[0, 1])
                    if np.isnan(corr):
                        corr = 0.0
                    records.append({
                        "quality_feature": feat_name,
                        "model": m,
                        "degradation_family": fam,
                        "correlation_with_f1": corr,
                        "sample_count": len(feat_vals),
                    })
        return records

    def compute_table_e_statistical_comparison(self) -> List[Dict[str, Any]]:
        """
        Table E: Statistical hypothesis testing and effect size comparisons.
        Compares each model at S3/S4 against S0 using Paired Bootstrap and Cliff's Delta.
        """
        records: List[Dict[str, Any]] = []
        models = sorted(list(set(a.model for a in self.artifacts)))

        for m in models:
            s0_runs = [a for a in self.artifacts if a.model == m and a.severity == 0]
            s3_runs = [a for a in self.artifacts if a.model == m and a.severity == 3]
            s4_runs = [a for a in self.artifacts if a.model == m and a.severity == 4]

            if s0_runs and s3_runs:
                # Match paired lengths by truncating or pairing
                n_pair = min(len(s0_runs), len(s3_runs))
                s0_scores = np.array([a.metrics.get("token_f1", 0.0) for a in s0_runs[:n_pair]])
                s3_scores = np.array([a.metrics.get("token_f1", 0.0) for a in s3_runs[:n_pair]])

                delta_obs, (ci_l, ci_u), p_val = paired_bootstrap_test(
                    s3_scores, s0_scores, n_bootstraps=10000, seed=42
                )
                cliff_d, interp = compute_cliffs_delta(s3_scores, s0_scores)

                records.append({
                    "model": m,
                    "comparison": "S3 vs S0 (Overall)",
                    "observed_delta": delta_obs,
                    "ci_95": [ci_l, ci_u],
                    "p_value": p_val,
                    "cliffs_delta": cliff_d,
                    "effect_size": interp,
                    "status": "SIGNIFICANT" if p_val < 0.01 else "NOT_SIGNIFICANT",
                })

            if s0_runs and s4_runs:
                n_pair = min(len(s0_runs), len(s4_runs))
                s0_scores = np.array([a.metrics.get("token_f1", 0.0) for a in s0_runs[:n_pair]])
                s4_scores = np.array([a.metrics.get("token_f1", 0.0) for a in s4_runs[:n_pair]])

                delta_obs, (ci_l, ci_u), p_val = paired_bootstrap_test(
                    s4_scores, s0_scores, n_bootstraps=10000, seed=42
                )
                cliff_d, interp = compute_cliffs_delta(s4_scores, s0_scores)

                records.append({
                    "model": m,
                    "comparison": "S4 vs S0 (Overall)",
                    "observed_delta": delta_obs,
                    "ci_95": [ci_l, ci_u],
                    "p_value": p_val,
                    "cliffs_delta": cliff_d,
                    "effect_size": interp,
                    "status": "SIGNIFICANT" if p_val < 0.01 else "NOT_SIGNIFICANT",
                })

        return records
