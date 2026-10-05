"""
Observable Signal Extraction for Phase 8 Uncertainty Estimation.
Extracts inference-time features from Phase 3 quality, Phase 6 retrieval,
and Phase 7 grounding outputs with zero ground-truth leakage.
"""

import math
from typing import Dict, Any, List, Optional
from src.uncertainty.schema import UncertaintyFeatures


def compute_normalized_entropy(scores: List[float]) -> float:
    """
    Compute normalized Shannon entropy in [0, 1] for a candidate score distribution.
    """
    if len(scores) <= 1:
        return 0.0

    # Convert scores to pseudo-probabilities via softmax or linear normalization
    pos_scores = [max(0.0, float(s)) for s in scores]
    tot = sum(pos_scores)
    if tot <= 1e-8:
        # Uniform if all zero
        return 1.0

    probs = [s / tot for s in pos_scores]
    k = len(probs)
    max_ent = math.log2(k)
    if max_ent <= 0:
        return 0.0

    ent = -sum(p * math.log2(p) for p in probs if p > 1e-8)
    return float(max(0.0, min(1.0, ent / max_ent)))


def compute_score_margin(scores: List[float]) -> float:
    """
    Compute normalized score margin between top-1 and top-2 candidates: (s1 - s2) / s1.
    """
    if len(scores) <= 1:
        return 1.0
    sorted_scores = sorted(scores, reverse=True)
    s1, s2 = sorted_scores[0], sorted_scores[1]
    if s1 <= 1e-8:
        return 0.0
    margin = (s1 - s2) / s1
    return float(max(0.0, min(1.0, margin)))


class SignalExtractor:
    """
    Assembles observable uncertainty signals from upstream pipeline outputs.
    """

    def extract_features(
        self,
        model_confidence: float = 1.0,
        page_retrieval_scores: Optional[List[float]] = None,
        region_retrieval_scores: Optional[List[float]] = None,
        phase7_support_result: Optional[Dict[str, Any]] = None,
        phase7_grounding_result: Optional[Dict[str, Any]] = None,
        citations_count: int = 1,
        quality_features: Optional[Dict[str, float]] = None,
        overall_quality: float = 1.0,
        page_count: int = 1
    ) -> UncertaintyFeatures:
        """
        Assemble UncertaintyFeatures from observable pipeline context.
        """
        # 1. Model confidence
        m_conf = float(max(0.0, min(1.0, model_confidence)))

        # 2. Retrieval signals
        ret_scores = page_retrieval_scores or [1.0]
        if region_retrieval_scores:
            ret_scores = region_retrieval_scores
        r_margin = compute_score_margin(ret_scores)
        r_entropy = compute_normalized_entropy(ret_scores)

        # 3. Grounding signals
        p7_supp = phase7_support_result or {}
        p7_gnd = phase7_grounding_result or {}

        sem_score = float(max(0.0, min(1.0, p7_supp.get("semantic_score", 1.0))))
        cov_score = float(max(0.0, min(1.0, p7_supp.get("coverage_score", 1.0))))
        spat_score = float(max(0.0, min(1.0, p7_supp.get("spatial_score", 1.0))))
        suff_status = p7_supp.get("sufficiency_status", p7_gnd.get("evidence_sufficiency_status", "SUFFICIENT"))
        gnd_status = p7_gnd.get("grounding_status", "GROUNDED")

        if suff_status not in ["SUFFICIENT", "PARTIALLY_SUFFICIENT", "INSUFFICIENT"]:
            suff_status = "SUFFICIENT"
        if gnd_status not in ["GROUNDED", "PARTIALLY_GROUNDED", "UNSUPPORTED"]:
            gnd_status = "GROUNDED"

        # 4. Document Quality signals
        q_feats = quality_features or {}
        vis_qual = float(max(0.0, min(1.0, overall_quality)))
        blur = float(max(0.0, min(1.0, q_feats.get("blur", 0.0))))
        noise = float(max(0.0, min(1.0, q_feats.get("noise", 0.0))))
        skew = float(max(0.0, min(1.0, q_feats.get("skew", 0.0))))
        contrast = float(max(0.0, min(1.0, q_feats.get("contrast", 1.0))))
        resolution = float(max(0.0, min(1.0, q_feats.get("resolution", 1.0))))

        return UncertaintyFeatures(
            model_confidence=m_conf,
            retrieval_margin=r_margin,
            retrieval_entropy=r_entropy,
            semantic_support_score=sem_score,
            entity_coverage=cov_score,
            spatial_valid=spat_score,
            sufficiency_status=suff_status,
            grounding_status=gnd_status,
            citation_count=citations_count,
            visual_quality_score=vis_qual,
            quality_blur=blur,
            quality_noise=noise,
            quality_skew=skew,
            quality_contrast=contrast,
            quality_resolution=resolution,
            page_count=max(1, page_count)
        )
