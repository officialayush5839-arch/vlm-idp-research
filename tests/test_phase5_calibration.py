"""
Tests for Phase 5 Multi-Signal Uncertainty Adapter and Post-Hoc Calibration.
Verifies strictly that calibration happens only on validation data and evaluates ECE and Brier score.
"""

import numpy as np
import pytest

from src.routing.schema import UncertaintyVector
from src.routing.uncertainty import UncertaintyAdapter
from src.routing.calibration import PostHocCalibrator


def test_uncertainty_adapter_vector_assembly():
    adapter = UncertaintyAdapter.from_config()
    u_vec = adapter.assemble_vector(
        vlm_confidence=0.88,
        ocr_confidence=0.92,
        retrieval_score=0.75,
        grounding_score=0.80,
        visual_quality_score=0.90,
        ocr_vlm_agreement=0.85,
    )
    assert isinstance(u_vec, UncertaintyVector)
    assert u_vec.u_vlm == 0.88
    assert u_vec.u_ocr == 0.92
    assert u_vec.u_ret == 0.75
    assert u_vec.u_gnd == 0.80
    assert u_vec.u_qual == 0.90
    assert u_vec.u_agr == 0.85


def test_post_hoc_calibrator_logistic_fit():
    calibrator = PostHocCalibrator(method="logistic")
    # Synthetic validation data: 50 validation samples
    np.random.seed(42)
    X_val = np.random.uniform(0.1, 0.9, size=(50, 6))
    # Ground-truth binary correctness correlated with signals
    y_val = (X_val.mean(axis=1) > 0.50).astype(int)

    # Fit strictly on validation
    calibrator.fit(X_val, y_val, partition="val")
    assert calibrator.is_fitted is True

    # Test-set calibration prohibition
    with pytest.raises(ValueError, match="strictly forbidden"):
        calibrator.fit(X_val, y_val, partition="test")

    # Predict calibrated confidence
    test_vec = [0.8, 0.85, 0.9, 0.75, 0.95, 0.88]
    c = calibrator.calibrate(test_vec)
    assert 0.0 <= c <= 1.0

    # Decision status mapping
    status = calibrator.get_status(c, tau_accept=0.75, tau_review=0.40)
    assert status in ["VERIFIED", "UNCERTAIN", "REVIEW_REQUIRED"]


def test_calibration_metrics_ece_and_brier():
    calibrator = PostHocCalibrator(method="logistic")
    y_true = np.array([1, 1, 0, 0, 1, 0, 1, 1, 0, 0])
    probs = np.array([0.9, 0.8, 0.2, 0.1, 0.7, 0.4, 0.85, 0.95, 0.3, 0.15])

    ece = calibrator.compute_ece(probs, y_true, num_bins=5)
    brier = calibrator.compute_brier_score(probs, y_true)

    assert 0.0 <= ece <= 1.0
    assert 0.0 <= brier <= 1.0
