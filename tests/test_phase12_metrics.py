"""Tests for Phase 12 Benchmark Metrics and Figures."""

import json
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).parent.parent
RES_PATH = REPO_ROOT / "experiments" / "phase12" / "results" / "benchmark_summary.json"
FIG_DIR = REPO_ROOT / "experiments" / "phase12" / "figures"


def test_benchmark_summary_baselines():
    assert RES_PATH.exists()
    with open(RES_PATH, "r", encoding="utf-8") as fp:
        res = json.load(fp)
    for b in ["B12-0", "B12-1", "B12-2", "B12-3", "B12-4", "B12-5"]:
        assert b in res
        assert res[b]["total_runs"] == 275  # 55 test queries * 5 seeds


def test_all_publication_figures_exist():
    assert FIG_DIR.exists()
    for i in range(1, 10):
        pngs = list(FIG_DIR.glob(f"fig{i}_*.png"))
        assert len(pngs) == 1, f"Figure {i} missing from {FIG_DIR}"
