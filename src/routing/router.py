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
    def create_default(
        cls,
        routing_cfg_path: Optional[str] = None,
        rules_cfg_path: Optional[str] = None,
        uncertainty_cfg_path: Optional[str] = None,
        cost_cfg_path: Optional[str] = None,
        trace_dir: Optional[str] = None,
    ) -> AdaptiveRouter:
        feature_adapter = QualityFeatureAdapter()
        policy_manager = RoutingPolicyManager.from_configs(
            routing_cfg_path=routing_cfg_path,
            rules_cfg_path=rules_cfg_path,
            uncertainty_cfg_path=uncertainty_cfg_path,
        )
        fallback_handler = StructuralFallbackHandler(fallback_target="B2", enabled=True)
        cost_model = RoutingCostModel.from_config(cost_cfg_path) if cost_cfg_path else RoutingCostModel.from_config()
        decision_tracer = RoutingDecisionTracer(trace_dir=trace_dir)
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
        phase: str = "phase5_1",
        sample_id: Optional[str] = None,
        degradation_family: Optional[str] = None,
        severity: Optional[int] = None,
        configuration_hash: Optional[str] = None,
        model_revision: Optional[str] = None,
        input_hash: Optional[str] = None,
        quality_feature_hash: Optional[str] = None,
        fallback_status: Optional[str] = None,
        compute_cost: Optional[float] = None,
    ) -> Tuple[RoutingDecision, RoutingTrace]:
        """
        Executes routing decision and logs trace with complete provenance.
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

        trace = self.decision_tracer.record_trace(
            decision=decision,
            phase=phase,
            sample_id=sample_id,
            degradation_family=degradation_family,
            severity=severity,
            seed=seed,
            policy=policy.value,
            configuration_hash=configuration_hash,
            model_revision=model_revision,
            input_hash=input_hash,
            quality_feature_hash=quality_feature_hash,
            fallback_status=fallback_status,
            latency_ms=latency_ms,
            compute_cost=compute_cost,
        )
        return decision, trace
