"""Unit tests for Phase 3 DocumentQualityPipeline."""

from PIL import Image
import pytest

from src.ingestion.schema import Document, Page
from src.quality.pipeline import DocumentQualityPipeline
from src.quality.synthetic import create_clean_document_fixture


@pytest.fixture
def pipeline():
    return DocumentQualityPipeline()


def test_assess_page_success(pipeline):
    img = create_clean_document_fixture()
    page_res = pipeline.assess_page(img, document_id="doc_test_1", page_id="page_1")
    assert page_res.status == "SUCCESS"
    assert page_res.document_id == "doc_test_1"
    assert page_res.page_id == "page_1"
    assert page_res.width == 600
    assert page_res.height == 400
    assert len(page_res.features) == 10
    assert page_res.overall_quality_score is None
    assert page_res.overall_quality_status == "NOT_DEFINED"
    assert page_res.runtime.total_latency_ms > 0.0


def test_assess_document_multi_page(pipeline, tmp_path):
    img1 = create_clean_document_fixture(title="PAGE 1")
    img2 = create_clean_document_fixture(title="PAGE 2")
    p1_path = tmp_path / "page_1.png"
    p2_path = tmp_path / "page_2.png"
    img1.save(p1_path)
    img2.save(p2_path)

    doc = Document(
        document_id="doc_multi_001",
        source_path=str(tmp_path),
        source_hash_sha256="dummy_hash_001",
        page_count=2,
        pages=[
            Page(
                page_id="p001",
                document_id="doc_multi_001",
                page_number=1,
                width=600,
                height=400,
                image_path=str(p1_path),
                source_dimensions=(600.0, 400.0),
                page_hash_sha256="hash1",
            ),
            Page(
                page_id="p002",
                document_id="doc_multi_001",
                page_number=2,
                width=600,
                height=400,
                image_path=str(p2_path),
                source_dimensions=(600.0, 400.0),
                page_hash_sha256="hash2",
            ),
        ],
    )

    doc_res = pipeline.assess_document(doc)
    assert doc_res.document_id == "doc_multi_001"
    assert doc_res.page_count == 2
    assert len(doc_res.pages) == 2
    assert "blur" in doc_res.summary_statistics
    assert "mean" in doc_res.summary_statistics["blur"]
    assert doc_res.worst_page_id is not None
    assert doc_res.status == "SUCCESS"
