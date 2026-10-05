"""
Unit tests for Phase 8 Signal Extraction and Feature Aggregator.
"""

from src.uncertainty.signals import SignalExtractor, compute_normalized_entropy, compute_score_margin
from src.uncertainty.features import FeatureAggregator


def test_compute_entropy_and_margin():
    # Peaked distribution (low entropy, high margin)
    scores = [0.95, 0.20, 0.10]
    ent = compute_normalized_entropy(scores)
    margin = compute_score_margin(scores)
    assert ent < 0.70
    assert margin > 0.70

    # Flat distribution (high entropy, low margin)
    flat_scores = [0.5, 0.5, 0.5]
    flat_ent = compute_normalized_entropy(flat_scores)
    flat_margin = compute_score_margin(flat_scores)
    assert flat_ent > 0.95
    assert flat_margin == 0.0


def test_signal_extractor():
    extractor = SignalExtractor()
    feats = extractor.extract_features(
        model_confidence=0.9,
        page_retrieval_scores=[0.9, 0.3],
        phase7_support_result={"semantic_score": 0.85, "coverage_score": 0.8, "spatial_score": 1.0, "sufficiency_status": "SUFFICIENT"},
        phase7_grounding_result={"grounding_status": "GROUNDED"},
        overall_quality=0.95,
        quality_features={"blur": 0.05, "noise": 0.02}
    )

    assert feats.model_confidence == 0.9
    assert feats.semantic_support_score == 0.85
    assert feats.sufficiency_status == "SUFFICIENT"
    assert feats.visual_quality_score == 0.95


def test_feature_aggregator():
    extractor = SignalExtractor()
    aggregator = FeatureAggregator()

    feats = extractor.extract_features(
        model_confidence=0.9,
        page_retrieval_scores=[0.9, 0.2],
        phase7_support_result={"semantic_score": 0.9, "coverage_score": 0.9, "spatial_score": 1.0},
        phase7_grounding_result={"grounding_status": "GROUNDED"},
        overall_quality=0.9
    )

    conf = aggregator.compute_composite_confidence(feats)
    assert 0.8 <= conf <= 1.0
