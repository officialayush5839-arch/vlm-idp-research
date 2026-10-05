"""
Unit tests for Isotonic Regression Calibrator.
"""

from src.uncertainty.isotonic import IsotonicRegressionCalibrator


def test_isotonic_regression_fit_and_monotonicity():
    cal = IsotonicRegressionCalibrator()
    confs = [0.1, 0.2, 0.4, 0.6, 0.7, 0.8, 0.9]
    labels = [0, 0, 0, 1, 1, 1, 1]

    cal.fit(confs, labels)
    assert cal.is_fitted is True

    preds = cal.predict_batch([0.15, 0.5, 0.85])
    # Monotonicity check
    assert preds[0] <= preds[1] <= preds[2]
    assert 0.0 <= preds[0] <= 1.0


def test_isotonic_regression_serialization():
    cal = IsotonicRegressionCalibrator()
    confs = [0.2, 0.5, 0.8]
    labels = [0, 1, 1]
    cal.fit(confs, labels)

    d = cal.to_dict()
    cal_rec = IsotonicRegressionCalibrator.from_dict(d)
    assert cal_rec.predict(0.5) == cal.predict(0.5)
