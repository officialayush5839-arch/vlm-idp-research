"""Tests for Phase 12 Duplicate Detection."""

import json
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).parent.parent
SPLITS_PATH = REPO_ROOT / "data" / "phase12_authentic" / "splits.json"


def test_zero_exact_duplicates():
    with open(SPLITS_PATH, "r", encoding="utf-8") as fp:
        s = json.load(fp)
    assert s["duplicate_audit"]["exact_duplicate_count"] == 0
    assert len(s["duplicate_audit"]["duplicates_flagged"]) == 0
