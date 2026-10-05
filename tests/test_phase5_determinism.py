"""
Tests for Phase 5 Routing Determinism.
Verifies identical routing decisions across identical inputs, configurations, and seeds.
"""

from src.routing.schema import RoutingPolicyType, UncertaintyVector
from src.routing.policy import RoutingPolicyManager


def test_routing_determinism_repeated_execution():
    manager = RoutingPolicyManager.from_configs()
    features = {"blur": 0.45, "noise": 0.12, "skew": 0.05}
    u_vec = UncertaintyVector(u_vlm=0.8, u_ocr=0.8, u_ret=0.8, u_gnd=0.8, u_qual=0.8, u_agr=0.8)

    # 10 identical invocations
    decisions = [
        manager.dispatch(
            policy=RoutingPolicyType.R2_RULE_BASED,
            run_id=f"run_det_{i}",
            document_id="doc_det",
            page_id="doc_det_p0",
            dataset="DocVQA",
            partition="test",
            seed=42,
            quality_features=features,
            uncertainty_vector=u_vec,
        )
        for i in range(10)
    ]

    first_model = decisions[0].selected_model
    first_reason = decisions[0].decision_reason
    first_conf = decisions[0].routing_confidence

    for d in decisions:
        assert d.selected_model == first_model
        assert d.decision_reason == first_reason
        assert d.routing_confidence == first_conf
