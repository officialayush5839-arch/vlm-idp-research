"""Tests for Phase 15 Document Adapter & Multi-Page Document Handling."""

import pytest
from pathlib import Path
from PIL import Image, ImageDraw
from pypdf import PdfWriter
from src.runtime.document_adapter import DocumentAdapter, DocumentMetadata, DocumentAdapterError

@pytest.fixture
def sample_png(tmp_path):
    img_path = tmp_path / "sample_invoice.png"
    img = Image.new("RGB", (600, 800), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw.text((50, 50), "INVOICE #1042", fill=(0, 0, 0))
    draw.text((50, 100), "Total Balance Due: $1,420.50", fill=(0, 0, 0))
    img.save(img_path)
    return img_path

@pytest.fixture
def sample_pdf(tmp_path):
    pdf_path = tmp_path / "two_page_doc.pdf"
    writer = PdfWriter()
    writer.add_blank_page(width=612, height=792) # 8.5 x 11 inches
    writer.add_blank_page(width=612, height=792)
    with open(pdf_path, "wb") as f:
        writer.write(f)
    return pdf_path

def test_inspect_png(sample_png):
    adapter = DocumentAdapter()
    meta = adapter.inspect_document(sample_png)
    assert isinstance(meta, DocumentMetadata)
    assert meta.page_count == 1
    assert meta.is_pdf is False
    assert meta.dimensions_per_page == [(600, 800)]
    assert meta.file_type == "image/png"

def test_render_png_page(sample_png):
    adapter = DocumentAdapter()
    img = adapter.render_page_as_image(sample_png, page_num=1)
    assert isinstance(img, Image.Image)
    assert img.size == (600, 800)
    assert img.mode == "RGB"

def test_inspect_pdf(sample_pdf):
    adapter = DocumentAdapter()
    meta = adapter.inspect_document(sample_pdf)
    assert meta.is_pdf is True
    assert meta.page_count == 2
    assert len(meta.dimensions_per_page) == 2
    assert meta.dimensions_per_page[0] == (612, 792)

def test_render_pdf_page(sample_pdf):
    adapter = DocumentAdapter()
    img = adapter.render_page_as_image(sample_pdf, page_num=1)
    assert isinstance(img, Image.Image)
    assert img.width > 0 and img.height > 0

def test_invalid_page_number(sample_png):
    adapter = DocumentAdapter()
    with pytest.raises(DocumentAdapterError, match="Page number out of bounds"):
        adapter.render_page_as_image(sample_png, page_num=2)

def test_corrupted_document(tmp_path):
    bad_file = tmp_path / "corrupted.png"
    bad_file.write_bytes(b"\x89PNG\r\n\x1a\ncorrupted_data_not_an_image")
    adapter = DocumentAdapter()
    with pytest.raises(DocumentAdapterError, match="Could not inspect"):
        adapter.inspect_document(bad_file)
