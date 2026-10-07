"""Tests for Phase 14 Physical CUDA Systems, Benchmark Integrity & Safety."""

import csv
import json
from pathlib import Path
import pytest

from src.phase14.hardware_gate import inspect_hardware_gate
from src.phase14.timing import PhysicalStageProfiler
from src.phase14.telemetry import PhysicalCUDAMonitor
from src.phase14.audit import run_static_ast_leakage_audit, run_runtime_adversarial_sentinel_audit

REPO_ROOT = Path(__file__).parent.parent
TABLES_DIR = REPO_ROOT / "experiments" / "phase14" / "tables"
FIGURES_DIR = REPO_ROOT / "experiments" / "phase14" / "figures"
TRACES_FILE = REPO_ROOT / "experiments" / "phase14" / "traces" / "physical_inference_traces.jsonl"


def test_phase14_hardware_gate():
    hw = inspect_hardware_gate()
    assert "os_name" in hw
    assert "python_version" in hw
    assert "physical_gpu_detected" in hw
    assert hw["physical_gpu_detected"] is True
    assert "RTX 3050" in hw["gpu_model"]
    assert hw["gpu_total_vram_mb"] == 6144


def test_phase14_timing_profiler():
    profiler = PhysicalStageProfiler(use_cuda_sync=False)
    profiler.start_stage("test_stage")
    import time
    time.sleep(0.005)
    dur = profiler.end_stage("test_stage")
    assert dur > 0.004
    summary = profiler.get_summary()
    assert "test_stage" in summary
    assert summary["test_stage"]["count"] == 1
    assert summary["test_stage"]["mean_ms"] > 4.0


def test_phase14_telemetry_monitor():
    monitor = PhysicalCUDAMonitor(device_id=0)
    assert monitor.device_id == 0
    stats = monitor.get_cuda_memory_mb()
    assert "allocated_mb" in stats
    assert "reserved_mb" in stats
    assert "max_allocated_mb" in stats


def test_phase14_ast_and_sentinel_audits():
    ast_findings = run_static_ast_leakage_audit()
    assert len(ast_findings) == 0, f"Found AST leakage in phase14: {ast_findings}"
    sentinel_findings = run_runtime_adversarial_sentinel_audit()
    assert len(sentinel_findings) == 0, f"Found sentinel leak: {sentinel_findings}"


def test_phase14_traces_integrity():
    assert TRACES_FILE.exists()
    records = []
    with open(TRACES_FILE, "r", encoding="utf-8") as f:
        for line in f:
            records.append(json.loads(line))
    assert len(records) == 1100

    exp_ids = set()
    for rec in records:
        assert rec["experiment_id"] not in exp_ids
        exp_ids.add(rec["experiment_id"])
        assert "condition" in rec
        assert "seed" in rec
        assert "physical_latency_s" in rec
        assert "exact_match_accuracy" in rec
        assert "grounding_iou" in rec
        assert "unsupported_answer_rate" in rec
        assert "safe_useful_coverage" in rec


def test_phase14_tables_all_15_exist():
    assert TABLES_DIR.exists()
    for i in range(1, 16):
        pattern = f"table_{i:02d}_*.csv"
        matching = list(TABLES_DIR.glob(pattern))
        assert len(matching) == 1, f"Missing table {i:02d} in {TABLES_DIR}"
        with open(matching[0], "r", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        assert len(rows) > 0, f"Table {matching[0].name} is empty"


def test_phase14_figures_all_12_exist():
    assert FIGURES_DIR.exists()
    for i in range(1, 13):
        pattern = f"fig_{i:02d}_*.png"
        matching = list(FIGURES_DIR.glob(pattern))
        assert len(matching) == 1, f"Missing figure {i:02d} in {FIGURES_DIR}"
        assert matching[0].stat().st_size > 1000, f"Figure {matching[0].name} is too small"


def test_phase14_quantization_matrix_empirical_values():
    q_csv = TABLES_DIR / "table_04_quantization_matrix.csv"
    assert q_csv.exists()
    with open(q_csv, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 3
    row_map = {r["Precision"]: float(r["Peak_VRAM_MB"]) for r in rows}
    fp16_vram = row_map["Q0_FP16"]
    int8_vram = row_map["Q1_INT8"]
    int4_vram = row_map["Q2_INT4"]
    assert int4_vram < int8_vram < fp16_vram
    assert int4_vram < 600.0


def test_phase14_retrieval_and_safety_gains():
    e2e_csv = TABLES_DIR / "table_12_end_to_end.csv"
    assert e2e_csv.exists()
    with open(e2e_csv, "r", encoding="utf-8") as f:
        rows = {r["Condition"]: r for r in csv.DictReader(f)}

    b14_a = rows["B14-A"]
    b14_b = rows["B14-B"]
    b14_c = rows["B14-C"]
    b14_d = rows["B14-D"]

    # Context pruning speedup
    assert float(b14_b["Page_Reduction_Pct"]) == 60.0
    assert float(b14_b["Latency_s"]) < float(b14_a["Latency_s"])

    # Accuracy improvement
    assert float(b14_b["Exact_Match"]) > float(b14_a["Exact_Match"])

    # Grounding IoU improvement
    assert float(b14_c["Grounding_IoU"]) > float(b14_a["Grounding_IoU"])

    # Hallucination suppression
    assert float(b14_d["Unsupported_Rate"]) < float(b14_a["Unsupported_Rate"])
    assert float(b14_d["Unsupported_Rate"]) < 0.05
    assert float(b14_d["Safe_Useful_Coverage"]) > 0.85


def test_phase14_statistical_hypotheses():
    stats_csv = TABLES_DIR / "table_13_statistical_tests.csv"
    assert stats_csv.exists()
    with open(stats_csv, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 2
    for row in rows:
        assert row["Decision"] == "SUPPORTED"
        assert float(row["P_Value"]) < 0.05
