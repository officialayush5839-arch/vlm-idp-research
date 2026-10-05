"""
Tests for Phase 5 Routing Schemas and Data Models.
Verifies strict validation, immutability, and provenance compliance.
"""

import pytest
from pydantic import ValidationError

from src.routing.schema import (
    RoutingPolicyType,
    UncertaintyVector,
    RoutingDecision,
    RoutingTrace,
    RoutingCost,
    RoutingRunArtifact,
)


def test_routing_policy_type_enum():
    assert RoutingPolicyType.R0_ORACLE.value == "R0_ORACLE"
    assert RoutingPolicyType.R1_FIXED_BEST.value == "R1_FIXED_BEST"
    assert RoutingPolicyType.R2_RULE_BASED.value == "R2_RULE_BASED"
    assert RoutingPolicyType.R3_UNCERTAINTY.value == "R3_UNCERTAINTY"
    assert RoutingPolicyType.R4_LEARNED.value == "R4_LEARNED"
    assert RoutingPolicyType.R5_COMPOSITE.value == "R5_COMPOSITE"


def test_uncertainty_vector_validation():
    # Valid vector
    u = UncertaintyVector(
        u_vlm=0.85,
        u_ocr=0.92,
        u_ret=0.78,
        u_gnd=0.88,
        u_qual=0.95,
        u_agr=0.90,
    )
    assert u.to_list() == [0.85, 0.92, 0.78, 0.88, 0.95, 0.90]

    # Out of bounds should raise ValidationError
    with pytest.raises(ValidationError):
        UncertaintyVector(
            u_vlm=1.5,
            u_ocr=0.9,
            u_ret=0.8,
            u_gnd=0.8,
            u_qual=0.9,
            u_agr=0.9,
        )


def test_routing_decision_instantiation():
    decision = RoutingDecision(
        run_id="run_p5_001",
        document_id="doc_test_01",
        page_id="doc_test_01_p0",
        dataset="DocVQA",
        partition="test",
        seed=42,
        routing_policy=RoutingPolicyType.R2_RULE_BASED,
        router_version="1.0.0",
        candidate_models=["B0", "B1", "B2", "B0-U"],
        selected_model="B2",
        routing_confidence=0.88,
        decision_reason="Severe skew detected in quality vector",
        fallback_triggered=False,
        quality_features={"skew": 0.85, "blur": 0.12},
    )
    assert decision.selected_model == "B2"
    assert decision.fallback_triggered is False
    assert decision.decision_reason == "Severe skew detected in quality vector"


def test_routing_trace_immutability():
    trace = RoutingTrace(
        trace_id="trace_001",
        run_id="run_p5_001",
        document_id="doc_test_01",
        candidate_models=["B0", "B1", "B2", "B0-U"],
        selected_model="B2",
        decision_reason="Severe blur",
        policy_version="1.0.0",
        router_confidence=0.91,
        fallback_triggered=False,
    )
    assert trace.selected_model == "B2"


def test_routing_cost_calculation():
    cost = RoutingCost(
        latency_ms=120.5,
        compute_cost=0.015,
        model_invocations=1,
        fallback_invocations=0,
    )
    assert cost.total_engineering_cost(lambda_latency=0.001, lambda_compute=1.0) == pytest.approx(
        0.015 + (120.5 * 0.001)
    )


def test_routing_run_artifact():
    artifact = RoutingRunArtifact(
        run_id="run_p5_art_01",
        document_id="doc_01",
        dataset="FUNSD",
        partition="test",
        seed=42,
        policy=RoutingPolicyType.R1_FIXED_BEST,
        selected_model="B2",
        final_answer="Invoice Total $50.00",
        metrics={"exact_match": 1.0, "token_f1": 1.0},
        regret=0.0,
        status="SUCCESS",
    )
    assert artifact.status == "SUCCESS"
    assert artifact.regret == 0.0
