"""
Unit Tests for Phase 4 Benchmark Schemas and Data Models.
"""

from PIL import Image
import pytest
from src.benchmark.schema import (
    BenchmarkSample,
    BenchmarkRunArtifact,
    DegradationCondition,
    ModelExecutionResult,
    EvaluationMetricsResult,
    ReconciliationRecord,
    TaskType,
    DatasetSplit,
)


def test_benchmark_sample_creation():
    img = Image.new("RGB", (100, 100), color=(255, 255, 255))
    sample = BenchmarkSample(
        sample_id="samp_001",
        document_id="doc_001",
        dataset="DocVQA",
        split="test",
        page_idx=0,
        total_pages=1,
        image=img,
        task_type=TaskType.VQA.value,
        question="What is the total?",
        ground_truth_answers=["$100"],
        ground_truth_bboxes=[[10, 20, 50, 60]],
        source_sha256="abc123hash",
    )

    assert sample.sample_id == "samp_001"
    assert sample.dataset == "DocVQA"
    assert sample.split == "test"
    assert sample.ground_truth_answers == ["$100"]
    assert sample.ground_truth_bboxes == [[10, 20, 50, 60]]


def test_degradation_condition_validation():
    cond = DegradationCondition(
        family="gaussian_blur",
        severity=3,
        parameter_name="sigma",
        parameter_value=4.0,
        seed=42,
    )
    assert cond.family == "gaussian_blur"
    assert cond.severity == 3
    assert cond.parameter_value == 4.0

    with pytest.raises(Exception):
        DegradationCondition(
            family="gaussian_blur",
            severity=5,  # Must be in [0, 4]
            parameter_name="sigma",
            parameter_value=10.0,
        )


def test_benchmark_run_artifact_serialization():
    artifact = BenchmarkRunArtifact(
        experiment_id="E4-DOCVQA-B2-BLUR-S3-SEED42",
        dataset="DocVQA",
        sample_id="samp_001",
        document_id="doc_001",
        page_idx=0,
        split="test",
        model="B2",
        degradation_family="gaussian_blur",
        severity=3,
        seed=42,
        input={"source_sha256": "h1", "derived_sha256": "h2"},
        degradation_params={"sigma": 4.0},
        model_metadata={"model_name": "Qwen2.5-VL-7B-Instruct"},
        prediction="$100",
        ground_truth=["$100"],
        metrics={"token_f1": 1.0, "anls": 1.0},
        runtime={"latency_ms": 25.4, "device": "cpu"},
        status="SUCCESS",
    )

    json_str = artifact.model_dump_json()
    recovered = BenchmarkRunArtifact.model_validate_json(json_str)
    assert recovered.experiment_id == artifact.experiment_id
    assert recovered.prediction == "$100"
    assert recovered.metrics["token_f1"] == 1.0


def test_reconciliation_record():
    rec = ReconciliationRecord(
        model="B2",
        metric_name="ANLS",
        historical_value=1.00,
        phase4_s0_value=0.99,
        difference=0.01,
        tolerance=0.05,
        status="PASS",
    )
    assert rec.status == "PASS"
    assert rec.difference <= rec.tolerance
