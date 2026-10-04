"""Unit Tests for Timing Breakdown and Latency Measurement."""

import time
from src.vlm.schema import TimingBreakdown


def test_timing_breakdown_accumulation():
    """Verify timing breakdown attributes and sum."""
    tb = TimingBreakdown(
        preprocessing_ms=15.2,
        inference_ms=120.4,
        postprocessing_ms=2.1,
        total_latency_ms=137.7
    )
    assert tb.preprocessing_ms > 0
    assert tb.inference_ms > 0
    assert tb.total_latency_ms >= (tb.preprocessing_ms + tb.inference_ms + tb.postprocessing_ms)
