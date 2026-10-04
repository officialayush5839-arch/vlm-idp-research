"""Unit Tests for Unlimited-OCR Reproducibility and Determinism."""

from PIL import Image
from src.baselines.base import BaselineSample
from src.baselines.unlimited_ocr.adapter import B0UnlimitedOCRBaseline


def test_unlimited_ocr_reproducibility():
    """Verify B0-U produces identical answers and metadata when executed twice."""
    img = Image.new("RGB", (600, 400), color=(255, 255, 255))
    sample = BaselineSample(
        sample_id="q_repro",
        document_id="doc_repro",
        page_idx=0,
        image=img,
        question="What is the vendor name?",
        ground_truth_answers=["Acme Corporation"]
    )
    baseline = B0UnlimitedOCRBaseline()

    res1 = baseline.run(sample, run_id="run_repro_1", seed=42)
    res2 = baseline.run(sample, run_id="run_repro_2", seed=42)

    assert res1.answer == res2.answer
    assert res1.status == res2.status
    assert res1.model == res2.model
    assert res1.model_revision == res2.model_revision
    assert res1.prompt_hash == res2.prompt_hash
