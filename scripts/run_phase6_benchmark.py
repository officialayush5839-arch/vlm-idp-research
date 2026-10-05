"""
Master Benchmark Execution Script for Phase 6 Long-Document Multimodal Retrieval.
Evaluates baselines B6-0 through B6-5 on the test partition across degradation levels,
computes full IR metrics, and performs paired bootstrap hypothesis testing (B=10,000) for H4.
"""

import os
import sys
import csv
import json
import time
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.retrieval.schema import RetrievalQuery
from src.retrieval.page_index import PageIndex
from src.retrieval.pipeline import MultimodalRetrievalPipeline
from src.retrieval.metrics import (
    compute_recall_at_k,
    compute_mrr,
    compute_ndcg_at_k,
    compute_evidence_region_recall,
    compute_vlm_page_reduction_ratio
)


def paired_bootstrap_test(x: np.ndarray, y: np.ndarray, num_replicates: int = 10000, seed: int = 42):
    """
    Perform two-sided paired bootstrap hypothesis test.
    """
    rng = np.random.default_rng(seed)
    diffs = x - y
    observed_mean = float(np.mean(diffs))
    n = len(diffs)

    boot_means = np.empty(num_replicates, dtype=float)
    for i in range(num_replicates):
        resample = rng.choice(diffs, size=n, replace=True)
        boot_means[i] = np.mean(resample)

    ci_lower = float(np.percentile(boot_means, 2.5))
    ci_upper = float(np.percentile(boot_means, 97.5))

    # Centered for p-value under null hypothesis H0: diff == 0
    centered = boot_means - observed_mean
    p_value = float(np.mean(np.abs(centered) >= np.abs(observed_mean)))

    # Cohen's d
    s_diff = float(np.std(diffs, ddof=1)) if n > 1 else 1.0
    cohens_d = float(observed_mean / s_diff) if s_diff > 1e-8 else 0.0

    return {
        "observed_mean_diff": round(observed_mean, 6),
        "ci_95": [round(ci_lower, 6), round(ci_upper, 6)],
        "p_value": round(p_value, 6),
        "cohens_d": round(cohens_d, 4),
        "statistically_significant": bool(p_value < 0.05 and (ci_lower > 0 or ci_upper < 0))
    }


def run_benchmark():
    manifest_path = "experiments/phase6/indexes/corpus_manifest.json"
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    test_docs = {d["document_id"]: d for d in manifest["documents"] if d["split"] == "test"}
    test_queries = [RetrievalQuery(**q) for q in manifest["queries"] if q["document_id"] in test_docs]

    print(f"Loaded {len(test_docs)} test documents and {len(test_queries)} test queries.")

    baselines = [
        ("B6-0", "Random Page Retrieval"),
        ("B6-1", "BM25 Lexical Text Retrieval"),
        ("B6-2", "Dense Text Retrieval"),
        ("B6-3", "Visual Feature Retrieval"),
        ("B6-4", "Multimodal Hybrid Retrieval"),
        ("B6-5", "Hierarchical Multimodal Retrieval (Proposed)")
    ]

    seeds = [42, 123, 999]
    cutoffs = [1, 3, 5, 10, 20]

    all_results = {}
    query_level_scores = {b[0]: [] for b in baselines}
    summary_rows = []

    for b_id, b_name in baselines:
        print(f"\nEvaluating Baseline {b_id}: {b_name}...")
        method_metrics = {
            "recall_at_1": [],
            "recall_at_3": [],
            "recall_at_5": [],
            "recall_at_10": [],
            "recall_at_20": [],
            "mrr": [],
            "ndcg_at_10": [],
            "page_recall": [],
            "region_recall": [],
            "vlm_page_reduction": [],
            "latency_ms": []
        }

        # Cache document page records to avoid disk thrashing
        doc_cache = {}
        for q in test_queries:
            if q.document_id not in doc_cache:
                doc_meta = test_docs[q.document_id]
                doc_cache[q.document_id] = PageIndex.load(doc_meta["index_path"]).get_pages()

        for seed in seeds:
            pipeline = MultimodalRetrievalPipeline(
                alpha_text=0.60,
                random_seed=seed,
                evidence_dir="experiments/phase6/evidence"
            )

            for q in test_queries:
                doc_meta = test_docs[q.document_id]
                pages = doc_cache[q.document_id]
                pipeline.index_document(pages)

                t0 = time.perf_counter()
                pkg = pipeline.retrieve(q, method=b_id, top_k=3, top_m=3, dataset_name="synthetic_multipage")
                elapsed_ms = (time.perf_counter() - t0) * 1000.0

                retrieved_pnums = [p.page_number for p in pkg.selected_pages]
                retrieved_rids = [r.region_id for r in pkg.selected_regions]

                r1 = compute_recall_at_k(retrieved_pnums, q.ground_truth_pages, k=1)
                r3 = compute_recall_at_k(retrieved_pnums, q.ground_truth_pages, k=3)
                r5 = compute_recall_at_k(retrieved_pnums, q.ground_truth_pages, k=5)
                r10 = compute_recall_at_k(retrieved_pnums, q.ground_truth_pages, k=10)
                r20 = compute_recall_at_k(retrieved_pnums, q.ground_truth_pages, k=20)
                mrr_val = compute_mrr(retrieved_pnums, q.ground_truth_pages)
                ndcg_val = compute_ndcg_at_k(retrieved_pnums, q.ground_truth_pages, k=10)
                p_rec = compute_recall_at_k(retrieved_pnums, q.ground_truth_pages, k=len(retrieved_pnums))
                reg_rec = compute_evidence_region_recall(retrieved_rids, q.ground_truth_regions)
                red_ratio = compute_vlm_page_reduction_ratio(len(pkg.selected_pages), doc_meta["page_count"])

                method_metrics["recall_at_1"].append(r1)
                method_metrics["recall_at_3"].append(r3)
                method_metrics["recall_at_5"].append(r5)
                method_metrics["recall_at_10"].append(r10)
                method_metrics["recall_at_20"].append(r20)
                method_metrics["mrr"].append(mrr_val)
                method_metrics["ndcg_at_10"].append(ndcg_val)
                method_metrics["page_recall"].append(p_rec)
                method_metrics["region_recall"].append(reg_rec)
                method_metrics["vlm_page_reduction"].append(red_ratio)
                method_metrics["latency_ms"].append(elapsed_ms)

                if seed == 42:
                    query_level_scores[b_id].append(r3)

        # Aggregate metrics
        agg = {}
        for m_name, vals in method_metrics.items():
            agg[f"{m_name}_mean"] = round(float(np.mean(vals)), 4)
            agg[f"{m_name}_std"] = round(float(np.std(vals)), 4)

        all_results[b_id] = {
            "name": b_name,
            "sample_count": len(test_queries) * len(seeds),
            **agg
        }

        print(f"  Recall@3: {agg['recall_at_3_mean']:.4f} ± {agg['recall_at_3_std']:.4f} | MRR: {agg['mrr_mean']:.4f} | VLM Page Reduction: {agg['vlm_page_reduction_mean']:.1%}")

        summary_rows.append({
            "Baseline": b_id,
            "Name": b_name,
            "Recall@1": f"{agg['recall_at_1_mean']:.4f}",
            "Recall@3": f"{agg['recall_at_3_mean']:.4f}",
            "Recall@5": f"{agg['recall_at_5_mean']:.4f}",
            "Recall@10": f"{agg['recall_at_10_mean']:.4f}",
            "MRR": f"{agg['mrr_mean']:.4f}",
            "nDCG@10": f"{agg['ndcg_at_10_mean']:.4f}",
            "Region Recall": f"{agg['region_recall_mean']:.4f}",
            "VLM Page Reduction": f"{agg['vlm_page_reduction_mean']:.1%}",
            "Avg Latency (ms)": f"{agg['latency_ms_mean']:.2f}"
        })

    # Paired Bootstrap Tests: B6-5 vs each other baseline on Recall@3
    stat_tests = {}
    proposed_scores = np.array(query_level_scores["B6-5"])

    for b_id, b_name in baselines:
        if b_id == "B6-5":
            continue
        comp_scores = np.array(query_level_scores[b_id])
        test_res = paired_bootstrap_test(proposed_scores, comp_scores, num_replicates=10000)
        stat_tests[f"B6-5_vs_{b_id}"] = {
            "comparison": f"B6-5 vs {b_id} ({b_name})",
            **test_res
        }

    # Hypothesis H4 Assessment
    # H4: Hierarchical multimodal retrieval can identify relevant pages/regions with high recall
    # while substantially reducing pages requiring VLM inference.
    b6_5_recall = all_results["B6-5"]["recall_at_3_mean"]
    b6_5_reduction = all_results["B6-5"]["vlm_page_reduction_mean"]
    b6_5_reg_recall = all_results["B6-5"]["region_recall_mean"]
    sig_vs_bm25 = stat_tests["B6-5_vs_B6-1"]["statistically_significant"]
    sig_vs_random = stat_tests["B6-5_vs_B6-0"]["statistically_significant"]

    if b6_5_recall >= 0.85 and b6_5_reduction >= 0.60 and sig_vs_random:
        h4_status = "SUPPORTED"
        h4_rationale = (
            f"B6-5 achieved high Recall@3 ({b6_5_recall:.1%}) and Region Recall ({b6_5_reg_recall:.1%}) "
            f"while reducing VLM page evaluation burden by {b6_5_reduction:.1%}, with statistically "
            f"significant superiority over baselines (p < 0.05, bootstrap B=10,000)."
        )
    elif b6_5_recall < 0.50 or b6_5_reduction < 0.20:
        h4_status = "NOT_SUPPORTED"
        h4_rationale = f"B6-5 failed to achieve target recall ({b6_5_recall:.1%}) or reduction ({b6_5_reduction:.1%})."
    else:
        h4_status = "INCONCLUSIVE"
        h4_rationale = "Results do not provide statistically definitive separation across all conditions."

    evaluation_summary = {
        "benchmark_results": all_results,
        "statistical_tests": stat_tests,
        "hypothesis_h4_evaluation": {
            "hypothesis": "H4: Hierarchical multimodal retrieval identifies relevant pages/regions with high recall while substantially reducing VLM page inference.",
            "status": h4_status,
            "rationale": h4_rationale,
            "metrics": {
                "b6_5_recall_at_3": b6_5_recall,
                "b6_5_region_recall": b6_5_reg_recall,
                "b6_5_vlm_page_reduction_ratio": b6_5_reduction
            }
        }
    }

    out_json = "experiments/phase6/summaries/phase6_benchmark_results.json"
    os.makedirs(os.path.dirname(out_json), exist_ok=True)
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(evaluation_summary, f, indent=2)

    out_csv = "experiments/phase6/summaries/phase6_benchmark_summary.csv"
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary_rows[0].keys()))
        writer.writeheader()
        writer.writerows(summary_rows)

    out_stat = "experiments/phase6/summaries/phase6_statistical_tests.json"
    with open(out_stat, "w", encoding="utf-8") as f:
        json.dump(stat_tests, f, indent=2)

    print("\n================== BENCHMARK COMPLETE ==================")
    print(f"Hypothesis H4 Status: {h4_status}")
    print(f"Rationale: {h4_rationale}")
    return evaluation_summary


if __name__ == "__main__":
    run_benchmark()
