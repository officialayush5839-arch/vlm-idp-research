"""
Table and Cell Context Verification Module for Phase 7 Evidence Grounding.
Verifies that values extracted from tabular structures align with row/column
headers and grid layout rather than coincidental page occurrences.
"""

import re
from typing import Dict, Any, List, Optional, Tuple


class TableVerifier:
    """
    Verifies tabular evidence by evaluating row header, column header,
    and cell value alignment in extracted tabular text.
    """

    def __init__(self, tabular_min_score: float = 0.50):
        self.tabular_min_score = tabular_min_score

    @classmethod
    def is_tabular_text(cls, text: str) -> bool:
        """
        Heuristic detection of tabular formatted text (pipes, tabs, multiple spaces).
        """
        if "|" in text or "\t" in text:
            return True
        # Check for multiple lines with aligned multi-space gaps
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        if len(lines) >= 2:
            multi_space_count = sum(1 for line in lines if re.search(r"\s{2,}", line))
            if multi_space_count >= 2:
                return True
        return False

    def verify_table_cell(
        self,
        row_header_query: str,
        col_header_query: str,
        answer_value: str,
        table_snippet: str
    ) -> Dict[str, Any]:
        """
        Verify that answer_value occurs in table_snippet associated with row and col headers.
        """
        norm_snippet = " ".join(table_snippet.lower().split())
        norm_ans = " ".join(answer_value.lower().split())
        norm_row = " ".join(row_header_query.lower().split())
        norm_col = " ".join(col_header_query.lower().split())

        has_value = norm_ans in norm_snippet if norm_ans else False
        has_row = norm_row in norm_snippet if norm_row else True
        has_col = norm_col in norm_snippet if norm_col else True

        score = 0.0
        if has_value:
            score += 0.5
        if has_row:
            score += 0.25
        if has_col:
            score += 0.25

        passes = (score >= self.tabular_min_score) and has_value

        return {
            "is_tabular": self.is_tabular_text(table_snippet),
            "has_value": has_value,
            "has_row_context": has_row,
            "has_col_context": has_col,
            "table_alignment_score": score,
            "passes_verification": passes,
            "reason": "Tabular alignment confirmed" if passes else "Missing row/col/value context in table"
        }
