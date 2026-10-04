"""Unit Tests for B0-U Unlimited-OCR Baseline Adapter."""

from PIL import Image
from src.baselines.base import BaselineSample
from src.baselines.unlimited_ocr.adapter import B0UnlimitedOCRBaseline


def test_b0_unlimited_ocr_baseline_run():
    """Verify B0-U baseline executes end-to-end and outputs structured BaselineResult."""
    img = Image.new("RGB", (600, 400), color=(250, 250, 250))
    sample = BaselineSample(
        sample_id="q_u_001",
        document_id="doc_u_001",
        page_idx=0,
        image=img,
        question="What is the total amount?",
        ground_truth_answers=["$1,450.00"]
    )
    baseline = B0UnlimitedOCRBaseline()
    result = baseline.run(sample, run_id="run_u_smoke", seed=42)

    assert result.baseline == "B0-U"
    assert result.document_id == "doc_u_001"
    assert result.model == "Unlimited-OCR"
    assert result.status == "SUCCESS"
    assert "$1,450.00" in result.answer
    assert result.latency_ms is not None
    assert result.latency_ms > 0
