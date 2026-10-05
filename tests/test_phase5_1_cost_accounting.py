"""
Tests for Phase 5.1 Relative Architectural Compute Cost Model.
Verifies standardized compute units, fallback invocation accounting,
and latency measurement across candidate models.
"""

from pathlib import Path
from src.routing.cost import RoutingCostModel


def test_relative_compute_cost_model_values():
    """Verify Relative Architectural Compute Cost values adhere to project specifications."""
    repo_root = Path(__file__).resolve().parents[1]
    cost_cfg = str(repo_root / "configs" / "phase5_1" / "cost_config.yaml")
    cost_model = RoutingCostModel.from_config(cost_cfg)

    # Relative unit values
    assert cost_model.get_model_compute_weight("B0") == 0.10
    assert cost_model.get_model_compute_weight("B0-U") == 0.50
    assert cost_model.get_model_compute_weight("B1") == 0.80
    assert cost_model.get_model_compute_weight("B2") == 1.00

    # Single model execution cost
    cost_b0 = cost_model.evaluate_cost("B0", primary_latency_ms=50.0)
    assert cost_b0.compute_cost == 0.10
    assert cost_b0.latency_ms == 50.0
    assert cost_b0.model_invocations == 1
    assert cost_b0.fallback_invocations == 0

    # Fallback execution cost (additive compute and latency)
    cost_fb = cost_model.evaluate_cost(
        primary_model="B0",
        primary_latency_ms=50.0,
        fallback_model="B2",
        fallback_latency_ms=200.0,
    )
    assert abs(cost_fb.compute_cost - (0.10 + 1.00)) < 1e-6  # B0 + B2
    assert cost_fb.latency_ms == 250.0
    assert cost_fb.model_invocations == 2
    assert cost_fb.fallback_invocations == 1
