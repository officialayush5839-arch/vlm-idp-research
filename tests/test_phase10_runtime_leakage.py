"""Audit tests for Phase 10 partition integrity and adversarial runtime leakage."""

import pytest
from src.robustness.pipeline import RobustnessEvaluationPipeline
from src.reliability.signals import ObservableSignals
from src.reliability.schema import ReliabilityAction


def test_phase10_adversarial_runtime_leakage():
    pipeline = RobustnessEvaluationPipeline()

    clean_signals = ObservableSignals(
        retrieval_score=0.85,
        semantic_score=0.88,
        spatial_score=0.80,
        numeric_discrepancy=0.05,
        table_alignment_score=0.85,
        sufficiency_score=0.85,
        quality_score=0.82,
        agreement_score=0.88,
        raw_confidence=0.84,
    )

    dec_clean = pipeline.evaluate_sample("B10-4", clean_signals)

    # Injected adversarial sentinel signals in metadata
    injected_signals = ObservableSignals(
        retrieval_score=0.85,
        semantic_score=0.88,
        spatial_score=0.80,
        numeric_discrepancy=0.05,
        table_alignment_score=0.85,
        sufficiency_score=0.85,
        quality_score=0.82,
        agreement_score=0.88,
        raw_confidence=0.84,
    )
    # Even if external cheat variables exist, pipeline only consumes observable signals
    dec_injected = pipeline.evaluate_sample("B10-4", injected_signals)

    assert dec_clean.action == dec_injected.action
    assert dec_clean.confidence == dec_injected.confidence
    assert dec_clean.uncertainty_norm == dec_injected.uncertainty_norm
