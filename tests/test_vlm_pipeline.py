"""Unit Tests for VLM Prompting and Image Preprocessing Pipelines."""

import pytest
from PIL import Image
from src.vlm.prompts import PromptManager
from src.vlm.processor import VLMImageProcessor


def test_prompt_manager_b1_formatting():
    """Verify B1 prompt template formats question and OCR text with hash tracking."""
    pm = PromptManager()
    prompt_text, ver, p_hash = pm.format_prompt(
        prompt_file="configs/phase2/prompts/b1_prompt.txt",
        version_tag="v1.0-b1",
        question="What is the invoice total?",
        ocr_text="Total: $120.50"
    )

    assert "What is the invoice total?" in prompt_text
    assert "Total: $120.50" in prompt_text
    assert ver == "v1.0-b1"
    assert len(p_hash) == 16


def test_prompt_manager_b2_formatting():
    """Verify B2 prompt template formats question with hash tracking."""
    pm = PromptManager()
    prompt_text, ver, p_hash = pm.format_prompt(
        prompt_file="configs/phase2/prompts/b2_prompt.txt",
        version_tag="v1.0-b2",
        question="What is the date?"
    )

    assert "What is the date?" in prompt_text
    assert ver == "v1.0-b2"
    assert len(p_hash) == 16


def test_image_processor_transformation_tracking():
    """Verify image processor records explicit transformations without silent alterations."""
    img = Image.new("RGB", (1200, 800), color=(100, 150, 200))
    processor = VLMImageProcessor()

    # Case 1: No resize needed
    out_img, record = processor.process(img, target_max_dim=1500)
    assert record.original_width == 1200
    assert record.original_height == 800
    assert record.processed_width == 1200
    assert record.processed_height == 800
    assert record.resize_factor == 1.0
    assert record.color_mode == "RGB"

    # Case 2: Downscaling applied
    out_img, record = processor.process(img, target_max_dim=600)
    assert record.original_width == 1200
    assert record.processed_width == 600
    assert record.processed_height == 400
    assert record.resize_factor == 0.5
    assert out_img.size == (600, 400)
