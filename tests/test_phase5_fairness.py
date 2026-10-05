"""
Tests for Phase 5 Model Fairness.
Verifies that the router selects among frozen candidate systems without altering the input document.
"""

from src.routing.schema import RoutingPolicyType
from src.routing.policy import RoutingPolicyManager


def test_routing_candidate_set_confinement():
    manager = RoutingPolicyManager.from_configs()
    features = {"skew": 0.8, "blur": 0.8}
    allowed_candidates = {"B0", "B1", "B2", "B0-U"}

    for policy in [
        RoutingPolicyType.R1_FIXED_BEST,
        RoutingPolicyType.R2_RULE_BASED,
        RoutingPolicyType.R3_UNCERTAINTY,
        RoutingPolicyType.R5_COMPOSITE,
    ]:
        decision = manager.dispatch(
            policy=policy,
            run_id=f"run_fairness_{policy.value}",
            document_id="doc_fairness",
            page_id="doc_fairness_p0",
            dataset="DocVQA",
            partition="test",
            quality_features=features,
        )
        assert decision.selected_model in allowed_candidates
        assert set(decision.candidate_models) == allowed_candidates
