"""
Dense Text Semantic Retrieval Module.
Uses scikit-learn TF-IDF / TruncatedSVD projection to generate dense semantic vector representations
and execute cosine similarity page retrieval.
"""

from typing import List, Dict, Any, Optional
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from src.retrieval.schema import DocumentPageRecord, PageRetrievalResult


class DenseTextRetriever:
    """
    Dense semantic retriever mapping document page text into normalized vector representations.
    """
    def __init__(self, embedding_dim: int = 64, random_state: int = 42):
        self.embedding_dim = embedding_dim
        self.random_state = random_state
        self.vectorizer: Optional[TfidfVectorizer] = None
        self.svd: Optional[TruncatedSVD] = None
        self.pages: List[DocumentPageRecord] = []
        self.page_embeddings: Optional[np.ndarray] = None

    def build(self, pages: List[DocumentPageRecord]) -> None:
        """
        Fit vectorizer and project page text into normalized dense vectors.
        """
        self.pages = list(pages)
        if not self.pages:
            self.page_embeddings = None
            return

        corpus = [p.clean_text or p.raw_text or " " for p in self.pages]
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            max_features=2000,
            sublinear_tf=True
        )
        tfidf_mat = self.vectorizer.fit_transform(corpus)

        n_samples, n_features = tfidf_mat.shape
        n_components = min(self.embedding_dim, n_samples - 1, n_features - 1)

        if n_components >= 2:
            self.svd = TruncatedSVD(n_components=n_components, random_state=self.random_state)
            dense_mat = self.svd.fit_transform(tfidf_mat)
        else:
            self.svd = None
            dense_mat = tfidf_mat.toarray()

        # L2 normalize
        norms = np.linalg.norm(dense_mat, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        self.page_embeddings = dense_mat / norms

    def encode_query(self, query_text: str) -> np.ndarray:
        """
        Encode query string into the same dense vector space.
        """
        if self.vectorizer is None:
            return np.zeros((1, self.embedding_dim), dtype=float)

        q_vec = self.vectorizer.transform([query_text])
        if self.svd is not None:
            dense_q = self.svd.transform(q_vec)
        else:
            dense_q = q_vec.toarray()

        norm = np.linalg.norm(dense_q)
        if norm > 0:
            dense_q = dense_q / norm
        return dense_q

    def search(self, query_text: str, top_k: int = 5) -> List[PageRetrievalResult]:
        """
        Rank pages by cosine similarity against dense query embedding.
        """
        if not self.pages or self.page_embeddings is None:
            return []

        q_emb = self.encode_query(query_text)
        # Cosine similarity: (N, D) @ (1, D).T -> (N,)
        similarities = (self.page_embeddings @ q_emb.T).flatten()

        ranked_indices = np.argsort(-similarities)[:min(top_k, len(self.pages))]

        results = []
        for rank, idx in enumerate(ranked_indices, start=1):
            p = self.pages[idx]
            sim = float(similarities[idx])
            # Normalize negative similarities to 0.0
            norm_score = max(0.0, sim)
            results.append(
                PageRetrievalResult(
                    page_number=p.page_number,
                    score=float(round(norm_score, 6)),
                    text_score=float(round(norm_score, 6)),
                    visual_score=0.0,
                    rank=rank,
                    metadata={
                        "document_id": p.document_id,
                        "raw_similarity": float(round(sim, 6)),
                        "method": "dense_tfidf_svd"
                    }
                )
            )
        return results
