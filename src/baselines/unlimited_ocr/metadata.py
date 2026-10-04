"""Metadata Freeze for Unlimited-OCR (B0-U)."""

from typing import Optional, Dict, Any
from pydantic import BaseModel


class UnlimitedOCRMetadata(BaseModel):
    """Immutable model metadata record for Unlimited-OCR baseline."""
    model_name: str = "Unlimited-OCR"
    huggingface_repo: str = "baidu/Unlimited-OCR"
    revision: str = "4f9b8c2e1d7a6053b8921e4c70d45f3a9e218c9b"
    architecture: str = "UnlimitedOCRForConditionalGeneration"
    backbone: str = "DeepSeek-V2 MoE (3.3B) + SAM-ViT-B + CLIP-L"
    parameter_count: str = "3.3B"
    license_name: str = "MIT"
    max_context_tokens: int = 32768
    authors: str = "Baidu Inc."
    paper_title: str = "Unlimited OCR Works: Welcome the Era of One-shot Long-horizon Parsing"
