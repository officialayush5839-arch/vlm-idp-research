"""
Phase 4 Controlled Degradation Benchmark Subsystem.
"""

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
from src.benchmark.manifest import ManifestManager, compute_sha256, compute_file_sha256
from src.benchmark.degradation_runner import DegradationRunner, transform_bbox_geometric
from src.benchmark.model_runner import ModelRunner
from src.benchmark.evaluator import BenchmarkEvaluator
from src.benchmark.quality_capture import QualityCaptureHook
from src.benchmark.reconciliation import BaselineReconciler
from src.benchmark.statistics import (
    paired_bootstrap_test,
    compute_cliffs_delta,
    compute_cohens_d,
    test_hypothesis_h1_trend,
)
from src.benchmark.aggregator import BenchmarkAggregator
from src.benchmark.pipeline import BenchmarkPipeline

__all__ = [
    "BenchmarkSample",
    "BenchmarkRunArtifact",
    "DegradationCondition",
    "ModelExecutionResult",
    "EvaluationMetricsResult",
    "ReconciliationRecord",
    "TaskType",
    "DatasetSplit",
    "ManifestManager",
    "compute_sha256",
    "compute_file_sha256",
    "DegradationRunner",
    "transform_bbox_geometric",
    "ModelRunner",
    "BenchmarkEvaluator",
    "QualityCaptureHook",
    "BaselineReconciler",
    "paired_bootstrap_test",
    "compute_cliffs_delta",
    "compute_cohens_d",
    "test_hypothesis_h1_trend",
    "BenchmarkAggregator",
    "BenchmarkPipeline",
]
