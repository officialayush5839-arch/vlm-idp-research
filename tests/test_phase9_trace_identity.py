"""Tests for trace identity, provenance, and collision prevention."""

import tempfile
from pathlib import Path
import pytest
from src.reliability.provenance import ProvenanceTracker


def test_trace_id_generation_format():
    trace_id = ProvenanceTracker.generate_trace_id(
        dataset="synthetic_multipage",
        baseline="B9-5",
        doc_id="doc_001",
        query_id="q_002",
        condition="clean",
        seed=42,
    )
    assert trace_id == "run_P9_synthetic_multipage_B9_5_doc_001_q_002_clean_s42"


def test_provenance_registration_and_collision():
    with tempfile.TemporaryDirectory() as tmpdir:
        tracker = ProvenanceTracker(trace_dir=Path(tmpdir))
        trace_id = "run_P9_synthetic_multipage_B9_5_doc_001_q_001_clean_s42"
        data = {"output": "verified", "score": 0.95}

        # First registration should succeed
        p = tracker.register_trace(trace_id, data)
        assert p.exists()

        # Second registration of same ID in-memory should fail
        with pytest.raises(ValueError, match="Trace ID collision"):
            tracker.register_trace(trace_id, data)

        # Fresh tracker against same disk path should raise FileExistsError
        tracker2 = ProvenanceTracker(trace_dir=Path(tmpdir))
        with pytest.raises(FileExistsError):
            tracker2.register_trace(trace_id, data)
