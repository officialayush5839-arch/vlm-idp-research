"""
Validation Script for Phase 6.
Evaluates the validation partition (split == 'val') across various cutoffs K and alpha values,
verifying parameter calibration without touching the test split.
"""

import os
import sys
import json
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.retrieval.schema import RetrievalQuery
from src.retrieval.page_index import PageIndex
from src.retrieval.pipeline import MultimodalRetrievalPipeline
from src.retrieval.metrics import compute_recall_at_k, compute_mrr, compute_vlm_page_reduction_ratio


def run_validation():
    manifest_path = "experiments/phase6/indexes/corpus_manifest.json"
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    # Filter validation documents and queries
    val_docs = {d["document_id"]: d for d in manifest["documents"] if d["split"] == "val"}
    val_queries = [RetrievalQuery(**q) for q in manifest["queries"] if q["document_id"] in val_docs]

    print(f"Loaded {len(val_docs)} validation documents and {len(val_queries)} validation queries.")

    k_values = [1, 3, 5]
    alpha_values = [0.0, 0.40, 0.60, 0.80, 1.0]

    val_results = {"by_k": {}, "by_alpha": {}}

    # K sensitivity on val with default alpha=0.60
    for k in k_values:
        recalls = []
        mrrs = []
        reductions = []
        pipeline = MultimodalRetrievalPipeline(alpha_text=0.60, random_seed=42)

        for q in val_queries:
            doc_meta = val_docs[q.document_id]
            page_idx = PageIndex.load(doc_meta["index_path"])
            pipeline.index_document(page_idx.get_pages())

            pkg = pipeline.retrieve(q, method="B6-5", top_k=k, top_m=3)
            retrieved_pages = [p.page_number for p in pkg.selected_pages]

            r = compute_recall_at_k(retrieved_pages, q.ground_truth_pages, k=k)
            m = compute_mrr(retrieved_pages, q.ground_truth_pages)
            red = compute_vlm_page_reduction_ratio(len(pkg.selected_pages), doc_meta["page_count"])

            recalls.append(r)
            mrrs.append(m)
            reductions.append(red)

        val_results["by_k"][f"k_{k}"] = {
            "mean_recall": round(float(np.mean(recalls)), 4),
            "mean_mrr": round(float(np.mean(mrrs)), 4),
            "mean_page_reduction": round(float(np.mean(reductions)), 4)
        }

    # Alpha sensitivity on val at k=3
    for a in alpha_values:
        recalls = []
        mrrs = []
        pipeline = MultimodalRetrievalPipeline(alpha_text=a, random_seed=42)

        for q in val_queries:
            doc_meta = val_docs[q.document_id]
            page_idx = PageIndex.load(doc_meta["index_path"])
            pipeline.index_document(page_idx.get_pages())

            pkg = pipeline.retrieve(q, method="B6-5", top_k=3, top_m=3)
            retrieved_pages = [p.page_number for p in pkg.selected_pages]

            r = compute_recall_at_k(retrieved_pages, q.ground_truth_pages, k=3)
            m = compute_mrr(retrieved_pages, q.ground_truth_pages)

            recalls.append(r)
            mrrs.append(m)

        val_results["by_alpha"][f"alpha_{a:.2f}"] = {
            "mean_recall_at_3": round(float(np.mean(recalls)), 4),
            "mean_mrr": round(float(np.mean(mrrs)), 4)
        }

    out_file = "experiments/phase6/summaries/phase6_validation_results.json"
    os.makedirs(os.path.dirname(out_file), exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(val_results, f, indent=2)

    print("\n--- VALIDATION RESULTS ---")
    print(json.dumps(val_results, indent=2))
    return val_results


if __name__ == "__main__":
    run_validation()
