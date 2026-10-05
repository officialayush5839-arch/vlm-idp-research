"""
Phase 6 Ablation Studies Execution Script.
Executes all 8 defined retrieval ablations (A1 through A8), recording empirical deltas,
Recall@K metrics, and VLM page reduction ratios across conditions.
"""

import os
import sys
import json
import csv
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.retrieval.schema import RetrievalQuery
from src.retrieval.page_index import PageIndex
from src.retrieval.pipeline import MultimodalRetrievalPipeline
from src.retrieval.metrics import (
    compute_recall_at_k,
    compute_mrr,
    compute_evidence_region_recall,
    compute_vlm_page_reduction_ratio
)


def run_ablations():
    manifest_path = "experiments/phase6/indexes/corpus_manifest.json"
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    test_docs = {d["document_id"]: d for d in manifest["documents"] if d["split"] == "test"}
    test_queries = [RetrievalQuery(**q) for q in manifest["queries"] if q["document_id"] in test_docs]

    # Preload doc pages
    doc_cache = {}
    for q in test_queries:
        if q.document_id not in doc_cache:
            doc_meta = test_docs[q.document_id]
            doc_cache[q.document_id] = PageIndex.load(doc_meta["index_path"]).get_pages()

    ablations_data = {}

    # ----------------------------------------------------
    # A1: Modality Ablation (Text-only vs Visual-only vs Multimodal)
    # ----------------------------------------------------
    print("Running A1: Modality Ablation...")
    a1_results = {}
    for m_id, label in [("B6-1", "Text_Only_BM25"), ("B6-3", "Visual_Only"), ("B6-4", "Multimodal_Fusion"), ("B6-5", "Full_Hierarchical")]:
        recs, mrrs, reds = [], [], []
        pipe = MultimodalRetrievalPipeline(random_seed=42)
        for q in test_queries:
            doc_meta = test_docs[q.document_id]
            pipe.index_document(doc_cache[q.document_id])
            pkg = pipe.retrieve(q, method=m_id, top_k=3, top_m=3)
            pnums = [p.page_number for p in pkg.selected_pages]
            recs.append(compute_recall_at_k(pnums, q.ground_truth_pages, k=3))
            mrrs.append(compute_mrr(pnums, q.ground_truth_pages))
            reds.append(compute_vlm_page_reduction_ratio(len(pkg.selected_pages), doc_meta["page_count"]))
        a1_results[label] = {
            "mean_recall_at_3": round(float(np.mean(recs)), 4),
            "mean_mrr": round(float(np.mean(mrrs)), 4),
            "mean_page_reduction": round(float(np.mean(reds)), 4)
        }
    ablations_data["A1_Modality"] = a1_results

    # ----------------------------------------------------
    # A2: Top-K Cutoff Sensitivity
    # ----------------------------------------------------
    print("Running A2: Top-K Sensitivity...")
    a2_results = {}
    for k in [1, 3, 5, 10, 20]:
        recs, mrrs, reds = [], [], []
        pipe = MultimodalRetrievalPipeline(random_seed=42)
        for q in test_queries:
            doc_meta = test_docs[q.document_id]
            pipe.index_document(doc_cache[q.document_id])
            pkg = pipe.retrieve(q, method="B6-5", top_k=k, top_m=3)
            pnums = [p.page_number for p in pkg.selected_pages]
            recs.append(compute_recall_at_k(pnums, q.ground_truth_pages, k=k))
            mrrs.append(compute_mrr(pnums, q.ground_truth_pages))
            reds.append(compute_vlm_page_reduction_ratio(len(pkg.selected_pages), doc_meta["page_count"]))
        a2_results[f"K_{k}"] = {
            "mean_recall_at_k": round(float(np.mean(recs)), 4),
            "mean_mrr": round(float(np.mean(mrrs)), 4),
            "mean_page_reduction": round(float(np.mean(reds)), 4)
        }
    ablations_data["A2_TopK"] = a2_results

    # ----------------------------------------------------
    # A3: Fusion Weight Alpha Sensitivity
    # ----------------------------------------------------
    print("Running A3: Alpha Sensitivity...")
    a3_results = {}
    for alpha in [0.0, 0.20, 0.40, 0.60, 0.80, 1.0]:
        recs, mrrs = [], []
        pipe = MultimodalRetrievalPipeline(alpha_text=alpha, random_seed=42)
        for q in test_queries:
            pipe.index_document(doc_cache[q.document_id])
            pkg = pipe.retrieve(q, method="B6-4", top_k=3, top_m=3)
            pnums = [p.page_number for p in pkg.selected_pages]
            recs.append(compute_recall_at_k(pnums, q.ground_truth_pages, k=3))
            mrrs.append(compute_mrr(pnums, q.ground_truth_pages))
        a3_results[f"alpha_{alpha:.2f}"] = {
            "mean_recall_at_3": round(float(np.mean(recs)), 4),
            "mean_mrr": round(float(np.mean(mrrs)), 4)
        }
    ablations_data["A3_Alpha"] = a3_results

    # ----------------------------------------------------
    # A4: Cross-Modal Reranker Impact
    # ----------------------------------------------------
    print("Running A4: Cross-Modal Reranker Impact...")
    # B6-4 (No reranker) vs B6-5 (With reranker)
    a4_results = {
        "without_reranker": a1_results["Multimodal_Fusion"],
        "with_reranker": a1_results["Full_Hierarchical"],
        "delta_recall_at_3": round(a1_results["Full_Hierarchical"]["mean_recall_at_3"] - a1_results["Multimodal_Fusion"]["mean_recall_at_3"], 4),
        "delta_mrr": round(a1_results["Full_Hierarchical"]["mean_mrr"] - a1_results["Multimodal_Fusion"]["mean_mrr"], 4)
    }
    ablations_data["A4_Reranker"] = a4_results

    # ----------------------------------------------------
    # A5: Document Length Scaling
    # ----------------------------------------------------
    print("Running A5: Document Length Scaling...")
    a5_results = {}
    for length in [5, 10, 20, 50]:
        matching_q = [q for q in test_queries if test_docs[q.document_id]["page_count"] == length]
        if not matching_q:
            continue
        recs, reds = [], []
        pipe = MultimodalRetrievalPipeline(random_seed=42)
        for q in matching_q:
            doc_meta = test_docs[q.document_id]
            pipe.index_document(doc_cache[q.document_id])
            pkg = pipe.retrieve(q, method="B6-5", top_k=3, top_m=3)
            pnums = [p.page_number for p in pkg.selected_pages]
            recs.append(compute_recall_at_k(pnums, q.ground_truth_pages, k=3))
            reds.append(compute_vlm_page_reduction_ratio(len(pkg.selected_pages), doc_meta["page_count"]))
        a5_results[f"length_{length}p"] = {
            "query_count": len(matching_q),
            "mean_recall_at_3": round(float(np.mean(recs)), 4),
            "mean_page_reduction": round(float(np.mean(reds)), 4)
        }
    ablations_data["A5_DocLength"] = a5_results

    # ----------------------------------------------------
    # A6: Visual Degradation Impact
    # ----------------------------------------------------
    print("Running A6: Visual Degradation Robustness...")
    a6_results = {}
    for deg in ["clean", "mild", "moderate", "severe"]:
        matching_q = [q for q in test_queries if test_docs[q.document_id]["degradation_level"] == deg]
        if not matching_q:
            continue
        b6_1_recs, b6_5_recs = [], []
        pipe = MultimodalRetrievalPipeline(random_seed=42)
        for q in matching_q:
            pipe.index_document(doc_cache[q.document_id])
            pkg1 = pipe.retrieve(q, method="B6-1", top_k=3)
            pkg5 = pipe.retrieve(q, method="B6-5", top_k=3)
            b6_1_recs.append(compute_recall_at_k([p.page_number for p in pkg1.selected_pages], q.ground_truth_pages, k=3))
            b6_5_recs.append(compute_recall_at_k([p.page_number for p in pkg5.selected_pages], q.ground_truth_pages, k=3))
        a6_results[deg] = {
            "bm25_recall_at_3": round(float(np.mean(b6_1_recs)), 4),
            "b6_5_recall_at_3": round(float(np.mean(b6_5_recs)), 4),
            "delta_advantage": round(float(np.mean(b6_5_recs) - np.mean(b6_1_recs)), 4)
        }
    ablations_data["A6_Degradation"] = a6_results

    # ----------------------------------------------------
    # A7: Region-Level Granularity vs Page-Level Only
    # ----------------------------------------------------
    print("Running A7: Region Granularity...")
    reg_recalls = []
    pipe = MultimodalRetrievalPipeline(random_seed=42)
    for q in test_queries:
        pipe.index_document(doc_cache[q.document_id])
        pkg = pipe.retrieve(q, method="B6-5", top_k=3, top_m=3)
        rids = [r.region_id for r in pkg.selected_regions]
        reg_recalls.append(compute_evidence_region_recall(rids, q.ground_truth_regions))
    a7_results = {
        "page_recall_at_3": a1_results["Full_Hierarchical"]["mean_recall_at_3"],
        "region_evidence_recall": round(float(np.mean(reg_recalls)), 4)
    }
    ablations_data["A7_RegionGranularity"] = a7_results

    # ----------------------------------------------------
    # A8: Query Type Specificity
    # ----------------------------------------------------
    print("Running A8: Query Type Specificity...")
    a8_results = {}
    for qtype in ["table", "factoid"]:
        matching_q = [q for q in test_queries if q.query_type == qtype]
        if not matching_q:
            continue
        recs = []
        pipe = MultimodalRetrievalPipeline(random_seed=42)
        for q in matching_q:
            pipe.index_document(doc_cache[q.document_id])
            pkg = pipe.retrieve(q, method="B6-5", top_k=3, top_m=3)
            pnums = [p.page_number for p in pkg.selected_pages]
            recs.append(compute_recall_at_k(pnums, q.ground_truth_pages, k=3))
        a8_results[qtype] = {
            "query_count": len(matching_q),
            "mean_recall_at_3": round(float(np.mean(recs)), 4)
        }
    ablations_data["A8_QueryTypes"] = a8_results

    out_json = "experiments/phase6/ablations/phase6_ablation_results.json"
    os.makedirs(os.path.dirname(out_json), exist_ok=True)
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(ablations_data, f, indent=2)

    print("\nAll 8 Phase 6 Ablations executed successfully!")
    return ablations_data


if __name__ == "__main__":
    run_ablations()
