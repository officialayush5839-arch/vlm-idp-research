import pytest
from src.uncertainty.schema import UncertaintyFeatures, AbstentionDecision
from src.uncertainty.abstention import AbstentionPolicy


def test_abstention_policy_threshold_selection():
    # Validation confidences
    val_confidences = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    policy = AbstentionPolicy()
    thresholds = policy.fit_coverage_thresholds(val_confidences, target_coverages=[1.0, 0.8, 0.5])

    assert 1.0 in thresholds
    assert 0.8 in thresholds
    assert 0.5 in thresholds
    assert thresholds[1.0] <= 0.15
    assert thresholds[0.5] >= 0.55


def test_abstention_policy_decisions():
    policy = AbstentionPolicy()
    policy.set_threshold(0.65)

    feat_high = UncertaintyFeatures(
        model_confidence=0.85,
        retrieval_margin=0.6,
        retrieval_entropy=0.2,
        semantic_support_score=0.9,
        entity_coverage=0.9,
        spatial_valid=1.0,
        sufficiency_status="SUFFICIENT",
        grounding_status="GROUNDED",
        citation_count=2,
        visual_quality_score=0.85,
        composite_raw_confidence=0.85
    )

    decision_high = policy.decide(confidence=0.85, features=feat_high)
    assert decision_high.decision == "ANSWER"
    assert decision_high.abstention_reason == ""
    assert decision_high.margin >= 0.0

    feat_low = UncertaintyFeatures(
        model_confidence=0.35,
        retrieval_margin=0.1,
        retrieval_entropy=0.8,
        semantic_support_score=0.3,
        entity_coverage=0.2,
        spatial_valid=0.0,
        sufficiency_status="INSUFFICIENT",
        grounding_status="UNSUPPORTED",
        citation_count=0,
        visual_quality_score=0.3,
        composite_raw_confidence=0.35
    )

    decision_low = policy.decide(confidence=0.35, features=feat_low)
    assert decision_low.decision == "ABSTAIN"
    assert decision_low.abstention_reason == "INSUFFICIENT_EVIDENCE"
    assert decision_low.margin < 0.0
