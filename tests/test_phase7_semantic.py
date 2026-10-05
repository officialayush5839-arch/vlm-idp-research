"""
Unit tests for Phase 7 Semantic Support Verifier.
"""

from src.evidence.semantic_support import (
    tokenize_text,
    compute_token_jaccard,
    compute_token_recall,
    SemanticSupportVerifier
)


def test_tokenize_text():
    tokens = tokenize_text("Net Income in 2024: $45.2M!")
    assert tokens == ["net", "income", "in", "2024", "45", "2m"]


def test_token_jaccard_and_recall():
    toks1 = ["net", "income", "2024"]
    toks2 = ["total", "net", "income", "2024", "march"]
    # inter = 3 ("net", "income", "2024")
    # union = 5
    # jaccard = 3/5 = 0.6
    # recall = 3/3 = 1.0
    assert compute_token_jaccard(toks1, toks2) == 0.6
    assert compute_token_recall(toks1, toks2) == 1.0


def test_semantic_support_verifier_exact():
    verifier = SemanticSupportVerifier(min_support_threshold=0.50)
    res = verifier.verify_support(
        query_text="What was the total operating cost?",
        answer_text="$1,200,000",
        evidence_text="During the fiscal year, total operating cost amounted to $1,200,000 across all units."
    )
    assert res["is_supported"] is True
    assert res["heuristic_support_score"] == 1.0
    assert res["exact_substring_match"] is True


def test_semantic_support_verifier_partial():
    verifier = SemanticSupportVerifier(min_support_threshold=0.40)
    res = verifier.verify_support(
        query_text="Who is the primary vendor?",
        answer_text="Acme Global Logistics Incorporated",
        evidence_text="Shipment dispatched via Acme Global Logistics fleet on Monday."
    )
    assert res["is_supported"] is True
    assert res["exact_substring_match"] is False
    assert res["token_recall"] >= 0.75


def test_semantic_support_verifier_unsupported():
    verifier = SemanticSupportVerifier(min_support_threshold=0.50)
    res = verifier.verify_support(
        query_text="What is the discount percentage?",
        answer_text="25 percent discount",
        evidence_text="Standard terms apply with 0% discount on wholesale orders."
    )
    # The tokens "25", "percent", "discount" -> only "percent", "discount" overlap, but "25" is missing
    # Let's verify score calculation
    assert res["heuristic_support_score"] < 1.0
