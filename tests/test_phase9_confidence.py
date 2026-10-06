"""Tests for confidence models C0 (Raw), C1 (Weighted), C2 (Calibrated)."""

import pytest
from src.reliability.confidence import RawConfidenceModel, WeightedConfidenceModel, CalibratedCompositeModel
from src.reliability.schema import UncertaintyVector


def test_raw_confidence_model():
    model = RawConfidenceModel()
    score = model.compute(raw_confidence=0.88)
    assert score == 0.88


def test_weighted_confidence_model():
    weights = {
        "w_retrieval": 0.2,
        "w_semantic": 0.2,
        "w_spatial": 0.1,
        "w_numeric": 0.1,
        "w_table": 0.1,
        "w_sufficiency": 0.1,
        "w_quality": 0.1,
        "w_agreement": 0.1,
    }
    model = WeightedConfidenceModel(weights=weights)
    vec = UncertaintyVector.zeros()  # all uncertainties 0 -> all confidences 1.0
    conf = model.compute(uncertainty_vector=vec)
    assert pytest.approx(conf, 0.001) == 1.0

    vec_high = UncertaintyVector.ones()
    conf_low = model.compute(uncertainty_vector=vec_high)
    assert pytest.approx(conf_low, 0.001) == 0.0


def test_calibrated_composite_model_temperature_scaling():
    weights = {
        "w_retrieval": 0.15,
        "w_semantic": 0.15,
        "w_spatial": 0.15,
        "w_numeric": 0.15,
        "w_table": 0.10,
        "w_sufficiency": 0.15,
        "w_quality": 0.10,
        "w_agreement": 0.05,
    }
    model = CalibratedCompositeModel(weights=weights, temperature=1.5)
    vec = UncertaintyVector(0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1)
    conf = model.compute(uncertainty_vector=vec)
    assert 0.0 <= conf <= 1.0
