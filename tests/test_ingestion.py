"""
Unit and integration tests for PDF validation, page extraction, and ingestion.
Uses programmatically generated synthetic PDF fixtures (no external heavy files).
"""

from pathlib import Path
import fitz  # PyMuPDF
import pytest
from src.ingestion.pdf import PDFValidationError, ingest_pdf, render_pdf_page, validate_pdf


@pytest.fixture
def sample_pdf_path(tmp_path: Path) -> Path:
    """Generate a clean 2-page test PDF fixture using PyMuPDF."""
    pdf_file = tmp_path / "test_document.pdf"
    doc = fitz.open()

    # Page 1: Standard Letter size (612 x 792 pt)
    p1 = doc.new_page(width=612, height=792)
    p1.insert_text((72, 100), "VLM-IDP Research Project: Page 1 Title", fontsize=16)
    p1.insert_text((72, 150), "Figure 1: Architecture Overview and Routing Mechanism.", fontsize=11)

    # Page 2: Standard Letter size
    p2 = doc.new_page(width=612, height=792)
    p2.insert_text((72, 100), "Page 2: Results and Discussion", fontsize=16)
    p2.insert_text((72, 150), "Table 1: Baseline Comparison on DocVQA Benchmark.", fontsize=11)

    doc.save(str(pdf_file))
    doc.close()
    return pdf_file


@pytest.mark.ingestion
class TestPDFIngestion:

    def test_validate_pdf_valid(self, sample_pdf_path: Path):
        """Valid PDF returns correct page count."""
        page_count, meta = validate_pdf(sample_pdf_path)
        assert page_count == 2
        assert isinstance(meta, dict)

    def test_validate_pdf_nonexistent_fails(self, tmp_path: Path):
        """Non-existent file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            validate_pdf(tmp_path / "does_not_exist.pdf")

    def test_validate_pdf_corrupt_fails(self, tmp_path: Path):
        """Corrupted PDF raises PDFValidationError."""
        corrupt_file = tmp_path / "corrupt.pdf"
        corrupt_file.write_bytes(b"%PDF-1.4 but not real data")
        with pytest.raises(PDFValidationError):
            validate_pdf(corrupt_file)

    def test_render_pdf_page(self, sample_pdf_path: Path):
        """Rendering page 1 at 150 DPI produces expected image dimensions."""
        img, (w_pt, h_pt) = render_pdf_page(sample_pdf_path, page_number=1, dpi=150)
        assert w_pt == 612.0
        assert h_pt == 792.0
        # 612 * (150/72) = 1275 px
        assert abs(img.width - 1275) <= 2
        # 792 * (150/72) = 1650 px
        assert abs(img.height - 1650) <= 2

    def test_ingest_pdf_full_pipeline(self, sample_pdf_path: Path, tmp_path: Path):
        """Ingest multi-page PDF into Document and Page objects."""
        out_dir = tmp_path / "rendered_output"
        doc = ingest_pdf(
            sample_pdf_path,
            output_dir=out_dir,
            dpi=100,
            dataset_name="SyntheticTest",
            partition="test"
        )

        assert doc.document_id.startswith("doc_")
        assert doc.page_count == 2
        assert len(doc.pages) == 2
        assert doc.partition == "test"
        assert doc.dataset_name == "SyntheticTest"

        # Check Page 1
        page1 = doc.pages[0]
        assert page1.page_number == 1
        assert Path(page1.image_path).is_file()
        assert len(page1.page_hash_sha256) == 64
        assert page1.normalized_dimensions == (1000, 1000)

        # Check Page 2
        page2 = doc.pages[1]
        assert page2.page_number == 2
        assert Path(page2.image_path).is_file()
