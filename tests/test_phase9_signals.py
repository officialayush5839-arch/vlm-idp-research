"""Tests for observable signal extraction and 8D uncertainty vector math."""

import pytest
from src.reliability.signals import ObservableSignals, SignalExtractor
from src.reliability.uncertainty import UncertaintyCalculator
from src.reliability.schema import UncertaintyVector


def test_observable_signals_defaults():
    sig = ObservableSignals()
    assert sig.retrieval_score == 0.0
    assert sig.quality_score == 1.0


def test_signal_extractor_from_phase_outputs():
    # Simulate outputs from phase 3, 6, 7, 8
    phase3_output = {"quality_score": 0.82, "blur_score": 0.15}
    phase6_output = {"top1_score": 0.78, "margin": 0.12}
    phase7_output = {
        "status": "VERIFIED",
        "semantic_similarity": 0.85,
        "spatial_overlap": 0.90,
        "numeric_discrepancy": 0.05,
        "table_alignment_score": 0.88,
        "sufficiency_score": 0.92,
    }
    phase8_output = {"agreement_score": 0.89, "raw_confidence": 0.85}

    signals = SignalExtractor.extract(
        phase3_output=phase3_output,
        phase6_output=phase6_output,
        phase7_output=phase7_output,
        phase8_output=phase8_output,
    )

    assert signals.quality_score == 0.82
    assert signals.retrieval_score == 0.78
    assert signals.spatial_score == 0.90
    assert signals.agreement_score == 0.89


def test_uncertainty_calculator_vector_mapping():
    sig = ObservableSignals(
        retrieval_score=0.80,
        semantic_score=0.85,
        spatial_score=0.90,
        numeric_discrepancy=0.10,
        table_alignment_score=0.75,
        sufficiency_score=0.88,
        quality_score=0.70,
        agreement_score=0.95,
    )

    vec = UncertaintyCalculator.compute_uncertainty_vector(sig)
    assert isinstance(vec, UncertaintyVector)
    # Check inverse mappings: 1.0 - score
    assert pytest.approx(vec.u_retrieval, 0.01) == 0.20
    assert pytest.approx(vec.u_semantic, 0.01) == 0.15
    assert pytest.approx(vec.u_spatial, 0.01) == 0.10
    assert pytest.approx(vec.u_numeric, 0.01) == 0.10  # numeric discrepancy is direct
    assert pytest.approx(vec.u_table, 0.01) == 0.25
    assert pytest.approx(vec.u_sufficiency, 0.01) == 0.12
    assert pytest.approx(vec.u_quality, 0.01) == 0.30
    assert pytest.approx(vec.u_agreement, 0.01) == 0.05

    # Check norm is in [0, 1]
    assert 0.0 <= vec.l2_norm <= 1.0
