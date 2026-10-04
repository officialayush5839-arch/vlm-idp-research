"""Unit Tests for Metrics and Answer Normalization."""

from src.evaluation.metrics import (
    normalize_answer,
    compute_exact_match,
    compute_token_f1,
    compute_anls,
    compute_cer,
    compute_wer
)


def test_answer_normalization():
    """Verify standard text normalization operations."""
    assert normalize_answer("  The Apple, Inc.  ") == "apple inc"
    assert normalize_answer("A Document!") == "document"
    assert normalize_answer("An Example?") == "example"


def test_exact_match():
    """Verify Exact Match logic with normalization."""
    assert compute_exact_match("Apple Inc.", ["apple inc", "Apple"]) == 1.0
    assert compute_exact_match("Banana", ["apple inc", "Apple"]) == 0.0


def test_token_f1():
    """Verify Token F1 calculation."""
    # Complete match
    assert compute_token_f1("Invoice 1234", ["invoice 1234"]) == 1.0
    # Partial match
    f1 = compute_token_f1("Total Invoice 1234", ["Invoice 1234"])
    assert 0.7 < f1 < 0.9
    # No match
    assert compute_token_f1("Completely Different", ["Invoice 1234"]) == 0.0


def test_anls():
    """Verify ANLS Levenshtein similarity with tau threshold."""
    # Perfect match
    assert compute_anls("invoice", ["invoice"]) == 1.0
    # Minor typo (1 char edit out of 7 -> 1/7 = 0.1428 < 0.50)
    sim = compute_anls("invoicx", ["invoice"])
    assert sim > 0.8
    # Major difference (exceeding tau 0.50)
    assert compute_anls("completely different", ["invoice"]) == 0.0


def test_cer_and_wer():
    """Verify Character and Word Error Rate calculation."""
    # CER
    assert compute_cer("abc", "abc") == 0.0
    assert compute_cer("abx", "abc") == pytest_round(1 / 3, 4)

    # WER
    assert compute_wer("the invoice total", "the invoice total") == 0.0
    assert compute_wer("the invoice amount", "the invoice total") == pytest_round(1 / 3, 4)


def pytest_round(val: float, digits: int) -> float:
    return round(val, digits)
