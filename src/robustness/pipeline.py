"""src/robustness/pipeline.py
Phase 10 Evaluation Pipeline & Baselines Runner.
Consumes observable outputs and executes B10-0 through B10-4.
"""

from typing import Dict, Any, List, Optional
from src.robustness.schema import DomainID
from src.reliability.pipeline import ReliabilityPipeline
from src.reliability.signals import ObservableSignals
from src.reliability.schema import ReliabilityAction, ReliabilityDecision
from src.reliability.baselines import (
    BaselineB9_0_NoAbstention,
    BaselineB9_1_GroundingGate,
    BaselineB9_4_EvidenceGate,
    BaselineB9_5_Proposed,
)


class RobustnessEvaluationPipeline:
    """Executes baseline evaluations across shifted domains."""

    def __init__(self):
        self.proposed_pipeline = ReliabilityPipeline()
        self.b10_0 = BaselineB9_0_NoAbstention()
        self.b10_1 = BaselineB9_4_EvidenceGate(retrieval_threshold=0.70)
        self.b10_2 = BaselineB9_1_GroundingGate()
        self.b10_4 = BaselineB9_5_Proposed()

    def evaluate_sample(
        self,
        baseline_id: str,
        signals: ObservableSignals,
    ) -> ReliabilityDecision:
        if baseline_id == "B10-0":
            return self.b10_0.evaluate(signals)
        elif baseline_id == "B10-1":
            return self.b10_1.evaluate(signals)
        elif baseline_id == "B10-2":
            return self.b10_2.evaluate(signals)
        elif baseline_id == "B10-3":
            # Confidence-only threshold
            action = ReliabilityAction.ACCEPT if signals.raw_confidence >= 0.75 else ReliabilityAction.ABSTAIN
            return ReliabilityDecision(
                action=action,
                confidence=signals.raw_confidence,
                uncertainty_norm=1.0 - signals.raw_confidence,
                operating_point="confidence_only",
                reason="Gated by raw confidence",
            )
        elif baseline_id == "B10-4":
            return self.b10_4.evaluate(signals)
        else:
            raise ValueError(f"Unknown baseline ID: {baseline_id}")
