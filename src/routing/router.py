"""
Adaptive Router Orchestrator for Phase 5.
Combines feature adaptation, policy dispatch, fallback management, and audit tracing.
"""

from __future__ import annotations

import time
from typing import Any, Dict, Optional, Tuple

from src.quality.schema import PageQualityAssessment
from src.routing.schema import (
    RoutingPolicyType,
    RoutingDecision,
    RoutingTrace,
    UncertaintyVector,
)
from src.routing.feature_adapter import QualityFeatureAdapter
from src.routing.policy import RoutingPolicyManager
from src.routing.fallback import StructuralFallbackHandler
from src.routing.cost import RoutingCostModel
from src.routing.decision_trace import RoutingDecisionTracer


class AdaptiveRouter:
    """
    Central router interface orchestrating feature extraction, decision dispatch, and audit logging.
    """

    def __init__(
        self,
        feature_adapter: QualityFeatureAdapter,
        policy_manager: RoutingPolicyManager,
        fallback_handler: StructuralFallbackHandler,
        cost_model: RoutingCostModel,
        decision_tracer: RoutingDecisionTracer,
    ):
        self.feature_adapter = feature_adapter
        self.policy_manager = policy_manager
        self.fallback_handler = fallback_handler
        self.cost_model = cost_model
        self.decision_tracer = decision_tracer

    @classmethod
    def create_default(cls) -> AdaptiveRouter:
        feature_adapter = QualityFeatureAdapter()
        policy_manager = RoutingPolicyManager.from_configs()
        fallback_handler = StructuralFallbackHandler(fallback_target="B2", enabled=True)
        cost_model = RoutingCostModel.from_config()
        decision_tracer = RoutingDecisionTracer()
        return cls(
            feature_adapter=feature_adapter,
            policy_manager=policy_manager,
            fallback_handler=fallback_handler,
            cost_model=cost_model,
            decision_tracer=decision_tracer,
        )

    def route(
        self,
        run_id: str,
        document_id: str,
        page_id: str,
        dataset: str,
        quality_assessment: PageQualityAssessment,
        policy: RoutingPolicyType,
        partition: str = "test",
        seed: int = 42,
        uncertainty_vector: Optional[UncertaintyVector] = None,
        oracle_candidate_scores: Optional[Dict[str, float]] = None,
    ) -> Tuple[RoutingDecision, RoutingTrace]:
        """
        Executes routing decision and logs trace.
        """
        start_t = time.perf_counter()
        quality_features = self.feature_adapter.extract_features(quality_assessment)

        decision = self.policy_manager.dispatch(
            policy=policy,
            run_id=run_id,
            document_id=document_id,
            page_id=page_id,
            dataset=dataset,
            partition=partition,
            seed=seed,
            quality_features=quality_features,
            uncertainty_vector=uncertainty_vector,
            oracle_candidate_scores=oracle_candidate_scores,
        )
        latency_ms = (time.perf_counter() - start_t) * 1000.0
        decision.latency_ms = latency_ms

        trace = self.decision_tracer.record_trace(decision)
        return decision, trace
