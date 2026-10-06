"""src/recovery/safety_gate.py
Strict Phase 7 Evidence Verification & Safety Gate.
Prevents hallucination by requiring affirmative grounding support before emitting any recovered answer.
"""

from typing import Tuple
from src.reliability.signals import ObservableSignals


class EvidenceSafetyGate:
    """Certifies whether a recovered candidate satisfies safety constraints."""

    def __init__(
        self,
        min_sufficiency: float = 0.50,
        min_spatial: float = 0.40,
        max_discrepancy: float = 0.35,
    ):
        self.min_sufficiency = min_sufficiency
        self.min_spatial = min_spatial
        self.max_discrepancy = max_discrepancy

    def verify_safety(self, signals: ObservableSignals) -> Tuple[bool, str]:
        """Strict check: answers emitted must have verified grounding."""
        if signals.sufficiency_score < self.min_sufficiency:
            return False, f"Sufficiency score {signals.sufficiency_score:.3f} < {self.min_sufficiency}"

        if signals.spatial_score < self.min_spatial:
            return False, f"Spatial score {signals.spatial_score:.3f} < {self.min_spatial}"

        if signals.numeric_discrepancy > self.max_discrepancy:
            return False, f"Numeric discrepancy {signals.numeric_discrepancy:.3f} > {self.max_discrepancy}"

        return True, "Safety gate satisfied: verified grounding confirmed"
