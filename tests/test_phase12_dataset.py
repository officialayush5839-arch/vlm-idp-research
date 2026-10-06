"""Tests for Phase 12 Authentic Dataset Architecture."""

import json
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).parent.parent
MANIFEST_PATH = REPO_ROOT / "data" / "phase12_authentic" / "corpus_manifest.json"


def test_manifest_exists_and_scale():
    assert MANIFEST_PATH.exists()
    with open(MANIFEST_PATH, "r", encoding="utf-8") as fp:
        m = json.load(fp)
    assert m["total_families"] == 52
    assert m["total_documents"] == 260
    assert m["total_pages"] == 1300
    assert len(m["documents"]) == 260
    assert len(m["queries"]) == 260


def test_modalities_present():
    with open(MANIFEST_PATH, "r", encoding="utf-8") as fp:
        m = json.load(fp)
    mod_codes = set(doc["modality"] for doc in m["documents"])
    expected_mods = {"D12-0", "D12-1", "D12-2", "D12-3", "D12-4", "D12-5", "D12-6"}
    assert mod_codes == expected_mods
