"""Unit Tests for Structured Run Artifacts and Experiment Serialization."""

import json
from pathlib import Path
from src.baselines.base import BaselineResult
from src.evaluation.artifacts import save_run_artifact, save_experiment_summary


def test_save_run_artifact(tmp_path):
    """Verify individual inference result serializes to valid JSON matching Section 29."""
    res = BaselineResult(
        run_id="run_test_001",
        baseline="B2",
        document_id="doc_xyz",
        page_id="page_0",
        question_id="q_101",
        model="Qwen2.5-VL-7B-Instruct",
        model_revision="b450c26581decfcb4c555513ab4deeb85ab1a39d",
        prompt_version="v1.0-b2",
        prompt_hash="a1b2c3d4e5f60718",
        seed=42,
        device="cpu",
        dtype="float32",
        quantization="none",
        answer="Final Answer Text",
        ground_truth_answers=["Final Answer Text"],
        latency_ms=145.2,
        gpu_peak_memory_mb=None,
        status="SUCCESS"
    )

    artifact_path = save_run_artifact(res, output_dir=str(tmp_path))
    assert artifact_path.exists()

    with open(artifact_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data["run_id"] == "run_test_001"
    assert data["baseline"] == "B2"
    assert data["status"] == "SUCCESS"
    assert data["latency_ms"] == 145.2
    assert data["gpu_peak_memory_mb"] is None


def test_save_experiment_summary(tmp_path):
    """Verify batch experiment summary serializes aggregated counts and records."""
    res1 = BaselineResult(
        run_id="run_batch_01",
        baseline="B0",
        document_id="d1",
        page_id="page_0",
        question_id="q1",
        model="OCR_paddle",
        model_revision="2.8.1",
        seed=42,
        device="cpu",
        dtype="string",
        quantization="none",
        answer="Ans 1",
        status="SUCCESS"
    )
    res2 = BaselineResult(
        run_id="run_batch_02",
        baseline="B0",
        document_id="d2",
        page_id="page_0",
        question_id="q2",
        model="OCR_paddle",
        model_revision="2.8.1",
        seed=42,
        device="cpu",
        dtype="string",
        quantization="none",
        answer="",
        status="FAILED",
        error_type="OCR_ERROR"
    )

    summary_file = save_experiment_summary([res1, res2], "E2-SMOKE-B0", output_dir=str(tmp_path))
    assert summary_file.exists()

    with open(summary_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data["experiment_id"] == "E2-SMOKE-B0"
    assert data["total_samples"] == 2
    assert data["successful_runs"] == 1
    assert data["failed_runs"] == 1
