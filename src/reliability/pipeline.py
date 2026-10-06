"""src/reliability/pipeline.py
Master ReliabilityPipeline orchestrator for Phase 9.
"""

from typing import Dict, Any, Optional
from src.reliability.schema import ReliabilityPackage, ReliabilityDecision, UncertaintyVector
from src.reliability.signals import ObservableSignals, SignalExtractor
from src.reliability.uncertainty import UncertaintyCalculator
from src.reliability.confidence import CalibratedCompositeModel
from src.reliability.abstention import AbstentionPolicy
from src.reliability.failure_modes import FailureModeClassifier


class ReliabilityPipeline:
    """End-to-end reliability assessment and selective decision engine."""

    def __init__(
        self,
        confidence_model: Optional[CalibratedCompositeModel] = None,
        abstention_policy: Optional[AbstentionPolicy] = None,
        failure_classifier: Optional[FailureModeClassifier] = None,
    ):
        self.confidence_model = confidence_model or CalibratedCompositeModel()
        self.abstention_policy = abstention_policy or AbstentionPolicy()
        self.failure_classifier = failure_classifier or FailureModeClassifier()

    def process(
        self,
        doc_id: str,
        query_id: str,
        phase3_output: Optional[Dict[str, Any]] = None,
        phase6_output: Optional[Dict[str, Any]] = None,
        phase7_output: Optional[Dict[str, Any]] = None,
        phase8_output: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> ReliabilityPackage:
        # Step 1: Extract observable signals without leakage
        signals = SignalExtractor.extract(
            phase3_output=phase3_output,
            phase6_output=phase6_output,
            phase7_output=phase7_output,
            phase8_output=phase8_output,
        )

        # Step 2: Compute 8D Uncertainty Vector
        vec = UncertaintyCalculator.compute_uncertainty_vector(signals)

        # Step 3: Compute Calibrated Confidence
        calibrated_conf = self.confidence_model.compute(vec)

        # Step 4: Evaluate Abstention Policy
        decision = self.abstention_policy.evaluate(
            confidence=calibrated_conf,
            uncertainty_norm=vec.l2_norm,
        )

        # Step 5: Diagnose Failure Modes
        failure_mode = self.failure_classifier.diagnose(
            uncertainty_vector=vec,
            confidence=calibrated_conf,
            context_metadata=metadata,
        )

        return ReliabilityPackage(
            doc_id=doc_id,
            query_id=query_id,
            decision=decision,
            uncertainty_vector=vec,
            raw_confidence=signals.raw_confidence,
            calibrated_confidence=calibrated_conf,
            failure_mode=failure_mode,
            metadata=metadata,
        )
