"""
Determinism tests for Phase 6 Retrieval Pipeline.
Verifies that executing the same retrieval query with identical random seed
produces identical ranked candidates, scores, and evidence packages.
"""

from src.retrieval.pipeline import MultimodalRetrievalPipeline
from src.retrieval.schema import DocumentPageRecord, DocumentRegionRecord, RetrievalQuery


def _create_sample_pages():
    return [
        DocumentPageRecord(
            document_id="doc_det_1",
            page_number=1,
            split="test",
            raw_text="Introduction and corporate governance overview",
            regions=[]
        ),
        DocumentPageRecord(
            document_id="doc_det_1",
            page_number=2,
            split="test",
            raw_text="Financial statements, operating revenues, consolidated balance sheet",
            regions=[
                DocumentRegionRecord(
                    region_id="reg_bal",
                    page_number=2,
                    bbox=(100, 100, 900, 500),
                    region_type="table",
                    text_content="Consolidated balance sheet table"
                )
            ]
        ),
        DocumentPageRecord(
            document_id="doc_det_1",
            page_number=3,
            split="test",
            raw_text="Environmental impact statement and energy consumption",
            regions=[]
        ),
        DocumentPageRecord(
            document_id="doc_det_1",
            page_number=4,
            split="test",
            raw_text="Independent auditor report and risk factors",
            regions=[]
        ),
        DocumentPageRecord(
            document_id="doc_det_1",
            page_number=5,
            split="test",
            raw_text="Executive compensation and stock option grants",
            regions=[]
        )
    ]


def test_pipeline_determinism(tmp_path):
    pages = _create_sample_pages()
    query = RetrievalQuery(
        query_id="q_fin",
        document_id="doc_det_1",
        query_text="Where is the consolidated balance sheet table?",
        ground_truth_pages=[2]
    )

    pipe1 = MultimodalRetrievalPipeline(random_seed=42, evidence_dir=str(tmp_path / "e1"))
    pipe1.index_document(pages)
    pkg1 = pipe1.retrieve(query, method="B6-5", top_k=3, top_m=2)

    pipe2 = MultimodalRetrievalPipeline(random_seed=42, evidence_dir=str(tmp_path / "e2"))
    pipe2.index_document(pages)
    pkg2 = pipe2.retrieve(query, method="B6-5", top_k=3, top_m=2)

    # Candidate page rankings must match exactly
    pages1 = [p.page_number for p in pkg1.selected_pages]
    pages2 = [p.page_number for p in pkg2.selected_pages]
    assert pages1 == pages2

    # Scores must match exactly
    scores1 = [p.score for p in pkg1.selected_pages]
    scores2 = [p.score for p in pkg2.selected_pages]
    assert scores1 == scores2

    # Selected regions must match exactly
    regs1 = [r.region_id for r in pkg1.selected_regions]
    regs2 = [r.region_id for r in pkg2.selected_regions]
    assert regs1 == regs2
