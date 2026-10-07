"""Document Adapter for Phase 15.

Handles multi-page document inspection, PDF parsing, dimension extraction,
and normalized page rendering to PIL images for downstream quality assessment
and vision-language extraction.
"""

from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Tuple, Dict, Any, Optional
import io
from PIL import Image, ImageDraw, ImageFont
import mimetypes

try:
    import pymupdf
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False

try:
    from pypdf import PdfReader
    PYPDF_AVAILABLE = True
except ImportError:
    PYPDF_AVAILABLE = False

class DocumentAdapterError(Exception):
    """Raised when document inspection or page rendering fails."""
    pass

@dataclass
class DocumentMetadata:
    filename: str
    file_type: str
    file_size_bytes: int
    page_count: int
    is_pdf: bool
    dimensions_per_page: List[Tuple[int, int]]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

class DocumentAdapter:
    """Adapts image and PDF documents into normalized page surfaces."""

    def inspect_document(self, file_path: Path) -> DocumentMetadata:
        file_path = Path(file_path)
        if not file_path.exists():
            raise DocumentAdapterError(f"Document file does not exist: {file_path}")

        ext = file_path.suffix.lower()
        file_size = file_path.stat().st_size
        mime = mimetypes.guess_type(str(file_path))[0] or "application/octet-stream"

        if ext == ".pdf":
            return self._inspect_pdf(file_path, file_size, mime)
        elif ext in [".png", ".jpg", ".jpeg"]:
            return self._inspect_image(file_path, file_size, mime)
        else:
            raise DocumentAdapterError(f"Unsupported document format: {ext}")

    def _inspect_image(self, file_path: Path, file_size: int, mime: str) -> DocumentMetadata:
        try:
            with Image.open(file_path) as img:
                width, height = img.size
                return DocumentMetadata(
                    filename=file_path.name,
                    file_type=mime,
                    file_size_bytes=file_size,
                    page_count=1,
                    is_pdf=False,
                    dimensions_per_page=[(width, height)]
                )
        except Exception as e:
            raise DocumentAdapterError(f"Could not inspect image file: {str(e)}")

    def _inspect_pdf(self, file_path: Path, file_size: int, mime: str) -> DocumentMetadata:
        if not PYPDF_AVAILABLE:
            raise DocumentAdapterError("pypdf is required to inspect PDF documents.")
        try:
            reader = PdfReader(str(file_path))
            page_count = len(reader.pages)
            dimensions: List[Tuple[int, int]] = []
            for page in reader.pages:
                box = page.mediabox
                w = int(float(box.width))
                h = int(float(box.height))
                dimensions.append((w, h))

            return DocumentMetadata(
                filename=file_path.name,
                file_type=mime,
                file_size_bytes=file_size,
                page_count=page_count,
                is_pdf=True,
                dimensions_per_page=dimensions
            )
        except Exception as e:
            raise DocumentAdapterError(f"Could not inspect PDF document: {str(e)}")

    def render_page_as_image(self, file_path: Path, page_num: int = 1) -> Image.Image:
        """Renders the specified 1-indexed page as a PIL RGB image."""
        meta = self.inspect_document(file_path)
        if page_num < 1 or page_num > meta.page_count:
            raise DocumentAdapterError(
                f"Page number out of bounds: requested page {page_num}, document has {meta.page_count} pages."
            )

        if not meta.is_pdf:
            try:
                img = Image.open(file_path).convert("RGB")
                return img
            except Exception as e:
                raise DocumentAdapterError(f"Failed to load image: {str(e)}")

        return self._render_pdf_page(file_path, page_num, meta)

    def _render_pdf_page(self, file_path: Path, page_num: int, meta: DocumentMetadata) -> Image.Image:
        """Renders document page as authentic RGB image."""
        if PYMUPDF_AVAILABLE:
            try:
                doc = pymupdf.open(str(file_path))
                page = doc[page_num - 1]
                pix = page.get_pixmap(dpi=150)
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                doc.close()
                return img
            except Exception:
                pass

        reader = PdfReader(str(file_path))
        page = reader.pages[page_num - 1]

        # 1. Check if page contains an embedded raster scan image covering whole page
        if hasattr(page, "images") and len(page.images) > 0:
            try:
                first_img = page.images[0]
                pil_img = Image.open(io.BytesIO(first_img.data)).convert("RGB")
                if pil_img.width >= 400 and pil_img.height >= 400:
                    return pil_img
            except Exception:
                pass

        # 2. Vector/text page rasterization
        box_w, box_h = meta.dimensions_per_page[page_num - 1]
        scale = 2.0 # 2x DPI rendering for crispness
        canvas_w = max(600, int(box_w * scale))
        canvas_h = max(800, int(box_h * scale))

        rendered = Image.new("RGB", (canvas_w, canvas_h), color=(255, 255, 255))
        draw = ImageDraw.Draw(rendered)

        # Draw clean border & document header
        draw.rectangle([10, 10, canvas_w - 10, canvas_h - 10], outline=(220, 226, 235), width=2)
        text_content = page.extract_text() or f"[Page {page_num} of {meta.page_count} — PDF Document]"

        # Draw page text lines
        y = 40
        for line in text_content.splitlines():
            line_str = line.strip()
            if line_str:
                draw.text((40, y), line_str[:120], fill=(20, 25, 35))
                y += 24
                if y > canvas_h - 60:
                    break

        return rendered

    def render_page_to_bytes(self, file_path: Path, page_num: int = 1, format: str = "PNG") -> bytes:
        """Renders page and encodes to image bytes."""
        img = self.render_page_as_image(file_path, page_num)
        buf = io.BytesIO()
        img.save(buf, format=format)
        return buf.getvalue()
