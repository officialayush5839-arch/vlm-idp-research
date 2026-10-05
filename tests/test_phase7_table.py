"""
Unit tests for Phase 7 Table Verifier.
"""

from src.evidence.table_verifier import TableVerifier


def test_is_tabular_text():
    verifier = TableVerifier()
    text_pipes = "Item | Qty | Price\nWidget | 5 | $10.00"
    text_plain = "This is a regular narrative paragraph without tables."
    assert verifier.is_tabular_text(text_pipes) is True
    assert verifier.is_tabular_text(text_plain) is False


def test_verify_table_cell_pass():
    verifier = TableVerifier(tabular_min_score=0.50)
    snippet = "Revenue | 2022 | 2023\nNorth America | 120M | 150M\nEurope | 80M | 95M"
    res = verifier.verify_table_cell(
        row_header_query="North America",
        col_header_query="2023",
        answer_value="150M",
        table_snippet=snippet
    )
    assert res["is_tabular"] is True
    assert res["passes_verification"] is True
    assert res["table_alignment_score"] == 1.0


def test_verify_table_cell_fail():
    verifier = TableVerifier(tabular_min_score=0.50)
    snippet = "Revenue | 2022 | 2023\nNorth America | 120M | 150M"
    res = verifier.verify_table_cell(
        row_header_query="North America",
        col_header_query="2023",
        answer_value="999M",
        table_snippet=snippet
    )
    assert res["passes_verification"] is False
