"""
Routing Policy Manager for Phase 5.
Coordinates execution across R0 (Oracle), R1 (Fixed Best), R2 (Rule-Based),
R3 (Uncertainty-Directed), R4 (Learned), and R5 (Composite Quality+Uncertainty).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional
import yaml

from src.routing.schema import (
    RoutingPolicyType,
    RoutingDecision,
    UncertaintyVector,
)
from src.routing.rule_engine import RuleBasedQualityRouter
from src.routing.uncertainty import UncertaintyAdapter
from src.routing.learned_router import LearnedQualityRouter


class RoutingPolicyManager:
    """
    Central dispatch interface executing configured routing policies.
    """

    def __init__(
        self,
        config: Dict[str, Any],
        rule_router: RuleBasedQualityRouter,
        uncertainty_adapter: UncertaintyAdapter,
        learned_router: Optional[LearnedQualityRouter] = None,
    ):
        self.config = config
        self.default_model = config.get("default_fixed_baseline", "B2")
        self.candidate_models = [m["id"] for m in config.get("candidate_models", [])]
        self.rule_router = rule_router
        self.uncertainty_adapter = uncertainty_adapter
        self.learned_router = learned_router or LearnedQualityRouter()
        self.router_version = config.get("version", "1.0.0")

    @classmethod
    def from_configs(
        cls,
        routing_cfg_path: Optional[str] = None,
        rules_cfg_path: Optional[str] = None,
        uncertainty_cfg_path: Optional[str] = None,
        learned_router_model_path: Optional[str] = None,
    ) -> RoutingPolicyManager:
        base_dir = Path(__file__).parents[2] / "configs" / "phase5"
        routing_cfg_path = routing_cfg_path or str(base_dir / "routing_config.yaml")
        rules_cfg_path = rules_cfg_path or str(base_dir / "router_rules.yaml")
        uncertainty_cfg_path = uncertainty_cfg_path or str(base_dir / "uncertainty_config.yaml")

        with open(routing_cfg_path, "r", encoding="utf-8") as f:
            r_cfg = yaml.safe_load(f)

        rule_router = RuleBasedQualityRouter.from_config(rules_cfg_path)
        uncertainty_adapter = UncertaintyAdapter.from_config(uncertainty_cfg_path)

        model_path = learned_router_model_path or r_cfg.get("learned_router_model_path")
        learned_router = None
        if model_path:
            p = Path(model_path)
            if not p.is_absolute():
                p = Path(__file__).parents[2] / p
            if p.exists():
                learned_router = LearnedQualityRouter.from_file(p)

        return cls(r_cfg, rule_router, uncertainty_adapter, learned_router=learned_router)

    def dispatch(
        self,
        policy: RoutingPolicyType,
        run_id: str,
        document_id: str,
        page_id: str,
        dataset: str,
        partition: str = "test",
        seed: int = 42,
        quality_features: Optional[Dict[str, float]] = None,
        uncertainty_vector: Optional[UncertaintyVector] = None,
        oracle_candidate_scores: Optional[Dict[str, float]] = None,
    ) -> RoutingDecision:
        """
        Executes policy logic and returns a standardized, validated RoutingDecision.
        """
        quality_features = quality_features or {}

        if policy == RoutingPolicyType.R0_ORACLE:
            if not oracle_candidate_scores:
                raise ValueError("Oracle policy requires retrospective candidate scores and cannot run blind at inference time.")
            # Select model with strictly highest score retrospectively
            selected = max(oracle_candidate_scores.keys(), key=lambda m: oracle_candidate_scores[m])
            reason = f"Oracle retrospective selection based on actual performance (max_score={oracle_candidate_scores[selected]:.4f})."
            conf = 1.0

        elif policy == RoutingPolicyType.R1_FIXED_BEST:
            selected = self.default_model
            reason = f"Fixed single-best baseline policy always routing to {self.default_model}."
            conf = 1.0

        elif policy == RoutingPolicyType.R2_RULE_BASED:
            selected, reason, conf = self.rule_router.route(quality_features)

        elif policy == RoutingPolicyType.R3_UNCERTAINTY:
            if uncertainty_vector is None:
                selected = self.default_model
                reason = "No uncertainty vector provided; defaulting to robust fixed baseline B2."
                conf = 0.50
            else:
                conf = self.uncertainty_adapter.compute_weighted_confidence(uncertainty_vector)
                if conf >= self.uncertainty_adapter.tau_accept:
                    selected = "B0"
                    reason = f"High pipeline confidence (c={conf:.2f} >= tau_accept); routing to efficient OCR B0."
                elif conf >= self.uncertainty_adapter.tau_review:
                    selected = "B1"
                    reason = f"Moderate pipeline confidence (c={conf:.2f}); routing to hybrid OCR+VLM B1."
                else:
                    selected = "B2"
                    reason = f"High pipeline uncertainty (c={conf:.2f} < tau_review); routing to native robust VLM B2."

        elif policy == RoutingPolicyType.R4_LEARNED:
            feature_vector = [quality_features.get(k, 0.0) for k in [
                "blur", "noise", "skew", "glare", "contrast",
                "resolution", "compression", "illumination", "occlusion", "perspective"
            ]]
            selected, reason, conf = self.learned_router.predict(feature_vector)

        elif policy == RoutingPolicyType.R5_COMPOSITE:
            rule_selected, rule_reason, rule_conf = self.rule_router.route(quality_features)
            if uncertainty_vector is not None:
                u_conf = self.uncertainty_adapter.compute_weighted_confidence(uncertainty_vector)
                if u_conf < self.uncertainty_adapter.tau_review and rule_selected != "B2":
                    selected = "B2"
                    reason = (
                        f"Rule proposed {rule_selected}, but high pipeline uncertainty (c={u_conf:.2f}) "
                        f"triggered escalation to robust native VLM B2."
                    )
                    conf = 0.85
                else:
                    selected = rule_selected
                    reason = f"Composite policy adopted rule proposal: {rule_reason}"
                    conf = (rule_conf + u_conf) / 2.0
            else:
                selected = rule_selected
                reason = f"Composite policy fell back to rule decision: {rule_reason}"
                conf = rule_conf

        else:
            raise ValueError(f"Unknown routing policy: {policy}")

        return RoutingDecision(
            run_id=run_id,
            document_id=document_id,
            page_id=page_id,
            dataset=dataset,
            partition=partition,
            seed=seed,
            routing_policy=policy,
            router_version=self.router_version,
            candidate_models=self.candidate_models,
            selected_model=selected,
            routing_confidence=conf,
            decision_reason=reason,
            fallback_triggered=False,
            quality_features=quality_features,
            uncertainty_vector=uncertainty_vector,
        )
