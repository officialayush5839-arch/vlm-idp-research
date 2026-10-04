"""
PDF validation, page extraction, and deterministic rendering engine.
Uses PyMuPDF (fitz) for sub-pixel rendering accuracy and coordinate fidelity.
"""

from __future__ import annotations

import io
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from PIL import Image
import fitz  # PyMuPDF

from src.core.logging import get_logger
from src.ingestion.metadata import compute_sha256, derive_document_id
from src.ingestion.schema import Document, Page

logger = get_logger(__name__)


class PDFValidationError(ValueError):
    """Raised when a PDF file is corrupt, empty, or unreadable."""
    pass


def validate_pdf(pdf_path: str | Path) -> Tuple[int, Dict[str, str]]:
    """
    Validate PDF integrity and extract document-level metadata.
    
    Returns:
        (page_count, metadata_dict)
    Raises:
        PDFValidationError if corrupted or invalid.
    """
    path = Path(pdf_path)
    if not path.is_file():
        raise FileNotFoundError(f"PDF file does not exist: {path.resolve()}")

    try:
        doc = fitz.open(str(path))
        if doc.is_encrypted:
            raise PDFValidationError(f"Encrypted PDFs are not supported without credentials: {path.name}")
        page_count = len(doc)
        if page_count == 0:
            raise PDFValidationError(f"PDF contains 0 pages: {path.name}")

        meta = {k: str(v) for k, v in doc.metadata.items() if v} if doc.metadata else {}
        doc.close()
        return page_count, meta
    except Exception as e:
        if isinstance(e, (PDFValidationError, FileNotFoundError)):
            raise
        raise PDFValidationError(f"Failed to parse PDF {path.name}: {e}") from e


def render_pdf_page(
    pdf_path: str | Path,
    page_number: int,
    dpi: int = 150
) -> Tuple[Image.Image, Tuple[float, float]]:
    """
    Render a specific 1-indexed PDF page to a PIL Image at specified DPI.
    
    Returns:
        (PIL_Image, (original_width_pt, original_height_pt))
    """
    path = Path(pdf_path)
    doc = fitz.open(str(path))

    if page_number < 1 or page_number > len(doc):
        doc.close()
        raise IndexError(f"Page number {page_number} out of range [1, {len(doc)}]")

    page = doc.load_page(page_number - 1)
    rect = page.rect
    orig_dims = (rect.width, rect.height)

    # 72 points per inch standard PDF coordinate system
    zoom = dpi / 72.0
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat, alpha=False)

    img = Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")
    doc.close()

    return img, orig_dims


def ingest_pdf(
    pdf_path: str | Path,
    output_dir: Optional[str | Path] = None,
    dpi: int = 150,
    dataset_name: Optional[str] = None,
    partition: Optional[str] = None,
) -> Document:
    """
    Deterministically ingest a multi-page PDF document.
    Renders pages, computes cryptographic hashes, and constructs a Document object.
    
    Args:
        pdf_path: Absolute or relative path to PDF
        output_dir: Optional directory to save rendered page PNGs
        dpi: Target rendering DPI (default: 150)
        dataset_name: Optional dataset label
        partition: Optional split partition ('train', 'val', 'test')
    """
    path = Path(pdf_path).resolve()
    source_hash = compute_sha256(path)
    doc_id = derive_document_id(source_hash)
    page_count, meta = validate_pdf(path)

    if output_dir:
        out_path = Path(output_dir) / doc_id
        out_path.mkdir(parents=True, exist_ok=True)
    else:
        out_path = None

    pages: List[Page] = []

    for page_idx in range(1, page_count + 1):
        page_id = f"{doc_id}_p{page_idx:03d}"
        img, orig_dims = render_pdf_page(path, page_number=page_idx, dpi=dpi)

        if out_path:
            img_file = out_path / f"page_{page_idx:03d}.png"
            img.save(img_file, format="PNG")
            img_path_str = str(img_file.resolve())
            page_hash = compute_sha256(img_file)
        else:
            img_path_str = f"in_memory://{page_id}"
            # Compute hash from byte buffer
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            page_hash = compute_sha256(buf.getvalue())

        pages.append(
            Page(
                page_id=page_id,
                document_id=doc_id,
                page_number=page_idx,
                width=img.width,
                height=img.height,
                image_path=img_path_str,
                source_dimensions=orig_dims,
                normalized_dimensions=(1000, 1000),
                render_dpi=dpi,
                page_hash_sha256=page_hash,
                metadata={},
            )
        )

    return Document(
        document_id=doc_id,
        source_path=str(path),
        source_hash_sha256=source_hash,
        page_count=page_count,
        pages=pages,
        dataset_name=dataset_name,
        partition=partition,
        metadata=meta,
    )
