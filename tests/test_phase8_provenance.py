import os
import tempfile
import pytest
from src.uncertainty.provenance import (
    generate_trace_id,
    save_provenance_trace,
    TraceCollisionError
)


def test_generate_trace_id():
    trace_id = generate_trace_id(
        dataset="docvqa",
        baseline="A5_evidence_aware",
        doc_id="doc_001",
        query_id="q_101",
        condition="motion_blur_sev3",
        seed=42
    )
    assert trace_id == "run_P8_docvqa_A5_evidence_aware_doc_001_q_101_motion_blur_sev3_s42"


def test_save_provenance_trace_collision_prevention():
    with tempfile.TemporaryDirectory() as tmpdir:
        trace_id = "run_P8_test_001"
        payload1 = {"trace_id": trace_id, "confidence": 0.85, "data": "original"}
        payload2 = {"trace_id": trace_id, "confidence": 0.40, "data": "tampered_collision"}

        # First save succeeds
        file_path, sha = save_provenance_trace(payload1, output_dir=tmpdir)
        assert os.path.exists(file_path)
        assert len(sha) == 64

        # Identical payload save is idempotent / safe
        f2, sha2 = save_provenance_trace(payload1, output_dir=tmpdir)
        assert sha2 == sha

        # Conflicting payload save raises TraceCollisionError
        with pytest.raises(TraceCollisionError, match="collision detected"):
            save_provenance_trace(payload2, output_dir=tmpdir)
