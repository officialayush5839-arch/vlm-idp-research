"""
Semantic Support Assessment Module for Phase 7 Evidence Grounding.
Computes observable lexical and entity overlap between answer hypotheses
and extracted evidence units.
Scores are explicitly designated as 'heuristic semantic support score'
rather than calibrated probabilities.
"""

import re
from typing import List, Dict, Any, Tuple, Set, Optional


def tokenize_text(text: str) -> List[str]:
    """
    Standard whitespace and punctuation tokenizer with case normalization.
    """
    clean = re.sub(r"[^\w\s]", " ", text.lower())
    return [tok for tok in clean.split() if tok]


def compute_token_jaccard(tokens_a: List[str], tokens_b: List[str]) -> float:
    """
    Compute Jaccard similarity between two token sets.
    """
    set_a = set(tokens_a)
    set_b = set(tokens_b)
    if not set_a or not set_b:
        return 0.0
    inter = len(set_a.intersection(set_b))
    union = len(set_a.union(set_b))
    return round(float(inter) / float(union), 6)


def compute_token_recall(reference_tokens: List[str], candidate_tokens: List[str]) -> float:
    """
    Compute token recall of reference tokens in candidate token set.
    """
    set_ref = set(reference_tokens)
    set_cand = set(candidate_tokens)
    if not set_ref:
        return 0.0
    inter = len(set_ref.intersection(set_cand))
    return round(float(inter) / float(len(set_ref)), 6)


class SemanticSupportVerifier:
    """
    Verifies semantic alignment between candidate answers and evidence units.
    Operates strictly on observable textual content without oracle knowledge.
    """

    def __init__(
        self,
        min_support_threshold: float = 0.50,
        stop_words: Optional[Set[str]] = None
    ):
        self.min_support_threshold = min_support_threshold
        self.stop_words = stop_words or {
            "a", "an", "the", "in", "on", "at", "to", "for", "of", "with",
            "is", "are", "was", "were", "be", "been", "by", "that", "this", "it"
        }

    def filter_content_tokens(self, tokens: List[str]) -> List[str]:
        return [t for t in tokens if t not in self.stop_words]

    def verify_support(
        self,
        query_text: str,
        answer_text: str,
        evidence_text: str
    ) -> Dict[str, Any]:
        """
        Evaluate heuristic semantic support for an answer given evidence text.
        """
        ans_clean = answer_text.strip()
        ev_clean = evidence_text.strip()

        if not ans_clean or not ev_clean:
            return {
                "heuristic_support_score": 0.0,
                "is_supported": False,
                "token_recall": 0.0,
                "token_jaccard": 0.0,
                "exact_substring_match": False,
                "reason": "Empty answer or evidence string"
            }

        # Substring match (normalized)
        norm_ans = " ".join(ans_clean.lower().split())
        norm_ev = " ".join(ev_clean.lower().split())
        exact_sub = norm_ans in norm_ev

        ans_tokens = tokenize_text(ans_clean)
        content_ans_tokens = self.filter_content_tokens(ans_tokens) or ans_tokens
        ev_tokens = tokenize_text(ev_clean)

        tok_recall = compute_token_recall(content_ans_tokens, ev_tokens)
        tok_jaccard = compute_token_jaccard(content_ans_tokens, ev_tokens)

        # Composite heuristic: weight exact match, recall, and jaccard
        if exact_sub:
            heuristic_score = 1.0
        else:
            heuristic_score = round(0.70 * tok_recall + 0.30 * tok_jaccard, 6)

        is_supp = heuristic_score >= self.min_support_threshold

        return {
            "heuristic_support_score": heuristic_score,
            "is_supported": is_supp,
            "token_recall": tok_recall,
            "token_jaccard": tok_jaccard,
            "exact_substring_match": exact_sub,
            "reason": "Exact match" if exact_sub else f"Token recall: {tok_recall:.3f}"
        }
