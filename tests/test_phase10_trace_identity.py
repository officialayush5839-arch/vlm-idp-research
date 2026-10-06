"""Unit tests for Phase 10 trace identity and collision prevention."""

import tempfile
from pathlib import Path
import pytest
from src.robustness.provenance import RobustnessProvenanceTracker


def test_phase10_trace_id_generation():
    trace_id = RobustnessProvenanceTracker.generate_trace_id(
        domain="D1_layout_shift",
        baseline="B10-4",
        doc_id="doc_mp_027",
        query_id="q_doc_mp_027",
        condition="moderate",
        seed=42,
    )
    assert trace_id == "run_P10_d1_layout_shift_B10_4_doc_mp_027_q_doc_mp_027_moderate_s42"


def test_phase10_trace_collision_prevention():
    with tempfile.TemporaryDirectory() as tmpdir:
        tracker = RobustnessProvenanceTracker(trace_dir=Path(tmpdir))
        t_id = "run_P10_d0_B10_0_doc_01_q_01_clean_s42"
        data = {"score": 0.8}

        p = tracker.register_trace(t_id, data)
        assert p.exists()

        with pytest.raises(ValueError, match="Trace ID collision"):
            tracker.register_trace(t_id, data)
