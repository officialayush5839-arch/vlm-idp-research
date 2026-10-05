"""
Unified Hierarchical Multimodal Retrieval Pipeline for Long Documents.
Supports baseline hierarchy:
  - B6-0: Random Page Retrieval
  - B6-1: BM25 Lexical Text Retrieval
  - B6-2: Dense Text Retrieval
  - B6-3: Visual Feature Retrieval
  - B6-4: Multimodal Hybrid Retrieval (Text + Visual fusion with alpha=0.60)
  - B6-5: Hierarchical Multimodal Retrieval + Region Selection + Reranker (Proposed)
"""

import random
import time
from typing import List, Dict, Any, Optional
from src.retrieval.schema import (
    DocumentPageRecord,
    RetrievalQuery,
    PageRetrievalResult,
    RegionRetrievalResult,
    EvidencePackage
)
from src.retrieval.text_index import TextIndex
from src.retrieval.dense_retrieval import DenseTextRetriever
from src.retrieval.visual_index import VisualRetriever
from src.retrieval.fusion import MultimodalFusion
from src.retrieval.reranker import CrossModalReranker
from src.retrieval.region import RegionRetriever
from src.retrieval.evidence import EvidencePackageBuilder
from src.retrieval.provenance import create_retrieval_provenance


class MultimodalRetrievalPipeline:
    """
    Master pipeline orchestrating indexing, search, fusion, reranking, and evidence packaging.
    """
    def __init__(
        self,
        alpha_text: float = 0.60,
        random_seed: int = 42,
        evidence_dir: str = "experiments/phase6/evidence"
    ):
        self.alpha_text = float(alpha_text)
        self.random_seed = int(random_seed)
        self.evidence_builder = EvidencePackageBuilder(output_dir=evidence_dir)

        # Components
        self.text_index = TextIndex()
        self.dense_retriever = DenseTextRetriever(random_state=self.random_seed)
        self.visual_retriever = VisualRetriever()
        self.fusion = MultimodalFusion(alpha_text=self.alpha_text)
        self.reranker = CrossModalReranker()
        self.region_retriever = RegionRetriever()

        self.pages: List[DocumentPageRecord] = []
        self.pages_map: Dict[int, DocumentPageRecord] = {}

    def index_document(self, pages: List[DocumentPageRecord]) -> None:
        """
        Build all sub-indices over the document pages.
        """
        self.pages = list(pages)
        self.pages_map = {p.page_number: p for p in self.pages}

        self.text_index.build(self.pages)
        self.dense_retriever.build(self.pages)
        self.visual_retriever.build(self.pages)

    def retrieve(
        self,
        query: RetrievalQuery,
        method: str = "B6-5",
        top_k: int = 3,
        top_m: int = 3,
        dataset_name: str = "synthetic_multipage"
    ) -> EvidencePackage:
        """
        Execute document retrieval for the given query using the specified baseline method.
        """
        t0 = time.perf_counter()
        total_pages = len(self.pages)
        if total_pages == 0:
            raise ValueError("Cannot retrieve from an empty document index")

        selected_pages: List[PageRetrievalResult] = []
        selected_regions: List[RegionRetrievalResult] = []

        if method == "B6-0":
            # B6-0: Random Page Retrieval
            rng = random.Random(self.random_seed + abs(hash(query.query_id)) % 10000)
            page_numbers = [p.page_number for p in self.pages]
            sampled_pages = rng.sample(page_numbers, min(top_k, total_pages))
            for rank, p_num in enumerate(sampled_pages, start=1):
                selected_pages.append(
                    PageRetrievalResult(
                        page_number=p_num,
                        score=round(1.0 / rank, 4),
                        text_score=0.0,
                        visual_score=0.0,
                        rank=rank,
                        metadata={"method": "random"}
                    )
                )

        elif method == "B6-1":
            # B6-1: BM25 Lexical Text Retrieval
            selected_pages = self.text_index.search(query.query_text, top_k=top_k)

        elif method == "B6-2":
            # B6-2: Dense Text Retrieval
            selected_pages = self.dense_retriever.search(query.query_text, top_k=top_k)

        elif method == "B6-3":
            # B6-3: Visual Feature Retrieval
            selected_pages = self.visual_retriever.search_by_text_concept(query.query_text, top_k=top_k)

        elif method == "B6-4":
            # B6-4: Multimodal Hybrid Retrieval (Text + Visual fusion)
            text_candidates = self.text_index.search(query.query_text, top_k=total_pages)
            visual_candidates = self.visual_retriever.search_by_text_concept(query.query_text, top_k=total_pages)
            selected_pages = self.fusion.fuse(text_candidates, visual_candidates, top_k=top_k)

        elif method == "B6-5":
            # B6-5: Proposed Hierarchical Multimodal Retrieval
            # Step 1: Coarse multimodal fusion over all pages
            text_candidates = self.text_index.search(query.query_text, top_k=total_pages)
            visual_candidates = self.visual_retriever.search_by_text_concept(query.query_text, top_k=total_pages)
            coarse_candidates = self.fusion.fuse(text_candidates, visual_candidates, top_k=max(top_k, 5))

            # Step 2: Cross-modal reranker refining down to top_k
            selected_pages = self.reranker.rerank(coarse_candidates, self.pages_map, query, top_m=top_k)

            # Step 3: Fine region retrieval within the selected top_k pages
            candidate_page_records = [self.pages_map[p.page_number] for p in selected_pages if p.page_number in self.pages_map]
            selected_regions = self.region_retriever.retrieve_regions(candidate_page_records, query, top_m=top_m)

        else:
            raise ValueError(f"Unsupported retrieval method: {method}")

        elapsed_ms = (time.perf_counter() - t0) * 1000.0

        provenance = create_retrieval_provenance(
            dataset=dataset_name,
            method=method,
            document_id=query.document_id,
            query_id=query.query_id,
            seed=self.random_seed,
            config_dict={"alpha_text": self.alpha_text, "top_k": top_k, "top_m": top_m},
            document_content=f"{query.document_id}_{total_pages}",
            query_content=query.query_text
        )
        provenance["latency_ms"] = round(elapsed_ms, 3)

        evidence_pkg = self.evidence_builder.build_package(
            document_id=query.document_id,
            query=query,
            retrieval_method=method,
            total_document_pages=total_pages,
            selected_pages=selected_pages,
            selected_regions=selected_regions,
            provenance=provenance,
            top_k=top_k,
            top_m=top_m
        )

        return evidence_pkg
