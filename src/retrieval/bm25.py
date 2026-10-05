"""
Deterministic Pure-Python BM25 (Okapi) implementation for Lexical Document and Page Retrieval.
Designed for CPU-only, dependency-free execution with Robertson-Spärck Jones IDF smoothing.
"""

import math
import re
from typing import List, Dict, Optional, Tuple


def simple_tokenize(text: str) -> List[str]:
    """
    Standard lowercased alphanumeric tokenizer.
    """
    if not text:
        return []
    return re.findall(r"\b\w+\b", text.lower())


class BM25Okapi:
    """
    BM25Okapi scoring model for lexical retrieval.
    """
    def __init__(
        self,
        corpus: List[List[str]],
        k1: float = 1.5,
        b: float = 0.75,
        epsilon: float = 0.25
    ):
        self.k1 = float(k1)
        self.b = float(b)
        self.epsilon = float(epsilon)
        self.corpus_size = len(corpus)
        self.doc_lengths: List[int] = [len(doc) for doc in corpus]
        self.avgdl = sum(self.doc_lengths) / self.corpus_size if self.corpus_size > 0 else 0.0

        self.doc_freqs: List[Dict[str, int]] = []
        self.nd: Dict[str, int] = {}
        self.idf: Dict[str, float] = {}

        self._initialize(corpus)

    def _initialize(self, corpus: List[List[str]]):
        for doc in corpus:
            frequencies: Dict[str, int] = {}
            for word in doc:
                frequencies[word] = frequencies.get(word, 0) + 1
            self.doc_freqs.append(frequencies)

            for word in frequencies:
                self.nd[word] = self.nd.get(word, 0) + 1

        # Calculate IDF with RSJ smoothing
        idf_sum = 0.0
        negative_idfs = []
        for word, freq in self.nd.items():
            # Robertson-Spärck Jones formula
            val = (self.corpus_size - freq + 0.5) / (freq + 0.5)
            # Add 1.0 inside log to guarantee non-negativity or handle negative
            idf_val = math.log(val + 1.0)
            self.idf[word] = idf_val
            idf_sum += idf_val
            if idf_val < 0:
                negative_idfs.append(word)

        avg_idf = idf_sum / len(self.nd) if self.nd else 0.0
        eps_idf = self.epsilon * avg_idf
        for word in negative_idfs:
            self.idf[word] = eps_idf

    def get_scores(self, query_tokens: List[str]) -> List[float]:
        """
        Calculate BM25 scores for all corpus documents against query tokens.
        """
        if self.corpus_size == 0 or not query_tokens:
            return [0.0] * self.corpus_size

        scores = [0.0] * self.corpus_size
        if self.avgdl == 0.0:
            return scores

        for q_token in query_tokens:
            if q_token not in self.idf:
                continue
            idf_val = self.idf[q_token]
            for doc_idx in range(self.corpus_size):
                f = self.doc_freqs[doc_idx].get(q_token, 0)
                if f > 0:
                    doc_len = self.doc_lengths[doc_idx]
                    denom = f + self.k1 * (1.0 - self.b + self.b * (doc_len / self.avgdl))
                    numerator = f * (self.k1 + 1.0)
                    scores[doc_idx] += idf_val * (numerator / denom)

        return scores

    def get_top_k(self, query_tokens: List[str], k: int = 5) -> List[Tuple[int, float]]:
        """
        Retrieve top-k ranked document indices and their BM25 scores.
        """
        scores = self.get_scores(query_tokens)
        scored_indices = list(enumerate(scores))
        scored_indices.sort(key=lambda x: x[1], reverse=True)
        return scored_indices[:k]
