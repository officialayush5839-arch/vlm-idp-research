"""src/robustness/shift_detector.py
Detection and quantification of distribution shifts relative to reference validation profile.
Uses Wasserstein distance and Population Stability Index (PSI) on observable features.
"""

import math
from typing import Dict, Any
from src.robustness.schema import DomainID, ObservableDistributionProfile, DistributionShiftMetrics


class ShiftDetector:
    """Quantifies distributional divergence between a domain profile and validation reference."""

    @staticmethod
    def detect_shift(
        reference_profile: ObservableDistributionProfile,
        target_profile: ObservableDistributionProfile,
    ) -> DistributionShiftMetrics:
        # Standardized Mean Difference across observable density and visual quality
        d_qual = abs(reference_profile.mean_visual_quality - target_profile.mean_visual_quality)
        d_tokens = abs(reference_profile.mean_token_count - target_profile.mean_token_count) / (
            reference_profile.mean_token_count + 1e-6
        )
        d_density = abs(reference_profile.mean_text_density - target_profile.mean_text_density) / (
            reference_profile.mean_text_density + 1e-6
        )

        smd = float((d_qual + d_tokens + d_density) / 3.0)

        # Wasserstein distance approximation on normalized vectors
        ref_vec = [
            reference_profile.mean_text_density,
            reference_profile.mean_region_density / 10.0,
            reference_profile.mean_visual_quality,
        ]
        tgt_vec = [
            target_profile.mean_text_density,
            target_profile.mean_region_density / 10.0,
            target_profile.mean_visual_quality,
        ]
        w_dist = float(sum(abs(r - t) for r, t in zip(ref_vec, tgt_vec)) / len(ref_vec))

        # Population Stability Index (PSI) proxy
        eps = 1e-4
        psi = 0.0
        for r, t in zip(ref_vec, tgt_vec):
            r_clamped = max(eps, min(1.0, r))
            t_clamped = max(eps, min(1.0, t))
            psi += (t_clamped - r_clamped) * math.log(t_clamped / r_clamped)
        psi = max(0.0, float(psi))

        if psi < 0.10:
            classification = "STABLE"
        elif psi < 0.25:
            classification = "MODERATE_SHIFT"
        else:
            classification = "SIGNIFICANT_SHIFT"

        return DistributionShiftMetrics(
            domain_id=target_profile.domain_id,
            standardized_mean_diff=round(smd, 4),
            wasserstein_distance=round(w_dist, 4),
            population_stability_index=round(psi, 4),
            shift_classification=classification,
        )
