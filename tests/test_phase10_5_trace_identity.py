"""tests/test_phase10_5_trace_identity.py
Unit tests verifying Phase 10.5 trace ID format and reproducibility.
"""

from src.recovery.provenance import RecoveryProvenanceTracker


def test_trace_id_format():
    trace_id = RecoveryProvenanceTracker.generate_trace_id(
        dataset="docvqa",
        domain="d2_visual_style_shift",
        baseline="B10.5-5",
        document_id="doc_mp_028",
        query_id="q_doc_mp_028",
        strategy="preprocessing_restoration",
        condition="severe",
        seed=42,
    )
    assert trace_id.startswith("run_P10_5_docvqa_d2_visual_style_shift_b10_5_5_")
    assert "_s42" in trace_id
    assert "doc_mp_028" in trace_id


def test_trace_hash_deterministic():
    data1 = {"trace_id": "test_id", "confidence": 0.85, "action": "EMIT_COMPLETE"}
    data2 = {"action": "EMIT_COMPLETE", "trace_id": "test_id", "confidence": 0.85}
    h1 = RecoveryProvenanceTracker.compute_sha256(data1)
    h2 = RecoveryProvenanceTracker.compute_sha256(data2)
    assert h1 == h2
