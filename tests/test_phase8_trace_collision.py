import os
import tempfile
import pytest
from src.uncertainty.provenance import save_provenance_trace, TraceCollisionError


def test_trace_collision_detection():
    with tempfile.TemporaryDirectory() as tmpdir:
        trace_payload = {
            "trace_id": "run_P8_test_collision_check",
            "document_id": "doc_01",
            "result": "success",
            "val": 100
        }
        path, h1 = save_provenance_trace(trace_payload, output_dir=tmpdir)
        assert os.path.exists(path)

        # Collision with modified value
        colliding_payload = {
            "trace_id": "run_P8_test_collision_check",
            "document_id": "doc_01",
            "result": "success",
            "val": 999
        }
        with pytest.raises(TraceCollisionError, match="collision detected"):
            save_provenance_trace(colliding_payload, output_dir=tmpdir)
