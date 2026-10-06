"""Tests for Phase 12 Trace Integrity and Provenance."""

import json
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).parent.parent
TRACES_DIR = REPO_ROOT / "experiments" / "phase12" / "traces"


def test_traces_count_and_no_duplicates():
    assert TRACES_DIR.exists()
    trace_files = list(TRACES_DIR.glob("*.json"))
    # 6 baselines * 5 seeds * 55 test queries = 1650 traces
    assert len(trace_files) == 1650
    trace_ids = set()
    for tf in trace_files:
        with open(tf, "r", encoding="utf-8") as fp:
            d = json.load(fp)
        t_id = d["trace_id"]
        assert t_id not in trace_ids, f"Duplicate trace ID found: {t_id}"
        trace_ids.add(t_id)
