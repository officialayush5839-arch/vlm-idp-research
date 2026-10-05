"""
Text-based Inverted Index and Lexical Retrieval using BM25.
Indexes document pages and resolves queries to ranked PageRetrievalResult candidate lists.
"""

from typing import List, Dict, Any, Optional
from src.retrieval.bm25 import BM25Okapi, simple_tokenize
from src.retrieval.schema import DocumentPageRecord, PageRetrievalResult


class TextIndex:
    """
    BM25 Lexical Index for page-level retrieval.
    """
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.pages: List[DocumentPageRecord] = []
        self.bm25: Optional[BM25Okapi] = None
        self.page_number_to_idx: Dict[int, int] = {}

    def build(self, pages: List[DocumentPageRecord]) -> None:
        """
        Build inverted BM25 index over provided pages.
        """
        self.pages = list(pages)
        self.page_number_to_idx = {p.page_number: i for i, p in enumerate(self.pages)}

        tokenized_corpus = [simple_tokenize(p.clean_text or p.raw_text) for p in self.pages]
        self.bm25 = BM25Okapi(tokenized_corpus, k1=self.k1, b=self.b)

    def search(self, query_text: str, top_k: int = 5) -> List[PageRetrievalResult]:
        """
        Search for top-k relevant pages using BM25.
        """
        if not self.pages or self.bm25 is None:
            return []

        tokens = simple_tokenize(query_text)
        top_k_indices = self.bm25.get_top_k(tokens, k=min(top_k, len(self.pages)))

        results = []
        for rank, (idx, score) in enumerate(top_k_indices, start=1):
            p = self.pages[idx]
            results.append(
                PageRetrievalResult(
                    page_number=p.page_number,
                    score=float(round(score, 6)),
                    text_score=float(round(score, 6)),
                    visual_score=0.0,
                    rank=rank,
                    metadata={
                        "document_id": p.document_id,
                        "quality_score": p.quality_score,
                        "degradation_level": p.degradation_level
                    }
                )
            )
        return results
