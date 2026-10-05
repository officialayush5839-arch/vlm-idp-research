"""
Evidence Sufficiency Assessment Module for Phase 7 Evidence Grounding.
Determines whether retrieved evidence contains sufficient information
to answer a query or whether essential entities are missing.
"""

from typing import List, Dict, Any, Set, Literal
import re
from src.evidence.schema import EvidenceUnit
from src.evidence.semantic_support import tokenize_text


class EvidenceSufficiencyEvaluator:
    """
    Evaluates evidence sufficiency by analyzing coverage of query requirements
    within candidate evidence text.
    """

    def __init__(
        self,
        min_coverage_sufficient: float = 0.70,
        min_coverage_partial: float = 0.40,
        stop_words: Set[str] = None
    ):
        self.min_coverage_sufficient = min_coverage_sufficient
        self.min_coverage_partial = min_coverage_partial
        self.stop_words = stop_words or {
            "what", "which", "where", "when", "who", "why", "how", "is", "are",
            "was", "were", "the", "a", "an", "of", "in", "for", "to", "on", "at",
            "by", "with", "from", "as", "about", "into", "through", "after", "over"
        }

    def extract_query_essential_tokens(self, query_text: str) -> List[str]:
        tokens = tokenize_text(query_text)
        return [t for t in tokens if t not in self.stop_words and len(t) > 1]

    def evaluate_sufficiency(
        self,
        query_text: str,
        evidence_units: List[EvidenceUnit]
    ) -> Dict[str, Any]:
        """
        Evaluate whether the evidence units collectively cover the essential query tokens.
        """
        if not evidence_units:
            return {
                "sufficiency_status": "INSUFFICIENT",
                "coverage_score": 0.0,
                "covered_tokens": [],
                "missing_tokens": self.extract_query_essential_tokens(query_text),
                "reason": "No evidence units provided"
            }

        essential_tokens = self.extract_query_essential_tokens(query_text)
        if not essential_tokens:
            # Query has no content words (unlikely, but fallback)
            return {
                "sufficiency_status": "SUFFICIENT",
                "coverage_score": 1.0,
                "covered_tokens": [],
                "missing_tokens": [],
                "reason": "Query contains no discriminative content tokens"
            }

        combined_ev_text = " ".join(u.text.lower() for u in evidence_units)
        ev_tokens = set(tokenize_text(combined_ev_text))

        covered = [t for t in essential_tokens if t in ev_tokens]
        missing = [t for t in essential_tokens if t not in ev_tokens]
        coverage_score = round(float(len(covered)) / float(len(essential_tokens)), 6)

        if coverage_score >= self.min_coverage_sufficient:
            status = "SUFFICIENT"
        elif coverage_score >= self.min_coverage_partial:
            status = "PARTIALLY_SUFFICIENT"
        else:
            status = "INSUFFICIENT"

        return {
            "sufficiency_status": status,
            "coverage_score": coverage_score,
            "covered_tokens": covered,
            "missing_tokens": missing,
            "reason": f"Coverage {coverage_score:.2f} (covered {len(covered)}/{len(essential_tokens)} tokens)"
        }
