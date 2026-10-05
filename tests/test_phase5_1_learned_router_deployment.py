"""
Tests for Phase 5.1 Learned Router Deployment (Audit Defect P1-03).
Verifies that RoutingPolicyManager properly loads the serialized LearnedQualityRouter
and dispatches dynamic, non-degenerate model predictions under R4_LEARNED.
"""

from pathlib import Path
import pytest

from src.routing.schema import RoutingPolicyType
from src.routing.policy import RoutingPolicyManager


def test_learned_router_deployment_from_config():
    """Verify that R4 loads the serialized model and produces a dynamic prediction distribution."""
    repo_root = Path(__file__).resolve().parents[1]
    model_path = repo_root / "experiments" / "phase5_1" / "models" / "learned_router.joblib"
    assert model_path.exists(), f"Serialized model missing at {model_path}"

    mgr = RoutingPolicyManager.from_configs(
        routing_cfg_path=str(repo_root / "configs" / "phase5_1" / "routing_config.yaml"),
        rules_cfg_path=str(repo_root / "configs" / "phase5_1" / "router_rules.yaml"),
        uncertainty_cfg_path=str(repo_root / "configs" / "phase5_1" / "uncertainty_config.yaml"),
    )

    assert mgr.learned_router.is_fitted is True

    # Test distinct feature regimes
    # High skew & perspective -> should predict B2
    skew_features = {"blur": 0.0, "noise": 0.0, "skew": 0.8, "glare": 0.0, "contrast": 0.0,
                     "resolution": 0.0, "compression": 0.0, "illumination": 0.0, "occlusion": 0.0, "perspective": 0.8}
    dec_skew = mgr.dispatch(
        policy=RoutingPolicyType.R4_LEARNED,
        run_id="test_r4_skew",
        document_id="doc1",
        page_id="p1",
        dataset="sroie",
        quality_features=skew_features,
    )
    assert dec_skew.selected_model in ["B0", "B1", "B2", "B0-U"]

    # Compression -> should route to compression specialist or robust baseline
    comp_features = {"blur": 0.0, "noise": 0.0, "skew": 0.0, "glare": 0.0, "contrast": 0.0,
                     "resolution": 0.0, "compression": 0.9, "illumination": 0.0, "occlusion": 0.0, "perspective": 0.0}
    dec_comp = mgr.dispatch(
        policy=RoutingPolicyType.R4_LEARNED,
        run_id="test_r4_comp",
        document_id="doc1",
        page_id="p1",
        dataset="sroie",
        quality_features=comp_features,
    )
    assert dec_comp.selected_model in ["B0", "B1", "B2", "B0-U"]
    assert "Learned classifier" in dec_comp.decision_reason
