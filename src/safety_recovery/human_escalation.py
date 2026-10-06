"""src/safety_recovery/human_escalation.py
Deterministic Human-in-the-Loop Escalation Package Generator.
"""

from typing import List, Dict, Any, Optional
from src.reliability.signals import ObservableSignals
from src.safety_recovery.schema import HumanReviewPackage, RiskLevel


class HumanEscalationController:
    """Formats prioritized review packages with precise bounding boxes for human review."""

    @staticmethod
    def create_package(
        document_id: str,
        query_id: str,
        candidate_answer: Optional[str],
        signals: ObservableSignals,
        failed_layers: List[str],
        page_id: int = 1,
    ) -> HumanReviewPackage:
        # Determine risk level based on failed layers and uncertainty
        unc_norm = round(1.0 - signals.raw_confidence, 3)
        if unc_norm > 0.60 or "layer4_numeric_consistency" in failed_layers:
            risk = RiskLevel.CRITICAL
        elif unc_norm > 0.40 or len(failed_layers) >= 3:
            risk = RiskLevel.HIGH
        elif len(failed_layers) >= 1:
            risk = RiskLevel.MEDIUM
        else:
            risk = RiskLevel.LOW

        # Generate localized inspection bounding box
        regions = []
        if signals.quality_score < 0.60:
            regions.append([0.1, 0.1, 0.45, 0.9])  # Visual blur / header area
        if signals.spatial_score < 0.50 or "layer2_spatial_grounding" in failed_layers:
            regions.append([0.45, 0.1, 0.85, 0.9])  # Grounding / entity region

        if not regions:
            regions.append([0.2, 0.2, 0.8, 0.8])

        reason_str = f"Verification failed on {', '.join(failed_layers)}" if failed_layers else "Uncertainty exceeds safety tolerance"
        suggested_action = "Inspect highlighted visual bounding boxes; verify numeric values and table row alignment."

        return HumanReviewPackage(
            document_id=document_id,
            page_id=page_id,
            query_id=query_id,
            candidate_answer=candidate_answer,
            evidence_regions=regions,
            confidence=signals.raw_confidence,
            uncertainty_norm=unc_norm,
            risk_level=risk,
            failure_reason=reason_str,
            suggested_action=suggested_action,
            citations=["cite_doc_page_1"],
        )
