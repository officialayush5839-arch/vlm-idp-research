"""src/recovery/escalation.py
Strategy E: Deterministic Human Escalation Flagging with Inspection Regions.
"""

from typing import List
from src.recovery.schema import InspectionRegion
from src.reliability.signals import ObservableSignals


class HumanEscalationManager:
    """Formats prioritized inspection regions for deterministic human escalation."""

    def __init__(self, max_regions: int = 3):
        self.max_regions = max_regions

    def generate_inspection_regions(
        self,
        signals: ObservableSignals,
        page_id: int = 1,
    ) -> List[InspectionRegion]:
        """Creates deterministic bounding regions where visual defects or uncertainty peaked."""
        regions = []

        # If visual quality degraded, flag full page header / body
        if signals.quality_score < 0.60:
            regions.append(
                InspectionRegion(
                    page_id=page_id,
                    bbox=[0.1, 0.1, 0.5, 0.9],
                    defect_type="severe_blur_or_noise",
                    uncertainty_score=round(1.0 - signals.quality_score, 3),
                    description="Visual quality degraded below confidence cutoff; manual inspection required",
                )
            )

        # If spatial / sufficiency was weak, flag content area
        if signals.spatial_score < 0.50 or signals.sufficiency_score < 0.50:
            regions.append(
                InspectionRegion(
                    page_id=page_id,
                    bbox=[0.5, 0.1, 0.9, 0.9],
                    defect_type="spatial_grounding_gap",
                    uncertainty_score=round(1.0 - signals.spatial_score, 3),
                    description="Grounding overlap low; verify bounding box alignment manually",
                )
            )

        return regions[: self.max_regions]
