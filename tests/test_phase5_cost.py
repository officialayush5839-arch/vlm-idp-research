"""
Tests for Phase 5 Routing Engineering Cost Model.
Verifies honest compute tracking, latency accounting, and objective function calculation.
"""

import pytest
from src.routing.cost import RoutingCostModel


def test_cost_model_relative_compute_lookup():
    cost_model = RoutingCostModel.from_config()
    assert cost_model.get_model_compute_weight("B0") == pytest.approx(0.10)
    assert cost_model.get_model_compute_weight("B0-U") == pytest.approx(0.50)
    assert cost_model.get_model_compute_weight("B1") == pytest.approx(0.80)
    assert cost_model.get_model_compute_weight("B2") == pytest.approx(1.00)


def test_cost_model_computation_single_model():
    cost_model = RoutingCostModel.from_config()
    cost = cost_model.evaluate_cost(
        primary_model="B0",
        primary_latency_ms=25.0,
        fallback_model=None,
        fallback_latency_ms=0.0,
    )
    assert cost.model_invocations == 1
    assert cost.fallback_invocations == 0
    assert cost.latency_ms == pytest.approx(25.0)
    assert cost.compute_cost == pytest.approx(0.10)
    # Total engineering cost: lambda_compute * compute + lambda_latency * latency
    # J = 1.0 * 0.10 + 0.001 * 25.0 = 0.125
    total = cost.total_engineering_cost(
        lambda_latency=cost_model.lambda_latency,
        lambda_compute=cost_model.lambda_compute,
    )
    assert total == pytest.approx(0.125)


def test_cost_model_computation_with_fallback():
    cost_model = RoutingCostModel.from_config()
    cost = cost_model.evaluate_cost(
        primary_model="B0",
        primary_latency_ms=30.0,
        fallback_model="B2",
        fallback_latency_ms=200.0,
    )
    assert cost.model_invocations == 2
    assert cost.fallback_invocations == 1
    assert cost.latency_ms == pytest.approx(230.0)
    # B0 (0.10) + B2 (1.00) = 1.10
    assert cost.compute_cost == pytest.approx(1.10)
