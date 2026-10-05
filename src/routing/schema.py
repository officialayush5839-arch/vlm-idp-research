"""
Pydantic Schemas and Data Models for Phase 5 Adaptive Routing.
Enforces strict provenance, zero-leakage constraints, and formal typing.
"""

from __future__ import annotations

import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator


class RoutingPolicyType(str, Enum):
    """Permitted routing policies in Phase 5 benchmark."""
    R0_ORACLE = "R0_ORACLE"              # Non-deployable retrospective upper bound
    R1_FIXED_BEST = "R1_FIXED_BEST"      # Fixed single best baseline (B2)
    R2_RULE_BASED = "R2_RULE_BASED"      # Quality-aware deterministic rule engine
    R3_UNCERTAINTY = "R3_UNCERTAINTY"    # Multi-signal uncertainty-directed policy
    R4_LEARNED = "R4_LEARNED"            # Lightweight learned model router
    R5_COMPOSITE = "R5_COMPOSITE"        # Joint quality and calibrated uncertainty policy


class UncertaintyVector(BaseModel):
    """
    6-signal composite uncertainty vector strictly conforming to protocol/uncertainty_protocol.md.
    u = [u_vlm, u_ocr, u_ret, u_gnd, u_qual, u_agr]
    All signals normalized into [0.0, 1.0] where 1.0 = maximum confidence / reliable evidence.
    """
    u_vlm: float = Field(ge=0.0, le=1.0, description="Normalized sequence token log-likelihood / consistency")
    u_ocr: float = Field(ge=0.0, le=1.0, description="Mean OCR word/character confidence in localized region")
    u_ret: float = Field(ge=0.0, le=1.0, description="Top-1 retrieval cosine similarity score")
    u_gnd: float = Field(ge=0.0, le=1.0, description="Fuzzy normalized alignment score within predicted bounding box")
    u_qual: float = Field(ge=0.0, le=1.0, description="Visual quality score Q in [0, 1]")
    u_agr: float = Field(ge=0.0, le=1.0, description="Cosine similarity between OCR text and VLM answer embedding")

    def to_list(self) -> List[float]:
        return [self.u_vlm, self.u_ocr, self.u_ret, self.u_gnd, self.u_qual, self.u_agr]


class RoutingDecision(BaseModel):
    """
    Standardized inference-time decision emitted by any routing policy before model execution.
    Contains no evaluation scores or ground-truth leakage.
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)

    run_id: str
    document_id: str
    page_id: str
    dataset: str
    partition: str = "test"
    seed: int = 42
    routing_policy: RoutingPolicyType
    router_version: str = "1.0.0"
    candidate_models: List[str] = Field(default_factory=lambda: ["B0", "B1", "B2", "B0-U"])
    selected_model: str
    routing_confidence: float = Field(ge=0.0, le=1.0)
    decision_reason: str
    fallback_triggered: bool = False
    fallback_model: Optional[str] = None
    quality_features: Dict[str, float] = Field(default_factory=dict)
    uncertainty_vector: Optional[UncertaintyVector] = None
    latency_ms: float = 0.0
    timestamp_utc: str = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())


class RoutingTrace(BaseModel):
    """
    Immutable audit trace capturing the internal state and reasoning for a routing decision.
    """
    trace_id: str
    run_id: str
    document_id: str
    candidate_models: List[str]
    selected_model: str
    decision_reason: str
    policy_version: str = "1.0.0"
    router_confidence: float
    fallback_triggered: bool = False
    timestamp_utc: str = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())


class RoutingCost(BaseModel):
    """
    Accounting of computational and latency expenditure for a routed execution.
    """
    latency_ms: float = 0.0
    compute_cost: float = 0.0
    model_invocations: int = 1
    fallback_invocations: int = 0

    def total_engineering_cost(self, lambda_latency: float = 0.001, lambda_compute: float = 1.0) -> float:
        """J_cost = lambda_compute * compute_cost + lambda_latency * latency_ms"""
        return (lambda_compute * self.compute_cost) + (lambda_latency * self.latency_ms)


class RoutingRunArtifact(BaseModel):
    """
    Complete benchmark run artifact recording routing, model execution, evaluation, and regret.
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)

    run_id: str
    document_id: str
    dataset: str
    partition: str
    seed: int
    policy: RoutingPolicyType
    selected_model: str
    final_answer: str
    metrics: Dict[str, float] = Field(default_factory=dict)
    regret: Optional[float] = None
    oracle_best_model: Optional[str] = None
    cost: Optional[RoutingCost] = None
    status: str = "SUCCESS"
    error_message: Optional[str] = None
    timestamp_utc: str = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
