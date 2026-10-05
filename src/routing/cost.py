"""
Engineering Cost Model for Phase 5 Adaptive Routing.
Computes latency and relative compute expenditure across primary and fallback model executions.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional
import yaml

from src.routing.schema import RoutingCost


class RoutingCostModel:
    """
    Computes computational expenditure metrics based on model identity and execution latency.
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.lambda_latency = config.get("objective_function", {}).get("lambda_latency", 0.001)
        self.lambda_compute = config.get("objective_function", {}).get("lambda_compute", 1.0)
        self.compute_weights = config.get("relative_model_compute_weights", {
            "B0": 0.10,
            "B0-U": 0.50,
            "B1": 0.80,
            "B2": 1.00,
        })

    @classmethod
    def from_config(cls, config_path: Optional[str] = None) -> RoutingCostModel:
        if config_path is None:
            config_path = str(Path(__file__).parents[2] / "configs" / "phase5" / "cost_config.yaml")
        with open(config_path, "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f)
        return cls(cfg)

    def get_model_compute_weight(self, model_id: str) -> float:
        """
        Returns normalized relative compute cost for a model architecture.
        """
        return float(self.compute_weights.get(model_id, 1.0))

    def evaluate_cost(
        self,
        primary_model: str,
        primary_latency_ms: float,
        fallback_model: Optional[str] = None,
        fallback_latency_ms: float = 0.0,
    ) -> RoutingCost:
        """
        Constructs a complete RoutingCost record for an execution.
        """
        primary_w = self.get_model_compute_weight(primary_model)
        total_latency = float(primary_latency_ms)
        total_compute = primary_w
        invocations = 1
        fallback_invocations = 0

        if fallback_model is not None:
            fallback_w = self.get_model_compute_weight(fallback_model)
            total_compute += fallback_w
            total_latency += float(fallback_latency_ms)
            invocations += 1
            fallback_invocations += 1

        return RoutingCost(
            latency_ms=total_latency,
            compute_cost=total_compute,
            model_invocations=invocations,
            fallback_invocations=fallback_invocations,
        )
