"""Tests for Phase 15 Upload Manager & Security Validation."""

import pytest
from pathlib import Path
from src.runtime.upload_manager import UploadManager, UploadValidationError, UploadRecord

@pytest.fixture
def upload_manager(tmp_path):
    return UploadManager(upload_dir=tmp_path / "uploads", max_size_bytes=5 * 1024 * 1024)

def test_valid_png_upload(upload_manager):
    # Valid PNG 1x1 image bytes
    png_bytes = (
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
        b"\x08\x06\x00\x00\x00\x1f\x15c4\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05"
        b"\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
    )
    record = upload_manager.save_upload(png_bytes, "test_document.png", "image/png")
    assert isinstance(record, UploadRecord)
    assert record.original_filename == "test_document.png"
    assert record.content_type == "image/png"
    assert record.extension == ".png"
    assert record.size_bytes == len(png_bytes)
    assert Path(record.file_path).exists()
    assert Path(record.file_path).read_bytes() == png_bytes

def test_valid_jpeg_upload(upload_manager):
    jpeg_bytes = b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xff\xdb" + b"\x00" * 20 + b"\xff\xd9"
    record = upload_manager.save_upload(jpeg_bytes, "scan.jpg", "image/jpeg")
    assert record.extension == ".jpg"
    assert Path(record.file_path).exists()

def test_valid_pdf_upload(upload_manager):
    pdf_bytes = b"%PDF-1.4\n1 0 obj\n<<>>\nendobj\ntrailer\n<<>>\n%%EOF"
    record = upload_manager.save_upload(pdf_bytes, "invoice.pdf", "application/pdf")
    assert record.extension == ".pdf"
    assert Path(record.file_path).exists()

def test_path_traversal_rejection(upload_manager):
    png_bytes = b"\x89PNG\r\n\x1a\n" + b"\x00" * 50
    record = upload_manager.save_upload(png_bytes, "../../../etc/passwd.png", "image/png")
    # File must be strictly inside upload_dir and traversal directories discarded
    assert Path(record.file_path).resolve().parent == upload_manager.upload_dir.resolve()
    assert ".." not in record.file_path

def test_unsupported_extension(upload_manager):
    exe_bytes = b"MZ\x90\x00" + b"\x00" * 50
    with pytest.raises(UploadValidationError, match="Unsupported file extension"):
        upload_manager.save_upload(exe_bytes, "malware.exe", "application/x-dosexec")

def test_empty_file_rejection(upload_manager):
    with pytest.raises(UploadValidationError, match="Empty file"):
        upload_manager.save_upload(b"", "empty.png", "image/png")

def test_oversized_file_rejection(upload_manager):
    huge_bytes = b"\x89PNG\r\n\x1a\n" + (b"X" * (6 * 1024 * 1024))
    with pytest.raises(UploadValidationError, match="exceeds maximum"):
        upload_manager.save_upload(huge_bytes, "huge.png", "image/png")

def test_magic_byte_mismatch(upload_manager):
    # Extension says png, but content is text
    fake_png = b"This is just text pretending to be png"
    with pytest.raises(UploadValidationError, match="File content does not match"):
        upload_manager.save_upload(fake_png, "fake.png", "image/png")

def test_cleanup_policy(upload_manager):
    png_bytes = (
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
        b"\x08\x06\x00\x00\x00\x1f\x15c4\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05"
        b"\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
    )
    record = upload_manager.save_upload(png_bytes, "temp.png", "image/png")
    assert Path(record.file_path).exists()
    # Age threshold 0 seconds should clean up the file
    cleaned = upload_manager.cleanup_old_uploads(max_age_seconds=0)
    assert cleaned >= 1
    assert not Path(record.file_path).exists()
