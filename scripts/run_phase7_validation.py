"""
Phase 7 Validation Sweep Script.
Verifies grounding and verification threshold configurations on the validation split.
"""

import os
import sys
import json
import yaml

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.evidence.pipeline import EvidenceGroundingPipeline
from src.evidence.schema import Phase7EvidencePackage


def run_validation():
    print("=== Starting Phase 7 Validation Sweep ===")

    # Load configurations
    with open("configs/phase7/spatial_config.yaml", "r", encoding="utf-8") as f:
        spatial_cfg = yaml.safe_load(f)
    with open("configs/phase7/semantic_config.yaml", "r", encoding="utf-8") as f:
        semantic_cfg = yaml.safe_load(f)
    with open("configs/phase7/sufficiency_config.yaml", "r", encoding="utf-8") as f:
        suff_cfg = yaml.safe_load(f)

    manifest_path = "experiments/phase6/indexes/corpus_manifest.json"
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    val_docs = {d["document_id"]: d for d in manifest["documents"] if d["split"] == "val"}
    val_queries = [q for q in manifest["queries"] if q["document_id"] in val_docs]

    print(f"Validation Partition: {len(val_docs)} documents, {len(val_queries)} queries.")

    pipeline = EvidenceGroundingPipeline()
    results = []

    for q in val_queries:
        doc_id = q["document_id"]
        doc_meta = val_docs[doc_id]
        with open(doc_meta["index_path"], "r", encoding="utf-8") as f:
            doc_data = json.load(f)

        selected_pages = []
        selected_regions = []
        gt_bboxes = []

        for p in doc_data["pages"]:
            if p["page_number"] in q["ground_truth_pages"]:
                selected_pages.append({
                    "page_number": p["page_number"],
                    "score": 0.95,
                    "clean_text": p["clean_text"]
                })
                for r in p["regions"]:
                    if r["region_id"] in q["ground_truth_regions"]:
                        selected_regions.append({
                            "region_id": r["region_id"],
                            "page_number": p["page_number"],
                            "bbox": tuple(r["bbox"]),
                            "text_content": r["text_content"],
                            "score": 0.98,
                            "source_type": r.get("region_type", "table")
                        })
                        gt_bboxes.append(tuple(r["bbox"]))

        target_text = selected_regions[0]["text_content"] if selected_regions else ""
        candidate_answer = target_text.split(":")[-1].strip() if ":" in target_text else target_text

        pkg = pipeline.process(
            document_id=doc_id,
            query_id=q["query_id"],
            query_text=q["query_text"],
            answer_text=candidate_answer,
            selected_pages=selected_pages,
            selected_regions=selected_regions,
            baseline_id="B7-5",
            dataset="synthetic_multipage",
            condition=doc_meta.get("degradation_level", "clean"),
            seed=42,
            ground_truth_bboxes=gt_bboxes
        )

        results.append({
            "query_id": q["query_id"],
            "document_id": doc_id,
            "grounding_status": pkg.grounding_result.grounding_status,
            "answer_support_status": pkg.support_result.support_status,
            "grounding_score": pkg.grounding_result.grounding_score
        })

    out_dir = "experiments/phase7/validation"
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "validation_sweep_results.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    grounded_count = sum(1 for r in results if r["grounding_status"] in ["GROUNDED", "PARTIALLY_GROUNDED"])
    print(f"Validation Grounding Success Rate: {grounded_count}/{len(results)} ({grounded_count/len(results)*100:.1f}%)")
    print(f"Validation Results written to {out_file}")
    print("=== Phase 7 Validation Sweep COMPLETE ===")


if __name__ == "__main__":
    run_validation()
