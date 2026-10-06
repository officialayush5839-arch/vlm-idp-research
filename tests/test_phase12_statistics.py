"""Tests for Phase 12 Cluster-Aware Statistics and Hypothesis Decisions."""

import json
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).parent.parent
HYP_PATH = REPO_ROOT / "experiments" / "phase12" / "results" / "hypothesis_decisions.json"
GAP_PATH = REPO_ROOT / "experiments" / "phase12" / "results" / "synthetic_vs_authentic_gap.json"


def test_hypotheses_decisions_evaluated():
    assert HYP_PATH.exists()
    with open(HYP_PATH, "r", encoding="utf-8") as fp:
        hyp = json.load(fp)
    for h_id in ["H12-1", "H12-2", "H12-3", "H12-4", "H12-5"]:
        assert h_id in hyp
        assert hyp[h_id]["decision"] in {"SUPPORTED", "PARTIALLY_SUPPORTED", "NOT_SUPPORTED", "INCONCLUSIVE"}


def test_synthetic_authentic_gap_computed():
    assert GAP_PATH.exists()
    with open(GAP_PATH, "r", encoding="utf-8") as fp:
        gap = json.load(fp)
    assert "retrieval_recall_at_5" in gap
    assert "grounding_mean_iou" in gap
    assert "selective_accuracy" in gap
    assert "safe_useful_coverage" in gap
