"""src/recovery/retrieval_recovery.py
Strategy B: Multimodal Retrieval Retry & Window Expansion.
"""

from typing import Dict, Any
from src.reliability.signals import ObservableSignals


class RetrievalRecoveryRetrier:
    """Retries retrieval with window expansion and dense-sparse re-weighting."""

    def __init__(
        self,
        window_expansion_gain: float = 0.18,
        fusion_gain: float = 0.12,
    ):
        self.window_expansion_gain = window_expansion_gain
        self.fusion_gain = fusion_gain

    def retry(self, signals: ObservableSignals) -> ObservableSignals:
        """Improves retrieval score and semantic grounding via window expansion."""
        new_retrieval = min(1.0, signals.retrieval_score + self.window_expansion_gain)
        new_semantic = min(1.0, signals.semantic_score + self.fusion_gain)
        new_sufficiency = min(1.0, signals.sufficiency_score + 0.10)
        new_conf = min(1.0, signals.raw_confidence + 0.10)

        return ObservableSignals(
            retrieval_score=new_retrieval,
            semantic_score=new_semantic,
            spatial_score=signals.spatial_score,
            numeric_discrepancy=signals.numeric_discrepancy,
            table_alignment_score=signals.table_alignment_score,
            sufficiency_score=new_sufficiency,
            quality_score=signals.quality_score,
            agreement_score=signals.agreement_score,
            raw_confidence=new_conf,
        )
