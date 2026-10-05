"""
Deterministic Rule-Based Quality Routing Engine for Phase 5.
Loads explicit decision boundaries from YAML and maps visual quality state to model selection.
Strictly non-leaking and configuration-driven.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional, Tuple
import yaml


class RuleBasedQualityRouter:
    """
    Evaluates inference-time quality features against YAML-configured thresholds
    to select the most appropriate document processing baseline.
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.thresholds = config.get("thresholds", {})
        self.router_version = config.get("version", "1.0.0")

    @classmethod
    def from_config(cls, config_path: Optional[str] = None) -> RuleBasedQualityRouter:
        if config_path is None:
            config_path = str(Path(__file__).parents[2] / "configs" / "phase5" / "router_rules.yaml")
        with open(config_path, "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f)
        return cls(cfg)

    def route(self, features: Dict[str, float]) -> Tuple[str, str, float]:
        """
        Determine model choice given normalized visual quality features.
        Returns: (selected_model, decision_reason, confidence)
        """
        # 1. Geometric Distortion Check (Skew & Perspective)
        geom = self.thresholds.get("geometric_distortion", {})
        skew = features.get("skew", 0.0)
        perspective = features.get("perspective", 0.0)
        if skew >= geom.get("min_skew", 0.25) or perspective >= geom.get("min_perspective", 0.25):
            reason = f"Geometric distortion detected (skew={skew:.2f}, perspective={perspective:.2f}); routing to B2 native VLM."
            return geom.get("target_model", "B2"), reason, 0.90

        # 2. Severe Blur or Sensor Noise Check
        blur_noise = self.thresholds.get("severe_blur_or_noise", {})
        blur = features.get("blur", 0.0)
        noise = features.get("noise", 0.0)
        if blur >= blur_noise.get("min_blur", 0.40) or noise >= blur_noise.get("min_noise", 0.40):
            reason = f"Severe blur or noise detected (blur={blur:.2f}, noise={noise:.2f}); routing to B2 native VLM."
            return blur_noise.get("target_model", "B2"), reason, 0.88

        # 3. Compression and Illumination Distortion (JPEG blocking, glare, attenuation)
        comp_illum = self.thresholds.get("compression_and_illumination", {})
        comp = features.get("compression", 0.0)
        illum = features.get("illumination", 0.0)
        glare = features.get("glare", 0.0)
        if (
            comp >= comp_illum.get("min_compression", 0.50)
            or illum >= comp_illum.get("min_illumination_attenuation", 0.50)
            or glare >= comp_illum.get("min_glare", 0.45)
        ):
            reason = (
                f"Compression or illumination distortion detected (compression={comp:.2f}, "
                f"illum={illum:.2f}, glare={glare:.2f}); routing to B0-U multimodal OCR."
            )
            return comp_illum.get("target_model", "B0-U"), reason, 0.85

        # 4. Severe Occlusion Check
        occ = self.thresholds.get("severe_occlusion", {})
        occlusion = features.get("occlusion", 0.0)
        if occlusion >= occ.get("min_occlusion", 0.30):
            reason = f"Severe occlusion detected (occlusion={occlusion:.2f}); routing to B2 native VLM."
            return occ.get("target_model", "B2"), reason, 0.86

        # 5. Clean Document Boundary Check
        clean = self.thresholds.get("clean_boundary", {})
        is_clean = (
            blur <= clean.get("max_blur", 0.20)
            and noise <= clean.get("max_noise", 0.20)
            and skew <= clean.get("max_skew", 0.15)
            and perspective <= clean.get("max_perspective", 0.15)
            and occlusion <= clean.get("max_occlusion", 0.10)
            and comp <= clean.get("max_compression", 0.25)
        )
        if is_clean:
            reason = "Clean document quality verified across all visual dimensions; routing to efficient B0 OCR."
            return clean.get("target_model", "B0"), reason, 0.95

        # 6. Default Fallback
        default_fb = self.thresholds.get("default_fallback", {})
        target = default_fb.get("target_model", "B2")
        reason = f"Moderate or unclassified degradation profile; routing to robust default baseline {target}."
        return target, reason, 0.80
