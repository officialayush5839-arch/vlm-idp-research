"""
Phase 6 Long-Document Multimodal Retrieval Package.
"""

from src.retrieval.schema import (
    DocumentRegionRecord,
    DocumentPageRecord,
    RetrievalQuery,
    PageRetrievalResult,
    RegionRetrievalResult,
    EvidencePackage,
    RetrievalMetricsResult,
)
from src.retrieval.bm25 import BM25Okapi, simple_tokenize
from src.retrieval.text_index import TextIndex
from src.retrieval.dense_retrieval import DenseTextRetriever
from src.retrieval.visual_index import VisualRetriever
from src.retrieval.fusion import MultimodalFusion, normalize_scores
from src.retrieval.reranker import CrossModalReranker
from src.retrieval.region import RegionRetriever
from src.retrieval.evidence import EvidencePackageBuilder
from src.retrieval.provenance import (
    generate_phase6_run_id,
    create_retrieval_provenance,
    compute_sha256,
    get_git_commit,
)
from src.retrieval.metrics import (
    compute_recall_at_k,
    compute_hit_at_k,
    compute_mrr,
    compute_ndcg_at_k,
    compute_evidence_region_recall,
    compute_vlm_page_reduction_ratio,
)
from src.retrieval.pipeline import MultimodalRetrievalPipeline

__all__ = [
    "DocumentRegionRecord",
    "DocumentPageRecord",
    "RetrievalQuery",
    "PageRetrievalResult",
    "RegionRetrievalResult",
    "EvidencePackage",
    "RetrievalMetricsResult",
    "BM25Okapi",
    "simple_tokenize",
    "TextIndex",
    "DenseTextRetriever",
    "VisualRetriever",
    "MultimodalFusion",
    "normalize_scores",
    "CrossModalReranker",
    "RegionRetriever",
    "EvidencePackageBuilder",
    "generate_phase6_run_id",
    "create_retrieval_provenance",
    "compute_sha256",
    "get_git_commit",
    "compute_recall_at_k",
    "compute_hit_at_k",
    "compute_mrr",
    "compute_ndcg_at_k",
    "compute_evidence_region_recall",
    "compute_vlm_page_reduction_ratio",
    "MultimodalRetrievalPipeline",
]
