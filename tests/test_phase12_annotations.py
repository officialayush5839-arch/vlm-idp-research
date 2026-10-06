"""Tests for Phase 12 Annotation Quality and Double-Annotation."""

import json
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).parent.parent
INDEX_DIR = REPO_ROOT / "data" / "phase12_authentic" / "indexes"


def test_regions_and_normalized_bboxes():
    idx_files = list(INDEX_DIR.glob("*.json"))
    assert len(idx_files) == 260
    sample = idx_files[0]
    with open(sample, "r", encoding="utf-8") as fp:
        doc = json.load(fp)
    for p in doc["pages"]:
        assert len(p["regions"]) >= 2
        for r in p["regions"]:
            bbox = r["bbox"]
            assert len(bbox) == 4
            assert 0 <= bbox[0] < bbox[2] <= 1000
            assert 0 <= bbox[1] < bbox[3] <= 1000
