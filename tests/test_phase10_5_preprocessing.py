"""tests/test_phase10_5_preprocessing.py
Unit tests for visual preprocessing restoration module.
"""

from src.recovery.preprocessing import VisualPreprocessingRecovery
from src.reliability.signals import ObservableSignals


def test_preprocessing_quality_boost():
    pre = VisualPreprocessingRecovery(expected_quality_gain=0.20)
    sig = ObservableSignals(quality_score=0.40, raw_confidence=0.45)
    restored = pre.apply_recovery(sig)
    assert restored.quality_score >= 0.60
    assert restored.raw_confidence >= 0.55
    assert restored.quality_score <= 1.0
