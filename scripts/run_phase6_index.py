"""
Corpus Index Builder for Phase 6 Long-Document Multimodal Retrieval.
Constructs realistic multi-page document collections with layout structures,
sub-page regions, and degradation levels across train, val, and test splits.
"""

import os
import sys
import json
import random
from typing import List, Dict, Any

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.retrieval.schema import DocumentPageRecord, DocumentRegionRecord, RetrievalQuery
from src.retrieval.page_index import PageIndex


def generate_synthetic_multipage_corpus(
    output_dir: str = "experiments/phase6/indexes",
    num_docs: int = 50,
    seed: int = 42
) -> Dict[str, Any]:
    """
    Generate multi-page documents with realistic corporate, technical, and financial structures.
    """
    os.makedirs(output_dir, exist_ok=True)
    rng = random.Random(seed)

    doc_lengths = [5, 10, 20, 50]
    degradation_levels = ["clean", "mild", "moderate", "severe"]
    splits = ["train"] * 10 + ["val"] * 15 + ["test"] * 25

    vocabulary_topics = {
        "finance": ["revenue", "operating profit", "ebitda", "balance sheet", "liabilities", "cash flow", "audit", "fiscal 2024", "dividend"],
        "governance": ["board of directors", "committee", "ethics policy", "shareholders", "executive compensation", "voting rights"],
        "operations": ["supply chain", "logistics", "procurement", "inventory turnover", "manufacturing facilities", "distribution network"],
        "technology": ["infrastructure", "cloud migration", "cybersecurity", "neural network", "vlm processing", "data privacy", "encryption"],
        "legal": ["compliance", "regulatory filings", "intellectual property", "patents", "litigation risks", "statutory requirements"]
    }

    manifest = {"documents": [], "queries": []}

    for d_idx in range(num_docs):
        doc_id = f"doc_mp_{d_idx + 1:03d}"
        doc_len = doc_lengths[d_idx % len(doc_lengths)]
        deg_level = degradation_levels[d_idx % len(degradation_levels)]
        split = splits[d_idx % len(splits)]

        page_index = PageIndex(document_id=doc_id)

        # Assign a target evidence page and topic
        target_page_num = rng.randint(2, doc_len)
        target_topic = list(vocabulary_topics.keys())[d_idx % len(vocabulary_topics)]
        target_terms = vocabulary_topics[target_topic]

        for p_num in range(1, doc_len + 1):
            if p_num == 1:
                # Cover page
                p_text = f"Annual Comprehensive Report: Document {doc_id}. Table of Contents, Executive Overview, Directory."
                regions = [
                    DocumentRegionRecord(
                        region_id=f"{doc_id}_p1_hdr",
                        page_number=1,
                        bbox=(50, 50, 950, 150),
                        region_type="header",
                        text_content="ANNUAL CORPORATE REPORT",
                        confidence=0.98
                    )
                ]
            elif p_num == target_page_num:
                # Evidence page
                p_text = f"Detailed Analysis of {target_topic.capitalize()}: " + " ".join(target_terms) + ". " + \
                         f"Specific metric: The total confirmed {target_terms[0]} for period was 48.7 million dollars with high margin."
                regions = [
                    DocumentRegionRecord(
                        region_id=f"{doc_id}_p{p_num}_tbl1",
                        page_number=p_num,
                        bbox=(80, 120, 920, 580),
                        region_type="table",
                        text_content=f"Consolidated Table for {target_terms[0]}: Total = $48.7M",
                        confidence=0.95
                    ),
                    DocumentRegionRecord(
                        region_id=f"{doc_id}_p{p_num}_txt1",
                        page_number=p_num,
                        bbox=(80, 600, 920, 850),
                        region_type="text",
                        text_content=f"Audited notes on {target_terms[1]} and statutory disclosures.",
                        confidence=0.92
                    )
                ]
            else:
                # Distractor page from other topics
                other_topic = list(vocabulary_topics.keys())[(d_idx + p_num) % len(vocabulary_topics)]
                other_terms = vocabulary_topics[other_topic]
                p_text = f"General Overview of {other_topic.capitalize()} Section {p_num}: " + " ".join(other_terms) + \
                         f". Standard administrative notes and boilerplate documentation for page {p_num}."
                regions = [
                    DocumentRegionRecord(
                        region_id=f"{doc_id}_p{p_num}_reg1",
                        page_number=p_num,
                        bbox=(50, 80, 950, 400),
                        region_type="text",
                        text_content=f"Narrative on {other_terms[0]}.",
                        confidence=0.89
                    )
                ]

            # In degraded variants, simulate OCR noise
            if deg_level == "mild":
                quality_score = 0.82
            elif deg_level == "moderate":
                quality_score = 0.65
                # Introduce slight OCR character substitutions
                p_text = p_text.replace("e", "e").replace("i", "1").replace("o", "0")
            elif deg_level == "severe":
                quality_score = 0.40
                p_text = p_text.replace("a", "@").replace("t", "+").replace("e", "3")
            else:
                quality_score = 0.95

            page_rec = DocumentPageRecord(
                document_id=doc_id,
                page_number=p_num,
                split=split,
                raw_text=p_text,
                quality_score=quality_score,
                degradation_level=deg_level,
                regions=regions
            )
            page_index.add_page(page_rec)

        # Save index file
        idx_path = os.path.join(output_dir, f"{doc_id}.json")
        page_index.save(idx_path)

        # Create corresponding query
        q_id = f"q_{doc_id}"
        query = RetrievalQuery(
            query_id=q_id,
            document_id=doc_id,
            query_text=f"What was the total {target_terms[0]} and financial table for {target_topic}?",
            query_type="table" if "table" in target_terms or d_idx % 2 == 0 else "factoid",
            ground_truth_pages=[target_page_num],
            ground_truth_regions=[f"{doc_id}_p{target_page_num}_tbl1"]
        )

        manifest["documents"].append({
            "document_id": doc_id,
            "page_count": doc_len,
            "split": split,
            "degradation_level": deg_level,
            "index_path": idx_path
        })
        manifest["queries"].append(query.model_dump())

    manifest_file = os.path.join(output_dir, "corpus_manifest.json")
    with open(manifest_file, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"Generated {num_docs} multi-page documents and queries in {output_dir}")
    return manifest


if __name__ == "__main__":
    generate_synthetic_multipage_corpus()
