"""
Phase 7 End-to-End Smoke Test Script.
Validates that all 6 baselines (B7-0 through B7-5) run successfully,
generate valid Phase7EvidencePackage artifacts, and compute metrics.
"""

import os
import sys
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.evidence.pipeline import EvidenceGroundingPipeline
from src.evidence.baselines import BASELINE_MAP
from src.evidence.schema import Phase7EvidencePackage


def run_smoke_test():
    print("=== Starting Phase 7 End-to-End Smoke Test ===")
    manifest_path = "experiments/phase6/indexes/corpus_manifest.json"
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    test_docs = {d["document_id"]: d for d in manifest["documents"] if d["split"] == "test"}
    test_queries = [q for q in manifest["queries"] if q["document_id"] in test_docs]

    assert len(test_docs) > 0, "No test documents found in manifest"
    assert len(test_queries) > 0, "No test queries found in manifest"

    sample_query = test_queries[0]
    doc_id = sample_query["document_id"]
    doc_meta = test_docs[doc_id]

    with open(doc_meta["index_path"], "r", encoding="utf-8") as f:
        doc_data = json.load(f)

    # Prepare candidate pages and regions
    selected_pages = []
    selected_regions = []
    gt_bboxes = []

    for p in doc_data["pages"]:
        if p["page_number"] in sample_query["ground_truth_pages"]:
            selected_pages.append({
                "page_number": p["page_number"],
                "score": 0.95,
                "clean_text": p["clean_text"]
            })
            for r in p["regions"]:
                if r["region_id"] in sample_query["ground_truth_regions"]:
                    selected_regions.append({
                        "region_id": r["region_id"],
                        "page_number": p["page_number"],
                        "bbox": tuple(r["bbox"]),
                        "text_content": r["text_content"],
                        "score": 0.98,
                        "source_type": r.get("region_type", "table")
                    })
                    gt_bboxes.append(tuple(r["bbox"]))

    assert len(selected_regions) > 0, "Failed to locate target region for smoke test"

    target_text = selected_regions[0]["text_content"]
    # Answer derived from target text (e.g. "$48.7M" or content tokens)
    candidate_answer = target_text.split(":")[-1].strip() if ":" in target_text else target_text

    pipeline = EvidenceGroundingPipeline()
    smoke_dir = "experiments/phase7/smoke"
    os.makedirs(smoke_dir, exist_ok=True)

    print(f"Document: {doc_id} | Query: {sample_query['query_id']}")
    print(f"Target text: {target_text} | Candidate answer: {candidate_answer}")

    for b_id in BASELINE_MAP.keys():
        print(f"Running baseline {b_id} ({BASELINE_MAP[b_id]['name']})...")
        pkg = pipeline.process(
            document_id=doc_id,
            query_id=sample_query["query_id"],
            query_text=sample_query["query_text"],
            answer_text=candidate_answer,
            selected_pages=selected_pages,
            selected_regions=selected_regions,
            baseline_id=b_id,
            dataset="synthetic_multipage",
            condition=doc_meta.get("degradation_level", "clean"),
            seed=42,
            ground_truth_bboxes=gt_bboxes
        )

        assert isinstance(pkg, Phase7EvidencePackage)
        assert pkg.package_hash != ""
        assert pkg.grounding_result is not None
        assert pkg.support_result is not None

        out_path = os.path.join(smoke_dir, f"smoke_{b_id}.json")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(pkg.model_dump_json(indent=2))

        print(f"  -> Status: {pkg.grounding_result.grounding_status} | "
              f"Support: {pkg.support_result.support_status} | "
              f"Score: {pkg.grounding_result.grounding_score:.3f} | "
              f"Citations: {len(pkg.citations)}")

    print("\n=== Phase 7 Smoke Test PASSED Successfully! ===")


if __name__ == "__main__":
    run_smoke_test()
