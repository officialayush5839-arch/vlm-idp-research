"""Tests for Phase 12 Grouped Partition Integrity."""

import json
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).parent.parent
SPLITS_PATH = REPO_ROOT / "data" / "phase12_authentic" / "splits.json"


def test_family_splits_strictly_disjoint():
    assert SPLITS_PATH.exists()
    with open(SPLITS_PATH, "r", encoding="utf-8") as fp:
        s = json.load(fp)
    tr = set(s["family_splits"]["train"])
    va = set(s["family_splits"]["validation"])
    te = set(s["family_splits"]["test"])
    assert tr.isdisjoint(va)
    assert tr.isdisjoint(te)
    assert va.isdisjoint(te)
    assert len(tr) + len(va) + len(te) == 52


def test_document_counts_match_splits():
    with open(SPLITS_PATH, "r", encoding="utf-8") as fp:
        s = json.load(fp)
    assert len(s["document_splits"]["train"]) == 155
    assert len(s["document_splits"]["validation"]) == 50
    assert len(s["document_splits"]["test"]) == 55
