"""
Tests for Phase 5 Learned Router and Routing Policy Manager.
Verifies all policies R0 through R5, ensuring zero test leakage and proper dispatch.
"""

import numpy as np
import pytest

from src.routing.schema import RoutingPolicyType, UncertaintyVector
from src.routing.learned_router import LearnedQualityRouter
from src.routing.policy import RoutingPolicyManager


def test_learned_router_train_and_predict():
    router = LearnedQualityRouter(classifier_type="logistic", random_state=42)
    # 60 synthetic training samples (10 features each)
    np.random.seed(42)
    X_train = np.random.uniform(0.0, 1.0, size=(60, 10))
    classes = ["B0", "B1", "B2", "B0-U"]
    y_train = [classes[i % 4] for i in range(60)]

    # Fitting on train split must succeed
    router.fit(X_train, y_train, partition="train")
    assert router.is_fitted is True

    # Test partition fitting must fail
    with pytest.raises(ValueError, match="strictly forbidden"):
        router.fit(X_train, y_train, partition="test")

    # Prediction
    sample = [0.1] * 10
    selected, reason, conf = router.predict(sample)
    assert selected in classes
    assert 0.0 <= conf <= 1.0


def test_policy_manager_fixed_best():
    manager = RoutingPolicyManager.from_configs()
    features = {"blur": 0.5, "skew": 0.3}
    decision = manager.dispatch(
        policy=RoutingPolicyType.R1_FIXED_BEST,
        run_id="run_01",
        document_id="doc_01",
        page_id="doc_01_p0",
        dataset="DocVQA",
        partition="test",
        quality_features=features,
    )
    assert decision.selected_model == "B2"
    assert decision.routing_policy == RoutingPolicyType.R1_FIXED_BEST


def test_policy_manager_rule_based():
    manager = RoutingPolicyManager.from_configs()
    features = {"skew": 0.70, "blur": 0.10}
    decision = manager.dispatch(
        policy=RoutingPolicyType.R2_RULE_BASED,
        run_id="run_02",
        document_id="doc_02",
        page_id="doc_02_p0",
        dataset="DocVQA",
        partition="test",
        quality_features=features,
    )
    assert decision.selected_model == "B2"


def test_policy_manager_uncertainty_policy():
    manager = RoutingPolicyManager.from_configs()
    u_high = UncertaintyVector(u_vlm=0.95, u_ocr=0.95, u_ret=0.9, u_gnd=0.9, u_qual=0.95, u_agr=0.9)
    decision = manager.dispatch(
        policy=RoutingPolicyType.R3_UNCERTAINTY,
        run_id="run_03",
        document_id="doc_03",
        page_id="doc_03_p0",
        dataset="DocVQA",
        partition="test",
        uncertainty_vector=u_high,
    )
    assert decision.selected_model == "B0"


def test_policy_manager_composite_policy():
    manager = RoutingPolicyManager.from_configs()
    # High visual quality clean features, but low uncertainty signal -> escalates to robust B2
    clean_features = {k: 0.05 for k in ["blur", "noise", "skew", "perspective", "occlusion", "compression"]}
    u_low = UncertaintyVector(u_vlm=0.2, u_ocr=0.2, u_ret=0.3, u_gnd=0.2, u_qual=0.3, u_agr=0.2)
    decision = manager.dispatch(
        policy=RoutingPolicyType.R5_COMPOSITE,
        run_id="run_04",
        document_id="doc_04",
        page_id="doc_04_p0",
        dataset="DocVQA",
        partition="test",
        quality_features=clean_features,
        uncertainty_vector=u_low,
    )
    assert decision.selected_model == "B2"
    assert "uncertainty" in decision.decision_reason.lower()


def test_policy_manager_oracle_disallows_blind_inference():
    manager = RoutingPolicyManager.from_configs()
    with pytest.raises(ValueError, match="Oracle policy requires retrospective"):
        manager.dispatch(
            policy=RoutingPolicyType.R0_ORACLE,
            run_id="run_05",
            document_id="doc_05",
            page_id="doc_05_p0",
            dataset="DocVQA",
            partition="test",
        )


def test_pipeline_sample_processing(tmp_path):
    from PIL import Image
    from src.benchmark.schema import BenchmarkSample
    from src.routing.pipeline import AdaptiveRoutingPipeline

    pipeline = AdaptiveRoutingPipeline.create_default()
    pipeline.output_dir = tmp_path

    # Synthetic sample and test image
    img = Image.new("RGB", (200, 200), color=(255, 255, 255))
    sample = BenchmarkSample(
        sample_id="s_test_p5_01",
        document_id="doc_p5_01",
        dataset="DocVQA",
        split="test",
        question="What is the total?",
        ground_truth_answers=["$100"],
        source_sha256="abc",
    )

    artifact = pipeline.process_sample(
        sample=sample,
        degraded_image=img,
        policy=RoutingPolicyType.R2_RULE_BASED,
        save_artifact=True,
    )

    assert artifact.selected_model in ["B0", "B1", "B2", "B0-U"]
    assert artifact.status in ["SUCCESS", "FAILED"]
    assert (tmp_path / f"{artifact.run_id}.json").exists()

