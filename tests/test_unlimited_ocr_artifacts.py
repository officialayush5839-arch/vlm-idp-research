"""Unit Tests for Unlimited-OCR Artifacts and Serialization."""

import json
from src.baselines.base import BaselineResult
from src.evaluation.artifacts import save_run_artifact


def test_save_b0_u_run_artifact(tmp_path):
    """Verify B0-U run artifact serializes properly to JSON matching Section 23/29."""
    res = BaselineResult(
        run_id="run_u_001",
        baseline="B0-U",
        document_id="doc_u_101",
        page_id="page_0",
        question_id="q_u_101",
        model="Unlimited-OCR",
        model_revision="4f9b8c2e1d7a6053b8921e4c70d45f3a9e218c9b",
        prompt_version="grounding-v1",
        prompt_hash="8c2e1d7a6053b892",
        seed=42,
        device="cpu",
        dtype="float32",
        quantization="none",
        answer="$1,450.00",
        ground_truth_answers=["$1,450.00"],
        latency_ms=18.4,
        gpu_peak_memory_mb=None,
        status="SUCCESS"
    )
    artifact_path = save_run_artifact(res, output_dir=str(tmp_path))
    assert artifact_path.exists()

    with open(artifact_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data["baseline"] == "B0-U"
    assert data["model"] == "Unlimited-OCR"
    assert data["status"] == "SUCCESS"
    assert data["latency_ms"] == 18.4
