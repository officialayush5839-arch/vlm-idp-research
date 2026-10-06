"""src/recovery/preprocessing.py
Strategy A: Observable Visual Preprocessing and Image Restoration.
"""

from typing import Dict, Any, Tuple
import numpy as np
from src.reliability.signals import ObservableSignals


class VisualPreprocessingRecovery:
    """Simulates/applies visual restoration to improve signal quality under visual degradation."""

    def __init__(
        self,
        contrast_boost: float = 0.15,
        sharpening_boost: float = 0.12,
        expected_quality_gain: float = 0.22,
    ):
        self.contrast_boost = contrast_boost
        self.sharpening_boost = sharpening_boost
        self.expected_quality_gain = expected_quality_gain

    def apply_recovery(self, signals: ObservableSignals) -> ObservableSignals:
        """Applies restoration transform to observable signals.
        Quality and sufficiency improve monotonically under restoration,
        while maintaining observable provenance.
        """
        # Restored visual quality
        new_quality = min(1.0, signals.quality_score + self.expected_quality_gain)
        # Improved OCR legibility and semantic grounding
        new_sufficiency = min(1.0, signals.sufficiency_score + 0.18)
        new_spatial = min(1.0, signals.spatial_score + 0.15)
        new_conf = min(1.0, signals.raw_confidence + 0.15)

        return ObservableSignals(
            retrieval_score=signals.retrieval_score,
            semantic_score=signals.semantic_score,
            spatial_score=new_spatial,
            numeric_discrepancy=max(0.0, signals.numeric_discrepancy - 0.10),
            table_alignment_score=signals.table_alignment_score,
            sufficiency_score=new_sufficiency,
            quality_score=new_quality,
            agreement_score=signals.agreement_score,
            raw_confidence=new_conf,
        )
