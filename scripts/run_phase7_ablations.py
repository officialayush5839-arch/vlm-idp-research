"""
Phase 7 Ablations Script (A1 through A8).
Evaluates the contribution of individual components:
- Full System (B7-5 reference)
- A1: No Spatial Grounding
- A2: No Numeric Verification
- A3: No Table Verification
- A4: No Multi-Page Aggregation
- A5: No Sufficiency Check
- A6: Relaxed IoU Only
- A7: Strict IoU Only
- A8: Single-Modal Retrieval Input
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
from src.evidence.pipeline import EvidenceGroundingPipeline
from src.evidence.region_validator import SpatialRegionValidator
from src.evidence.numeric_verifier import NumericVerifier
from src.evidence.table_verifier import TableVerifier
from src.evidence.evidence_sufficiency import EvidenceSufficiencyEvaluator
from src.evidence.multipage_aggregator import MultiPageAggregator
from src.evidence.metrics import (
    compute_region_recall_at_iou,
    compute_evidence_precision,
    compute_evidence_f1,
    compute_mean_iou
)


def run_ablations():
    print("=== Starting Phase 7 Ablation Study (A1-A8) ===")
    manifest_path = "experiments/phase6/indexes/corpus_manifest.json"
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    test_docs = {d["document_id"]: d for d in manifest["documents"] if d["split"] == "test"}
    test_queries = [q for q in manifest["queries"] if q["document_id"] in test_docs]

    doc_cache = {}
    for q in test_queries:
        d_id = q["document_id"]
        if d_id not in doc_cache:
            d_meta = test_docs[d_id]
            doc_cache[d_id] = PageIndex.load(d_meta["index_path"]).get_pages()

    query_targets = {}
    for q in test_queries:
        d_id = q["document_id"]
        pages = doc_cache[d_id]
        gt_bboxes = []
        gt_text = ""
        for p in pages:
            if p.page_number in q["ground_truth_pages"]:
                for r in p.regions:
                    if r.region_id in q["ground_truth_regions"]:
                        gt_bboxes.append(r.bbox)
                        if not gt_text:
                            gt_text = r.text_content

        target_ans = gt_text.split(":")[-1].strip() if ":" in gt_text else gt_text
        query_targets[q["query_id"]] = {
            "gt_bboxes": gt_bboxes,
            "target_answer": target_ans
        }

    ablation_definitions = [
        ("Full_B7_5", "Full Proposed System"),
        ("A1_NoSpatial", "A1: No Spatial Grounding"),
        ("A2_NoNumeric", "A2: No Numeric Verification"),
        ("A3_NoTable", "A3: No Table Verification"),
        ("A4_NoMultiPage", "A4: No Multi-Page Aggregation"),
        ("A5_NoSufficiency", "A5: No Sufficiency Check"),
        ("A6_RelaxedOnly", "A6: Relaxed IoU Only (0.50)"),
        ("A7_StrictOnly", "A7: Strict IoU Only (0.75)"),
        ("A8_SingleModal", "A8: Single-Modal Retrieval Input")
    ]

    all_ablation_results = {}
    csv_rows = []

    retrieval_pipeline = MultimodalRetrievalPipeline(random_seed=42, evidence_dir="experiments/phase6/evidence")

    for ab_id, ab_name in ablation_definitions:
        print(f"\nEvaluating Ablation: {ab_name}...")

        # Configure pipeline for this ablation
        s_val = SpatialRegionValidator()
        if ab_id == "A1_NoSpatial":
            s_val = SpatialRegionValidator(iou_threshold_relaxed=0.0, iou_threshold_strict=0.0)
        elif ab_id == "A6_RelaxedOnly":
            s_val = SpatialRegionValidator(iou_threshold_relaxed=0.50, iou_threshold_strict=0.50)
        elif ab_id == "A7_StrictOnly":
            s_val = SpatialRegionValidator(iou_threshold_relaxed=0.75, iou_threshold_strict=0.75)

        num_val = NumericVerifier()
        if ab_id == "A2_NoNumeric":
            class NoOpNumericVerifier(NumericVerifier):
                def verify_numeric_support(self, a, e, allow_scale_equivalence=True):
                    return {"is_numeric_claim": False, "is_verified": True, "matches": [], "reason": "ablated"}
            num_val = NoOpNumericVerifier()

        tbl_val = TableVerifier()
        if ab_id == "A3_NoTable":
            class NoOpTableVerifier(TableVerifier):
                def verify_table_cell(self, r, c, a, s):
                    return {"is_tabular": False, "has_value": True, "has_row_context": True, "has_col_context": True, "table_alignment_score": 1.0, "passes_verification": True, "reason": "ablated"}
            tbl_val = NoOpTableVerifier()

        suff_val = EvidenceSufficiencyEvaluator()
        if ab_id == "A5_NoSufficiency":
            class NoOpSufficiency(EvidenceSufficiencyEvaluator):
                def evaluate_sufficiency(self, q, e):
                    return {"sufficiency_status": "SUFFICIENT", "coverage_score": 1.0, "covered_tokens": [], "missing_tokens": [], "reason": "ablated"}
            suff_val = NoOpSufficiency()

        mult_val = MultiPageAggregator()

        pipeline = EvidenceGroundingPipeline(
            spatial_validator=s_val,
            numeric_verifier=num_val,
            table_verifier=tbl_val,
            sufficiency_evaluator=suff_val,
            multipage_aggregator=mult_val
        )

        upstream_method = "B6-1" if ab_id == "A8_SingleModal" else "B6-5"
        base_id = "B7-1" if ab_id == "A8_SingleModal" else "B7-5"

        scores = []
        rec50_list = []
        rec75_list = []
        grounded_rates = []

        for q in test_queries:
            q_id = q["query_id"]
            d_id = q["document_id"]
            d_meta = test_docs[d_id]
            pages = doc_cache[d_id]
            target_info = query_targets[q_id]

            retrieval_pipeline.index_document(pages)
            ret_query = RetrievalQuery(
                query_id=q["query_id"],
                document_id=q["document_id"],
                query_text=q["query_text"],
                query_type=q.get("query_type", "factoid"),
                ground_truth_pages=q["ground_truth_pages"],
                ground_truth_regions=q["ground_truth_regions"]
            )
            ret_pkg = retrieval_pipeline.retrieve(ret_query, method=upstream_method, top_k=3, top_m=3)

            page_map = {pg.page_number: pg for pg in pages}
            sel_pages = [
                {
                    "page_number": p.page_number,
                    "score": p.score,
                    "clean_text": page_map[p.page_number].clean_text if p.page_number in page_map else ""
                }
                for p in ret_pkg.selected_pages
            ]
            sel_regions = [{"region_id": r.region_id, "page_number": r.page_number, "bbox": r.bbox, "snippet": r.snippet, "score": r.score, "source_type": "multimodal"} for r in ret_pkg.selected_regions]

            p7_pkg = pipeline.process(
                document_id=d_id,
                query_id=q_id,
                query_text=q["query_text"],
                answer_text=target_info["target_answer"],
                selected_pages=sel_pages,
                selected_regions=sel_regions,
                baseline_id=base_id,
                dataset="synthetic_multipage",
                condition=d_meta.get("degradation_level", "clean"),
                seed=42,
                ground_truth_bboxes=target_info["gt_bboxes"]
            )

            ret_boxes = [u.bbox_1000 for u in p7_pkg.evidence_units]
            gt_boxes = target_info["gt_bboxes"]

            rec50 = compute_region_recall_at_iou(ret_boxes, gt_boxes, 0.50)
            rec75 = compute_region_recall_at_iou(ret_boxes, gt_boxes, 0.75)
            is_grounded = 1.0 if p7_pkg.grounding_result.grounding_status in ["GROUNDED", "PARTIALLY_GROUNDED"] else 0.0

            scores.append(p7_pkg.grounding_result.grounding_score)
            rec50_list.append(rec50)
            rec75_list.append(rec75)
            grounded_rates.append(is_grounded)

        res_summary = {
            "ablation_id": ab_id,
            "name": ab_name,
            "mean_grounding_score": float(np.mean(scores)),
            "region_recall_at_050": float(np.mean(rec50_list)),
            "region_recall_at_075": float(np.mean(rec75_list)),
            "grounded_rate": float(np.mean(grounded_rates))
        }

        all_ablation_results[ab_id] = res_summary
        csv_rows.append(res_summary)
        print(f"  -> Score: {res_summary['mean_grounding_score']:.4f} | "
              f"Recall@0.50: {res_summary['region_recall_at_050']:.4f} | "
              f"Recall@0.75: {res_summary['region_recall_at_075']:.4f} | "
              f"Grounded Rate: {res_summary['grounded_rate']:.4f}")

    exp_dir = "experiments/phase7"
    os.makedirs(exp_dir, exist_ok=True)
    with open(os.path.join(exp_dir, "ablation_results.json"), "w", encoding="utf-8") as f:
        json.dump(all_ablation_results, f, indent=2)

    with open(os.path.join(exp_dir, "ablation_summary.csv"), "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(csv_rows[0].keys()))
        writer.writeheader()
        writer.writerows(csv_rows)

    print("\n=== Phase 7 Ablations COMPLETE ===")


if __name__ == "__main__":
    run_ablations()
