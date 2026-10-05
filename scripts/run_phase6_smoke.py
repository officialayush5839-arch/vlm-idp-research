"""
Smoke Test for Phase 6 Long-Document Multimodal Retrieval.
Runs end-to-end execution of all retrieval baselines (B6-0 to B6-5)
over a multi-page document, verifies EvidencePackage integrity and serialization.
"""

import os
import sys
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.retrieval.schema import RetrievalQuery
from src.retrieval.page_index import PageIndex
from src.retrieval.pipeline import MultimodalRetrievalPipeline


def run_smoke_test():
    manifest_path = "experiments/phase6/indexes/corpus_manifest.json"
    if not os.path.exists(manifest_path):
        raise FileNotFoundError(f"Manifest not found: {manifest_path}. Run scripts/run_phase6_index.py first.")

    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    first_doc_meta = manifest["documents"][0]
    first_query_data = manifest["queries"][0]

    doc_id = first_doc_meta["document_id"]
    index_file = first_doc_meta["index_path"]
    query = RetrievalQuery(**first_query_data)

    print(f"Loading document {doc_id} with {first_doc_meta['page_count']} pages...")
    page_idx = PageIndex.load(index_file)
    pages = page_idx.get_pages()

    pipeline = MultimodalRetrievalPipeline(random_seed=42, evidence_dir="experiments/phase6/evidence")
    pipeline.index_document(pages)

    baselines = ["B6-0", "B6-1", "B6-2", "B6-3", "B6-4", "B6-5"]
    packages = {}

    for b in baselines:
        print(f"Testing baseline {b}...")
        pkg = pipeline.retrieve(query, method=b, top_k=3, top_m=3, dataset_name="synthetic_multipage")
        saved_path = pipeline.evidence_builder.save_package(pkg)
        assert os.path.exists(saved_path), f"Failed to save package for {b}"
        packages[b] = {
            "method": b,
            "selected_pages": [p.page_number for p in pkg.selected_pages],
            "vlm_page_reduction_ratio": pkg.vlm_page_reduction_ratio,
            "selected_regions_count": len(pkg.selected_regions),
            "package_path": saved_path
        }
        print(f"  [{b}] Selected pages: {packages[b]['selected_pages']} | Page reduction: {pkg.vlm_page_reduction_ratio:.1%}")

    print("\n--- SMOKE TEST SUMMARY ---")
    print(json.dumps(packages, indent=2))
    print("\nAll 6 baselines successfully generated valid, persisted EvidencePackages!")
    return packages


if __name__ == "__main__":
    run_smoke_test()
