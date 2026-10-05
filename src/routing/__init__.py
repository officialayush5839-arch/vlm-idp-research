"""
Phase 5 Routing Package: Adaptive Quality-Aware and Uncertainty-Aware Model Routing.
"""

from src.routing.schema import (
    RoutingPolicyType,
    UncertaintyVector,
    RoutingDecision,
    RoutingTrace,
    RoutingCost,
    RoutingRunArtifact,
)
from src.routing.feature_adapter import QualityFeatureAdapter
from src.routing.rule_engine import RuleBasedQualityRouter
from src.routing.uncertainty import UncertaintyAdapter
from src.routing.calibration import PostHocCalibrator
from src.routing.learned_router import LearnedQualityRouter
from src.routing.policy import RoutingPolicyManager
from src.routing.fallback import StructuralFallbackHandler
from src.routing.cost import RoutingCostModel
from src.routing.decision_trace import RoutingDecisionTracer
from src.routing.audit import ZeroLeakageRouterAuditor
from src.routing.router import AdaptiveRouter
from src.routing.pipeline import AdaptiveRoutingPipeline

__all__ = [
    "RoutingPolicyType",
    "UncertaintyVector",
    "RoutingDecision",
    "RoutingTrace",
    "RoutingCost",
    "RoutingRunArtifact",
    "QualityFeatureAdapter",
    "RuleBasedQualityRouter",
    "UncertaintyAdapter",
    "PostHocCalibrator",
    "LearnedQualityRouter",
    "RoutingPolicyManager",
    "StructuralFallbackHandler",
    "RoutingCostModel",
    "RoutingDecisionTracer",
    "ZeroLeakageRouterAuditor",
    "AdaptiveRouter",
    "AdaptiveRoutingPipeline",
]
