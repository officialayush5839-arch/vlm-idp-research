"""
Uncertainty and Abstention Baseline Registry for Phase 8.
Defines baselines A0 through A5:
A0: No Abstention (Full Coverage, Raw Confidence)
A1: Random Abstention
A2: Uncalibrated Heuristic Abstention
A3: Temperature Scaling Abstention
A4: Isotonic Regression Abstention
A5: Evidence-Aware Calibrated Abstention (Proposed Primary)
"""

from typing import Dict, Any, List, Optional, Type
import random
from src.uncertainty.schema import UncertaintyFeatures, AbstentionDecision, UncertaintyPackage
from src.uncertainty.calibration import CalibrationManager
from src.uncertainty.abstention import AbstentionPolicy


class BaseBaseline:
    name: str = "base"

    def evaluate_single(
        self,
        confidence: float,
        features: UncertaintyFeatures,
        target_coverage: float = 1.0,
        threshold: Optional[float] = None
    ) -> Any:
        raise NotImplementedError


class BaselineResult:
    def __init__(self, raw_confidence: float, calibrated_confidence: float, decision: AbstentionDecision):
        self.raw_confidence = raw_confidence
        self.calibrated_confidence = calibrated_confidence
        self.decision = decision


class A0NoAbstentionBaseline(BaseBaseline):
    """A0: No Abstention. Always answers with raw confidence."""
    name = "A0_no_abstention"

    def evaluate_single(
        self,
        confidence: float,
        features: UncertaintyFeatures,
        target_coverage: float = 1.0,
        threshold: Optional[float] = None
    ) -> BaselineResult:
        decision = AbstentionDecision(
            decision="ANSWER",
            calibrated_confidence=round(float(confidence), 6),
            threshold=0.0,
            target_coverage=round(float(target_coverage), 4),
            margin=round(float(confidence), 6),
            abstention_reason=""
        )
        return BaselineResult(confidence, confidence, decision)


class A1RandomAbstentionBaseline(BaseBaseline):
    """A1: Random Abstention. Decides to answer with probability target_coverage."""
    name = "A1_random_abstention"

    def __init__(self, seed: int = 42):
        self.rng = random.Random(seed)

    def evaluate_single(
        self,
        confidence: float,
        features: UncertaintyFeatures,
        target_coverage: float = 1.0,
        threshold: Optional[float] = None
    ) -> BaselineResult:
        rand_val = self.rng.random()
        is_answer = rand_val < target_coverage
        decision_str = "ANSWER" if is_answer else "ABSTAIN"
        reason = "" if is_answer else "RANDOM_ABSTENTION"

        decision = AbstentionDecision(
            decision=decision_str,
            calibrated_confidence=round(float(confidence), 6),
            threshold=round(float(1.0 - target_coverage), 4),
            target_coverage=round(float(target_coverage), 4),
            margin=round(float(target_coverage - rand_val), 6),
            abstention_reason=reason
        )
        return BaselineResult(confidence, confidence, decision)


class A2UncalibratedBaseline(BaseBaseline):
    """A2: Uncalibrated confidence with threshold selection on validation data."""
    name = "A2_uncalibrated_heuristic"

    def __init__(self, threshold: float = 0.5):
        self.policy = AbstentionPolicy(default_threshold=threshold)

    def evaluate_single(
        self,
        confidence: float,
        features: UncertaintyFeatures,
        target_coverage: float = 1.0,
        threshold: Optional[float] = None
    ) -> BaselineResult:
        dec = self.policy.decide(
            confidence=confidence,
            features=features,
            threshold=threshold,
            target_coverage=target_coverage
        )
        return BaselineResult(confidence, confidence, dec)


class A3TemperatureScalingBaseline(BaseBaseline):
    """A3: Temperature scaling post-hoc calibration."""
    name = "A3_temperature_scaling"

    def __init__(self, cal_manager: Optional[CalibrationManager] = None):
        self.cal_manager = cal_manager or CalibrationManager(method="temperature_scaling")
        self.policy = AbstentionPolicy()

    def evaluate_single(
        self,
        confidence: float,
        features: UncertaintyFeatures,
        target_coverage: float = 1.0,
        threshold: Optional[float] = None
    ) -> BaselineResult:
        cal_conf = self.cal_manager.predict(confidence)
        dec = self.policy.decide(
            confidence=cal_conf,
            features=features,
            threshold=threshold,
            target_coverage=target_coverage
        )
        return BaselineResult(confidence, cal_conf, dec)


class A4IsotonicBaseline(BaseBaseline):
    """A4: Isotonic regression post-hoc calibration."""
    name = "A4_isotonic_regression"

    def __init__(self, cal_manager: Optional[CalibrationManager] = None):
        self.cal_manager = cal_manager or CalibrationManager(method="isotonic_regression")
        self.policy = AbstentionPolicy()

    def evaluate_single(
        self,
        confidence: float,
        features: UncertaintyFeatures,
        target_coverage: float = 1.0,
        threshold: Optional[float] = None
    ) -> BaselineResult:
        cal_conf = self.cal_manager.predict(confidence)
        dec = self.policy.decide(
            confidence=cal_conf,
            features=features,
            threshold=threshold,
            target_coverage=target_coverage
        )
        return BaselineResult(confidence, cal_conf, dec)


class A5EvidenceAwareBaseline(BaseBaseline):
    """A5: Evidence-aware multi-signal calibrated confidence and abstention."""
    name = "A5_evidence_aware"

    def __init__(self, cal_manager: Optional[CalibrationManager] = None):
        self.cal_manager = cal_manager or CalibrationManager(method="isotonic_regression")
        self.policy = AbstentionPolicy()

    def evaluate_single(
        self,
        confidence: float,
        features: UncertaintyFeatures,
        target_coverage: float = 1.0,
        threshold: Optional[float] = None
    ) -> BaselineResult:
        # Use composite confidence derived from evidence signals
        raw_conf = features.composite_raw_confidence
        cal_conf = self.cal_manager.predict(raw_conf)
        dec = self.policy.decide(
            confidence=cal_conf,
            features=features,
            threshold=threshold,
            target_coverage=target_coverage
        )
        return BaselineResult(raw_conf, cal_conf, dec)


class BaselineRegistry:
    """Registry for all Phase 8 uncertainty baselines."""
    _REGISTRY: Dict[str, Type[BaseBaseline]] = {
        "A0_no_abstention": A0NoAbstentionBaseline,
        "A1_random_abstention": A1RandomAbstentionBaseline,
        "A2_uncalibrated_heuristic": A2UncalibratedBaseline,
        "A3_temperature_scaling": A3TemperatureScalingBaseline,
        "A4_isotonic_regression": A4IsotonicBaseline,
        "A5_evidence_aware": A5EvidenceAwareBaseline,
    }

    @classmethod
    def get(cls, name: str) -> Type[BaseBaseline]:
        if name not in cls._REGISTRY:
            raise KeyError(f"Baseline {name} not found in registry. Available: {list(cls._REGISTRY.keys())}")
        return cls._REGISTRY[name]

    @classmethod
    def list_baselines(cls) -> List[str]:
        return list(cls._REGISTRY.keys())
