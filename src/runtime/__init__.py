"""Phase 15 Runtime and Document Extraction Studio Engine.

Contains runtime upload management, document adapters, model registries,
and the end-to-end pipeline orchestrator for real document processing.
"""

from pathlib import Path

RUNTIME_DIR = Path(__file__).resolve().parent
UPLOADS_DIR = RUNTIME_DIR.parent.parent / "runtime" / "uploads"
