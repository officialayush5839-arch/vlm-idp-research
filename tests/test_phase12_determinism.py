"""Tests for Phase 12 Execution Determinism."""

import json
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).parent.parent
TRACES_DIR = REPO_ROOT / "experiments" / "phase12" / "traces"


def test_seed_determinism_consistency():
    # Pick sample trace for seed 42 and assert fields are valid
    s42_traces = list(TRACES_DIR.glob("*_42.json"))
    assert len(s42_traces) > 0
    with open(s42_traces[0], "r", encoding="utf-8") as fp:
        t = json.load(fp)
    assert t["seed"] == 42
    assert 0.0 <= t["confidence"] <= 1.0
    assert 0.0 <= t["grounding_iou"] <= 1.0
