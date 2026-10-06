"""src/reliability/baselines.py
Phase 9 Baseline Implementations:
- B9-0: No Abstention (always ACCEPT)
- B9-1: Grounding-Only Gate
- B9-2: Fixed Confidence Threshold
- B9-3: Quality-Only Reliability
- B9-4: Evidence-Only Reliability
- B9-5: Proposed Multi-Signal Calibrated Reliability
"""

from typing import Dict, Any, Optional
from src.reliability.schema import ReliabilityAction, ReliabilityDecision, UncertaintyVector
from src.reliability.signals import ObservableSignals
from src.reliability.uncertainty import UncertaintyCalculator
from src.reliability.confidence import RawConfidenceModel, CalibratedCompositeModel
from src.reliability.abstention import AbstentionPolicy


class BaselineB9_0_NoAbstention:
    """B9-0: Unconditional prediction, always ACCEPT."""

    def evaluate(self, signals: ObservableSignals) -> ReliabilityDecision:
        return ReliabilityDecision(
            action=ReliabilityAction.ACCEPT,
            confidence=signals.raw_confidence,
            uncertainty_norm=0.0,
            operating_point="unconditional",
            reason="Baseline B9-0: No abstention policy applied",
        )


class BaselineB9_1_GroundingGate:
    """B9-1: Accept only if grounding sufficiency and spatial score are high."""

    def evaluate(self, signals: ObservableSignals) -> ReliabilityDecision:
        if signals.sufficiency_score >= 0.70 and signals.spatial_score >= 0.50:
            action = ReliabilityAction.ACCEPT
            reason = "Grounding verification gate satisfied"
        else:
            action = ReliabilityAction.ABSTAIN
            reason = "Grounding verification gate failed"

        return ReliabilityDecision(
            action=action,
            confidence=signals.raw_confidence,
            uncertainty_norm=1.0 - signals.sufficiency_score,
            operating_point="grounding_gate",
            reason=reason,
        )


class BaselineB9_2_FixedConfidence:
    """B9-2: Fixed threshold on raw confidence."""

    def __init__(self, threshold: float = 0.75):
        self.threshold = threshold

    def evaluate(self, signals: ObservableSignals) -> ReliabilityDecision:
        if signals.raw_confidence >= self.threshold:
            action = ReliabilityAction.ACCEPT
            reason = f"Raw confidence >= {self.threshold}"
        else:
            action = ReliabilityAction.ABSTAIN
            reason = f"Raw confidence < {self.threshold}"

        return ReliabilityDecision(
            action=action,
            confidence=signals.raw_confidence,
            uncertainty_norm=1.0 - signals.raw_confidence,
            operating_point="fixed_confidence",
            reason=reason,
        )


class BaselineB9_3_QualityGate:
    """B9-3: Abstains based solely on Phase 3 visual degradation score."""

    def __init__(self, quality_threshold: float = 0.65):
        self.quality_threshold = quality_threshold

    def evaluate(self, signals: ObservableSignals) -> ReliabilityDecision:
        if signals.quality_score >= self.quality_threshold:
            action = ReliabilityAction.ACCEPT
            reason = f"Visual quality score >= {self.quality_threshold}"
        else:
            action = ReliabilityAction.ABSTAIN
            reason = f"Visual quality degraded < {self.quality_threshold}"

        return ReliabilityDecision(
            action=action,
            confidence=signals.raw_confidence,
            uncertainty_norm=1.0 - signals.quality_score,
            operating_point="quality_gate",
            reason=reason,
        )


class BaselineB9_4_EvidenceGate:
    """B9-4: Abstains based solely on Phase 6 retrieval confidence."""

    def __init__(self, retrieval_threshold: float = 0.70):
        self.retrieval_threshold = retrieval_threshold

    def evaluate(self, signals: ObservableSignals) -> ReliabilityDecision:
        if signals.retrieval_score >= self.retrieval_threshold:
            action = ReliabilityAction.ACCEPT
            reason = f"Retrieval confidence >= {self.retrieval_threshold}"
        else:
            action = ReliabilityAction.ABSTAIN
            reason = f"Retrieval confidence < {self.retrieval_threshold}"

        return ReliabilityDecision(
            action=action,
            confidence=signals.raw_confidence,
            uncertainty_norm=1.0 - signals.retrieval_score,
            operating_point="retrieval_gate",
            reason=reason,
        )


class BaselineB9_5_Proposed:
    """B9-5 Proposed: Full 8D uncertainty vector + calibrated confidence multi-level decision."""

    def __init__(
        self,
        confidence_model: Optional[CalibratedCompositeModel] = None,
        policy: Optional[AbstentionPolicy] = None,
    ):
        self.confidence_model = confidence_model or CalibratedCompositeModel()
        self.policy = policy or AbstentionPolicy()

    def evaluate(self, signals: ObservableSignals) -> ReliabilityDecision:
        vec = UncertaintyCalculator.compute_uncertainty_vector(signals)
        calibrated_conf = self.confidence_model.compute(vec)
        return self.policy.evaluate(
            confidence=calibrated_conf,
            uncertainty_norm=vec.l2_norm,
        )
