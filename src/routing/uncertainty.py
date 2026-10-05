"""
Uncertainty Signal Adapter for Phase 5.
Extracts and combines the 6-signal composite uncertainty vector per protocol/uncertainty_protocol.md.
Signals: [u_vlm, u_ocr, u_ret, u_gnd, u_qual, u_agr].
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional
import yaml

from src.routing.schema import UncertaintyVector


class UncertaintyAdapter:
    """
    Assembles normalized multi-signal uncertainty vectors from pipeline context.
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.signals = config.get("signals", {})
        self.weights = {k: v.get("default_weight", 1.0 / 6.0) for k, v in self.signals.items()}
        self.tau_accept = config.get("decision_thresholds", {}).get("tau_accept", 0.75)
        self.tau_review = config.get("decision_thresholds", {}).get("tau_review", 0.40)

    @classmethod
    def from_config(cls, config_path: Optional[str] = None) -> UncertaintyAdapter:
        if config_path is None:
            config_path = str(Path(__file__).parents[2] / "configs" / "phase5" / "uncertainty_config.yaml")
        with open(config_path, "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f)
        return cls(cfg)

    def assemble_vector(
        self,
        vlm_confidence: float = 1.0,
        ocr_confidence: float = 1.0,
        retrieval_score: float = 1.0,
        grounding_score: float = 1.0,
        visual_quality_score: float = 1.0,
        ocr_vlm_agreement: float = 1.0,
    ) -> UncertaintyVector:
        """
        Clamps and packages the 6 pipeline uncertainty signals into an UncertaintyVector.
        """
        def _clamp(val: float) -> float:
            return float(max(0.0, min(1.0, val)))

        return UncertaintyVector(
            u_vlm=_clamp(vlm_confidence),
            u_ocr=_clamp(ocr_confidence),
            u_ret=_clamp(retrieval_score),
            u_gnd=_clamp(grounding_score),
            u_qual=_clamp(visual_quality_score),
            u_agr=_clamp(ocr_vlm_agreement),
        )

    def compute_weighted_confidence(self, u_vec: UncertaintyVector) -> float:
        """
        Computes linearly weighted heuristic confidence score in [0.0, 1.0].
        """
        vals = {
            "u_vlm": u_vec.u_vlm,
            "u_ocr": u_vec.u_ocr,
            "u_ret": u_vec.u_ret,
            "u_gnd": u_vec.u_gnd,
            "u_qual": u_vec.u_qual,
            "u_agr": u_vec.u_agr,
        }
        total_w = sum(self.weights.values()) or 1.0
        weighted_sum = sum(vals[k] * self.weights.get(k, 1.0 / 6.0) for k in vals)
        return float(max(0.0, min(1.0, weighted_sum / total_w)))
