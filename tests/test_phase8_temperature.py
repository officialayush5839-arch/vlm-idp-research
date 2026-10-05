"""
Unit tests for Temperature Scaling Calibrator.
"""

import pytest
from src.uncertainty.temperature import TemperatureScalingCalibrator, logit, sigmoid


def test_logit_sigmoid_roundtrip():
    p = 0.75
    z = logit(p)
    p_rec = sigmoid(z)
    assert p_rec == pytest.approx(p, 1e-4)


def test_temperature_scaling_fit_and_predict():
    cal = TemperatureScalingCalibrator()
    # Overconfident model: predicted confidences 0.9, but ground truth accuracy is only 0.5
    confs = [0.95, 0.90, 0.85, 0.92, 0.88, 0.91]
    labels = [1, 0, 1, 0, 0, 1]  # 50% accuracy

    cal.fit(confs, labels)
    assert cal.is_fitted is True
    # Temperature should be > 1.0 to soften overconfident logits
    assert cal.temperature > 1.0

    # Calibrated probability should be lower than raw overconfident 0.90
    cal_p = cal.predict(0.90)
    assert cal_p < 0.90
