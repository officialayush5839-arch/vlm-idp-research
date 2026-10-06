"""tests/test_phase10_5_retrieval_recovery.py
Unit tests for retrieval retry and window expansion.
"""

from src.recovery.retrieval_recovery import RetrievalRecoveryRetrier
from src.reliability.signals import ObservableSignals


def test_retrieval_retry_gain():
    retrier = RetrievalRecoveryRetrier(window_expansion_gain=0.15)
    sig = ObservableSignals(retrieval_score=0.45, raw_confidence=0.50)
    retried = retrier.retry(sig)
    assert retried.retrieval_score >= 0.60
    assert retried.raw_confidence >= 0.55
