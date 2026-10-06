"""tests/test_phase10_5_cost.py
Unit tests verifying cost, token overhead, and latency constraints for Phase 10.5 recovery.
"""

from src.recovery.pipeline import RecoveryPipeline
from src.reliability.signals import ObservableSignals


def test_recovery_pipeline_computational_profile():
    pipeline = RecoveryPipeline()
    sig = ObservableSignals(
        retrieval_score=0.45,
        semantic_score=0.50,
        spatial_score=0.40,
        numeric_discrepancy=0.10,
        table_alignment_score=0.50,
        sufficiency_score=0.45,
        quality_score=0.35,
        agreement_score=0.70,
        raw_confidence=0.45,
    )
    # Execution should be fast and lightweight (< 100ms per sample on CPU)
    import time
    start = time.perf_counter()
    for _ in range(100):
        _ = pipeline.evaluate_sample("B10.5-5", sig)
    dur = time.perf_counter() - start
    avg_ms = (dur / 100) * 1000.0
    assert avg_ms < 50.0, f"Average execution took {avg_ms:.2f} ms (expected < 50ms)"
