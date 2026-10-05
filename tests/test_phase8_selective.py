import pytest
from src.uncertainty.selective import compute_selective_prediction_curve, compute_aurc


def test_selective_prediction_curve():
    # 10 predictions: (confidence, is_correct)
    predictions = [
        {"confidence": 0.95, "is_correct": 1},
        {"confidence": 0.90, "is_correct": 1},
        {"confidence": 0.85, "is_correct": 1},
        {"confidence": 0.80, "is_correct": 1},
        {"confidence": 0.70, "is_correct": 1},
        {"confidence": 0.60, "is_correct": 0},
        {"confidence": 0.50, "is_correct": 1},
        {"confidence": 0.40, "is_correct": 0},
        {"confidence": 0.30, "is_correct": 0},
        {"confidence": 0.20, "is_correct": 0},
    ]

    target_coverages = [1.0, 0.8, 0.5]
    results = compute_selective_prediction_curve(predictions, target_coverages=target_coverages)

    assert len(results) == 3
    # At coverage 1.0 (all 10): 6 correct, 4 wrong => risk = 4/10 = 0.40
    assert results[0].target_coverage == 1.0
    assert abs(results[0].selective_risk - 0.40) < 1e-4
    assert abs(results[0].selective_accuracy - 0.60) < 1e-4

    # At coverage 0.5 (top 5): all 5 correct => risk = 0.0, accuracy = 1.0
    res_50 = [r for r in results if r.target_coverage == 0.5][0]
    assert abs(res_50.selective_risk - 0.0) < 1e-4
    assert abs(res_50.selective_accuracy - 1.0) < 1e-4


def test_aurc_computation():
    coverages = [0.5, 0.8, 1.0]
    risks = [0.0, 0.125, 0.3]
    aurc, excess_aurc = compute_aurc(coverages, risks, overall_risk=0.3)
    assert aurc >= 0.0
    assert excess_aurc >= 0.0
