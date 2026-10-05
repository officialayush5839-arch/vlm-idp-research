"""
Tests for Phase 5.1 Trace Collision Detection (Audit Defect P1-01).
Verifies that overwriting an existing decision trace artifact with conflicting content raises FileExistsError.
"""

import pytest
import tempfile
import shutil
from pathlib import Path

from src.routing.decision_trace import RoutingDecisionTracer
from src.routing.schema import RoutingDecision, RoutingPolicyType


def test_trace_collision_detection_raises_error():
    """Verify that saving conflicting traces to the same run_id triggers FileExistsError."""
    temp_dir = tempfile.mkdtemp()
    try:
        tracer = RoutingDecisionTracer(trace_dir=temp_dir)

        d1 = RoutingDecision(
            run_id="run_P5_1_test_sample_blur_sev2_s42",
            document_id="doc_1",
            page_id="doc_1_p0",
            dataset="sroie",
            partition="test",
            seed=42,
            routing_policy=RoutingPolicyType.R2_RULE_BASED,
            router_version="1.1.0",
            candidate_models=["B0", "B1", "B2"],
            selected_model="B0",
            routing_confidence=0.90,
            decision_reason="Clean sample",
        )
        t1 = tracer.record_trace(d1)
        path1 = tracer.save_trace(t1)
        assert Path(path1).exists()

        # Conflicting decision with same run_id but different selected model
        d2 = RoutingDecision(
            run_id="run_P5_1_test_sample_blur_sev2_s42",
            document_id="doc_1",
            page_id="doc_1_p0",
            dataset="sroie",
            partition="test",
            seed=42,
            routing_policy=RoutingPolicyType.R2_RULE_BASED,
            router_version="1.1.0",
            candidate_models=["B0", "B1", "B2"],
            selected_model="B2",
            routing_confidence=0.50,
            decision_reason="Conflicting decision",
        )
        t2 = tracer.record_trace(d2)

        with pytest.raises(FileExistsError) as exc_info:
            tracer.save_trace(t2)
        assert "collision" in str(exc_info.value).lower()

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)
