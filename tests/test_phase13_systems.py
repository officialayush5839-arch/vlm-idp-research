"""Tests for Phase 13 Systems Infrastructure & Benchmark Integrity."""

import json
from pathlib import Path
import pytest

from src.phase13.hardware import detect_hardware_environment
from src.phase13.profiler import SystemsProfiler
from src.phase13.model_loader import VLMModelLoader
from src.phase13.audit import run_static_ast_leakage_audit, run_runtime_adversarial_audit

REPO_ROOT = Path(__file__).parent.parent
METRICS_PATH = REPO_ROOT / "experiments" / "phase13" / "metrics" / "phase13_summary_metrics.json"
TABLES_DIR = REPO_ROOT / "experiments" / "phase13" / "tables"
FIGURES_DIR = REPO_ROOT / "experiments" / "phase13" / "figures"
TRACES_DIR = REPO_ROOT / "experiments" / "phase13" / "traces"


def test_hardware_detection_honest():
    hw = detect_hardware_environment()
    assert "os" in hw
    assert "python_version" in hw
    assert hw["cuda_available_in_pytorch"] is False
    assert hw["physical_gpu_detected"] is True
    assert "RTX 3050" in hw["gpu_model"]


def test_systems_profiler_stage_timing():
    prof = SystemsProfiler(use_cuda_sync=False)
    prof.start_stage("test_stage")
    import time
    time.sleep(0.001)
    elapsed = prof.end_stage("test_stage")
    assert elapsed > 0.0
    summary = prof.get_summary()
    assert "test_stage" in summary["stage_latencies_ms"]
    assert summary["cuda_synchronized"] is False


def test_model_loader_hardware_gating():
    loader = VLMModelLoader(precision="INT4")
    res = loader.load_model()
    assert res["status"] == "NOT_EXECUTED — REQUIRED HARDWARE UNAVAILABLE"
    assert loader.hardware_gated is True


def test_zero_leakage_audits():
    s_findings = run_static_ast_leakage_audit()
    assert len(s_findings) == 0, f"Static leakage: {s_findings}"
    r_findings = run_runtime_adversarial_audit()
    assert len(r_findings) == 0, f"Runtime leakage: {r_findings}"


def test_traces_integrity_and_count():
    assert TRACES_DIR.exists()
    trace_files = list(TRACES_DIR.glob("*.json"))
    assert len(trace_files) == 1650
    # Assert zero duplicate IDs
    trace_ids = set()
    for tf in trace_files[:50]:
        with open(tf, "r", encoding="utf-8") as fp:
            d = json.load(fp)
        assert d["trace_id"] not in trace_ids
        trace_ids.add(d["trace_id"])


def test_machine_readable_tables_all_exist():
    assert TABLES_DIR.exists()
    for i in range(1, 12):
        csv_file = TABLES_DIR / f"table_{i:02d}_*.csv"
        matching = list(TABLES_DIR.glob(f"table_{i:02d}_*.csv"))
        assert len(matching) == 1, f"Table {i:02d} missing from {TABLES_DIR}"


def test_publication_figures_all_exist():
    assert FIGURES_DIR.exists()
    for i in range(1, 11):
        matching = list(FIGURES_DIR.glob(f"fig{i}_*.png"))
        assert len(matching) == 1, f"Figure {i} missing from {FIGURES_DIR}"


def test_baseline_summary_metrics_values():
    assert METRICS_PATH.exists()
    with open(METRICS_PATH, "r", encoding="utf-8") as fp:
        m = json.load(fp)
    assert "B13-1" in m
    assert "B13-5" in m
    assert m["B13-5"]["accuracy"] > m["B13-1"]["accuracy"]
    assert m["B13-5"]["unsupported_rate"] < m["B13-1"]["unsupported_rate"]
    assert m["B13-5"]["page_reduction_pct"] == 60.0
