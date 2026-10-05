"""
Tests for Phase 5.1 Uncertainty Vector Clean Assembly (Audit Defect P1-02).
Verifies that uncertainty vector is assembled strictly from observable visual features
without accessing benchmark condition metadata (severity, family) or ground-truth labels.
"""

import pytest
from src.routing.uncertainty import UncertaintyAdapter
from src.routing.schema import UncertaintyVector


def test_uncertainty_clean_assembly_no_condition_metadata():
    """Verify uncertainty vector derivation from pure visual features."""
    adapter = UncertaintyAdapter()

    # Clean document features
    clean_features = {
        "blur": 0.05,
        "noise": 0.02,
        "skew": 0.01,
        "perspective": 0.01,
        "occlusion": 0.0,
        "resolution": 0.05,
    }
    u_clean = adapter.assemble_from_quality_features(clean_features, overall_quality=0.95)

    assert isinstance(u_clean, UncertaintyVector)
    assert 0.0 <= u_clean.u_ocr <= 1.0
    assert 0.0 <= u_clean.u_vlm <= 1.0
    assert u_clean.u_ocr > 0.80
    assert u_clean.u_vlm > 0.80

    # Heavily distorted document features (high skew & perspective)
    skewed_features = {
        "blur": 0.05,
        "noise": 0.02,
        "skew": 0.85,
        "perspective": 0.70,
        "occlusion": 0.0,
        "resolution": 0.05,
    }
    u_skewed = adapter.assemble_from_quality_features(skewed_features, overall_quality=0.60)

    # OCR should be heavily penalized by geometric distortion
    assert u_skewed.u_ocr < u_clean.u_ocr
    # VLM should remain significantly more robust to geometric skew
    assert u_skewed.u_vlm > u_skewed.u_ocr


def test_uncertainty_weighted_confidence_monotonicity():
    """Verify confidence decreases monotonically with image degradation."""
    adapter = UncertaintyAdapter()

    conf_prev = 1.0
    for sev_level in range(5):
        deg_amount = sev_level * 0.20
        feats = {
            "blur": deg_amount,
            "noise": deg_amount,
            "skew": deg_amount * 0.5,
            "occlusion": deg_amount * 0.3,
            "resolution": deg_amount,
        }
        u_vec = adapter.assemble_from_quality_features(feats, overall_quality=1.0 - deg_amount)
        conf = adapter.compute_weighted_confidence(u_vec)
        assert conf <= conf_prev + 1e-6
        conf_prev = conf
