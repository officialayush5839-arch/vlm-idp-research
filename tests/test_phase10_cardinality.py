"""Unit test for Phase 10 full experiment cardinality and trace accounting."""

import json
from pathlib import Path

TRACES_DIR = Path("experiments/phase10/traces")
MANIFEST_PATH = Path("experiments/phase10/manifests/experiment_manifest.json")


def test_phase10_cardinality():
    assert MANIFEST_PATH.exists()
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    expected_count = manifest["total_experiments"]
    assert expected_count == 625, "Expected exactly 625 planned experiments in Phase 10 matrix"

    actual_traces = list(TRACES_DIR.glob("*.json"))
    assert len(actual_traces) == 625, f"Expected 625 traces on disk, found {len(actual_traces)}"


def test_phase10_trace_checksums():
    import hashlib
    traces = list(TRACES_DIR.glob("*.json"))
    for t in traces[:20]:
        with open(t, "r", encoding="utf-8") as f:
            data = json.load(f)
        assert "sha256" in data
        assert "trace_id" in data
