"""
Unit tests for Phase 7 Numeric Verifier.
"""

from src.evidence.numeric_verifier import NumericVerifier


def test_extract_numeric_tokens():
    verifier = NumericVerifier()
    text = "Revenue grew to $48.7M from $32.1 million, an increase of 15%."
    tokens = verifier.extract_numeric_tokens(text)
    assert len(tokens) >= 3

    # Check 48.7M
    tok0 = tokens[0]
    assert tok0["value"] == 48.7
    assert "USD" in tok0["units"]
    assert "MILLION" in tok0["units"]

    # Check 15%
    tok2 = tokens[2]
    assert tok2["value"] == 15.0
    assert "PERCENT" in tok2["units"]


def test_numeric_verifier_exact():
    verifier = NumericVerifier()
    res = verifier.verify_numeric_support(
        answer_text="$1,450.00",
        evidence_text="Balance remaining is $1,450.00 due on receipt."
    )
    assert res["is_numeric_claim"] is True
    assert res["is_verified"] is True


def test_numeric_verifier_scale():
    verifier = NumericVerifier()
    res = verifier.verify_numeric_support(
        answer_text="$48.7M",
        evidence_text="Total company revenue reached 48,700,000 USD."
    )
    assert res["is_numeric_claim"] is True
    assert res["is_verified"] is True


def test_numeric_verifier_mismatch():
    verifier = NumericVerifier()
    res = verifier.verify_numeric_support(
        answer_text="$48.7M",
        evidence_text="Invoice item subtotal: $487.00."
    )
    assert res["is_numeric_claim"] is True
    assert res["is_verified"] is False


def test_non_numeric_claim():
    verifier = NumericVerifier()
    res = verifier.verify_numeric_support(
        answer_text="Acme Corporation",
        evidence_text="Vendor: Acme Corporation"
    )
    assert res["is_numeric_claim"] is False
    assert res["is_verified"] is True
