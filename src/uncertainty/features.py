"""
Feature Aggregator and Composite Confidence Estimator for Phase 8.
Synthesizes observable signals into composite raw confidence scores.
"""

from typing import Dict, Any, Optional
from src.uncertainty.schema import UncertaintyFeatures


class FeatureAggregator:
    """
    Computes weighted linear composite confidence from UncertaintyFeatures.
    """

    def __init__(
        self,
        weight_model: float = 0.25,
        weight_retrieval: float = 0.20,
        weight_grounding: float = 0.30,
        weight_quality: float = 0.25,
        config: Optional[Dict[str, Any]] = None
    ):
        if config and "feature_weights" in config:
            fw = config["feature_weights"]
            weight_model = fw.get("model_confidence", weight_model)
            weight_retrieval = fw.get("retrieval_quality", weight_retrieval)
            weight_grounding = fw.get("grounding_support", weight_grounding)
            weight_quality = fw.get("visual_quality", weight_quality)

        tot = weight_model + weight_retrieval + weight_grounding + weight_quality
        self.w_model = weight_model / tot
        self.w_ret = weight_retrieval / tot
        self.w_gnd = weight_grounding / tot
        self.w_qual = weight_quality / tot

    def compute_composite_confidence(self, features: UncertaintyFeatures) -> float:
        """
        Compute normalized composite raw confidence in [0.0, 1.0].
        """
        # 1. Model component
        c_model = features.model_confidence

        # 2. Retrieval component
        c_ret = 0.60 * features.retrieval_margin + 0.40 * (1.0 - features.retrieval_entropy)

        # 3. Grounding component
        suff_penalty = 1.0
        if features.sufficiency_status == "PARTIALLY_SUFFICIENT":
            suff_penalty = 0.70
        elif features.sufficiency_status == "INSUFFICIENT":
            suff_penalty = 0.20

        gnd_penalty = 1.0
        if features.grounding_status == "PARTIALLY_GROUNDED":
            gnd_penalty = 0.75
        elif features.grounding_status == "UNSUPPORTED":
            gnd_penalty = 0.10

        c_gnd = (
            0.40 * features.semantic_support_score +
            0.30 * features.entity_coverage +
            0.30 * features.spatial_valid
        ) * suff_penalty * gnd_penalty

        # 4. Quality component
        q_penalty = max(features.quality_blur, features.quality_noise, features.quality_skew)
        c_qual = features.visual_quality_score * (1.0 - 0.50 * q_penalty)

        composite = (
            self.w_model * c_model +
            self.w_ret * c_ret +
            self.w_gnd * c_gnd +
            self.w_qual * c_qual
        )
        return float(max(0.0, min(1.0, round(composite, 6))))
