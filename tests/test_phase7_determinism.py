"""
Unit tests for Phase 7 Pipeline Determinism.
"""

from src.evidence.pipeline import EvidenceGroundingPipeline


def test_pipeline_determinism():
    pipeline = EvidenceGroundingPipeline()

    doc_id = "doc_det_001"
    query_id = "q_det_001"
    query = "What is the total due?"
    answer = "$500.00"
    pages = [{"page_number": 1, "score": 0.9, "clean_text": "Total Due: $500.00"}]
    regions = [{
        "region_id": "r1",
        "page_number": 1,
        "bbox": (100, 200, 300, 400),
        "snippet": "Total Due: $500.00",
        "score": 0.95
    }]
    gt_boxes = [(100, 200, 300, 400)]

    pkg1 = pipeline.process(
        document_id=doc_id,
        query_id=query_id,
        query_text=query,
        answer_text=answer,
        selected_pages=pages,
        selected_regions=regions,
        baseline_id="B7-5",
        dataset="docvqa",
        condition="clean",
        seed=42,
        ground_truth_bboxes=gt_boxes
    )

    pkg2 = pipeline.process(
        document_id=doc_id,
        query_id=query_id,
        query_text=query,
        answer_text=answer,
        selected_pages=pages,
        selected_regions=regions,
        baseline_id="B7-5",
        dataset="docvqa",
        condition="clean",
        seed=42,
        ground_truth_bboxes=gt_boxes
    )

    assert pkg1.package_id == pkg2.package_id
    assert pkg1.grounding_result.grounding_status == pkg2.grounding_result.grounding_status
    assert pkg1.grounding_result.grounding_score == pkg2.grounding_result.grounding_score
    assert len(pkg1.citations) == len(pkg2.citations)
    assert pkg1.citations[0].citation_id == pkg2.citations[0].citation_id
    assert pkg1.provenance["run_id"] == pkg2.provenance["run_id"]
