"""src/reliability/signals.py
Signal extraction from observable pipeline outputs across Phases 3, 6, 7, and 8.
Enforces strict zero-leakage invariant: No gold labels or ground-truth values consumed.
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class ObservableSignals:
    """Observable raw features extracted without ground truth."""
    retrieval_score: float = 0.0
    semantic_score: float = 0.0
    spatial_score: float = 0.0
    numeric_discrepancy: float = 0.0
    table_alignment_score: float = 0.0
    sufficiency_score: float = 0.0
    quality_score: float = 1.0
    agreement_score: float = 1.0
    raw_confidence: float = 0.5


class SignalExtractor:
    """Extracts observable signals from upstream component outputs."""

    @staticmethod
    def extract(
        phase3_output: Optional[Dict[str, Any]] = None,
        phase6_output: Optional[Dict[str, Any]] = None,
        phase7_output: Optional[Dict[str, Any]] = None,
        phase8_output: Optional[Dict[str, Any]] = None,
    ) -> ObservableSignals:
        sig = ObservableSignals()

        # Phase 3: Visual quality
        if phase3_output:
            sig.quality_score = float(phase3_output.get("quality_score", 1.0))

        # Phase 6: Retrieval confidence & margin
        if phase6_output:
            sig.retrieval_score = float(
                phase6_output.get("retrieval_score", phase6_output.get("top1_score", 0.0))
            )

        # Phase 7: Grounding & verification scores
        if phase7_output:
            sig.semantic_score = float(phase7_output.get("semantic_similarity", 0.0))
            sig.spatial_score = float(phase7_output.get("spatial_overlap", 0.0))
            sig.numeric_discrepancy = float(phase7_output.get("numeric_discrepancy", 0.0))
            sig.table_alignment_score = float(phase7_output.get("table_alignment_score", 0.0))
            sig.sufficiency_score = float(phase7_output.get("sufficiency_score", 0.0))

        # Phase 8: Agreement & raw confidence
        if phase8_output:
            sig.agreement_score = float(phase8_output.get("agreement_score", 1.0))
            sig.raw_confidence = float(phase8_output.get("raw_confidence", 0.5))

        return sig
