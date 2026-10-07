"""Upload Manager & Storage Security for Document Extraction Studio.

Enforces:
- Sanitized filenames and randomized UUID storage
- Magic bytes header validation
- Strict file extension and MIME type allowlists (.pdf, .png, .jpg, .jpeg)
- Size quotas (default 25 MB)
- Automated age-based cache eviction
"""

import os
import re
import time
import uuid
import mimetypes
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any, List

ALLOWED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg"}
ALLOWED_MIME_TYPES = {
    "application/pdf",
    "image/png",
    "image/jpeg",
    "image/jpg",
}

# Magic byte signatures
MAGIC_SIGNATURES = {
    ".pdf": [b"%PDF"],
    ".png": [b"\x89PNG\r\n\x1a\n"],
    ".jpg": [b"\xff\xd8\xff"],
    ".jpeg": [b"\xff\xd8\xff"],
}

class UploadValidationError(ValueError):
    """Raised when an uploaded file violates safety, format, or size policies."""
    pass

@dataclass
class UploadRecord:
    upload_id: str
    original_filename: str
    sanitized_filename: str
    extension: str
    content_type: str
    size_bytes: int
    created_at_epoch: float
    file_path: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

class UploadManager:
    """Manages secure file uploads, validation, and lifecycle cache."""

    def __init__(
        self,
        upload_dir: Optional[Path] = None,
        max_size_bytes: int = 25 * 1024 * 1024 # 25 MB
    ):
        if upload_dir is None:
            self.upload_dir = Path(__file__).resolve().parent.parent.parent / "runtime" / "uploads"
        else:
            self.upload_dir = Path(upload_dir)
        self.max_size_bytes = max_size_bytes
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    def validate_file(self, raw_bytes: bytes, filename: str, content_type: Optional[str] = None) -> str:
        """Validates file bytes, extension, MIME type, and magic bytes."""
        if not raw_bytes:
            raise UploadValidationError("Empty file: uploaded content has 0 bytes.")

        if len(raw_bytes) > self.max_size_bytes:
            raise UploadValidationError(
                f"File size ({len(raw_bytes)} bytes) exceeds maximum allowed limit ({self.max_size_bytes} bytes)."
            )

        # 1. Extension check
        ext = Path(filename).suffix.lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise UploadValidationError(
                f"Unsupported file extension '{ext}'. Allowed extensions: {sorted(ALLOWED_EXTENSIONS)}"
            )

        # 2. Magic byte check
        expected_sigs = MAGIC_SIGNATURES.get(ext, [])
        matched_magic = any(raw_bytes.startswith(sig) for sig in expected_sigs)
        if not matched_magic:
            raise UploadValidationError(
                f"File content does not match declared extension '{ext}' (invalid magic byte signature)."
            )

        return ext

    def sanitize_filename(self, filename: str) -> str:
        """Strips dangerous characters, directory traversal sequences, and windows reserved names."""
        clean_name = os.path.basename(filename)
        # Keep alphanumeric, dots, underscores, dashes
        clean_name = re.sub(r"[^a-zA-Z0-9._-]", "_", clean_name)
        if not clean_name or clean_name.startswith("."):
            clean_name = f"doc_{clean_name}"
        return clean_name

    def save_upload(
        self,
        raw_bytes: bytes,
        filename: str,
        content_type: Optional[str] = None
    ) -> UploadRecord:
        """Validates and persists uploaded file under an isolated UUID path."""
        ext = self.validate_file(raw_bytes, filename, content_type)
        sanitized = self.sanitize_filename(filename)

        upload_id = str(uuid.uuid4())
        # Safe storage filename: uuid_sanitized.ext
        storage_filename = f"{upload_id}_{sanitized}"
        target_path = self.upload_dir / storage_filename

        target_path.write_bytes(raw_bytes)

        # Resolve MIME type if missing or generic
        mime = content_type or mimetypes.guess_type(sanitized)[0] or "application/octet-stream"

        return UploadRecord(
            upload_id=upload_id,
            original_filename=filename,
            sanitized_filename=sanitized,
            extension=ext,
            content_type=mime,
            size_bytes=len(raw_bytes),
            created_at_epoch=time.time(),
            file_path=str(target_path)
        )

    def get_upload(self, upload_id: str) -> Optional[UploadRecord]:
        """Looks up an upload by ID."""
        for p in self.upload_dir.iterdir():
            if p.is_file() and p.name.startswith(f"{upload_id}_"):
                ext = p.suffix.lower()
                mime = mimetypes.guess_type(p.name)[0] or "application/octet-stream"
                orig_name = p.name[len(upload_id) + 1:]
                return UploadRecord(
                    upload_id=upload_id,
                    original_filename=orig_name,
                    sanitized_filename=orig_name,
                    extension=ext,
                    content_type=mime,
                    size_bytes=p.stat().st_size,
                    created_at_epoch=p.stat().st_mtime,
                    file_path=str(p)
                )
        return None

    def cleanup_old_uploads(self, max_age_seconds: int = 3600) -> int:
        """Deletes files in upload_dir older than max_age_seconds."""
        now = time.time()
        deleted_count = 0
        if not self.upload_dir.exists():
            return 0

        for p in self.upload_dir.iterdir():
            if p.is_file():
                try:
                    age = now - p.stat().st_mtime
                    if age >= max_age_seconds:
                        p.unlink()
                        deleted_count += 1
                except Exception:
                    pass
        return deleted_count
