"""tests/test_phase11_provenance.py
Unit tests verifying trace ID format and cryptographic reproducibility.
"""

from src.safety_recovery.provenance import Phase11ProvenanceTracker


def test_trace_id_generation():
    tid = Phase11ProvenanceTracker.generate_trace_id(
        dataset="docvqa",
        baseline="B11-6",
        document_id="doc_mp_026",
        query_id="q_doc_mp_026",
        domain="D0_in_domain",
        seed=42,
    )
    assert tid == "run_P11_docvqa_b11_6_doc_mp_026_q_doc_mp_026_d0_in_domain_s42"


def test_trace_hash_reproducibility():
    d1 = {"trace_id": "test", "state": "SAFE_RECOVERED", "action": "EMIT_COMPLETE"}
    d2 = {"action": "EMIT_COMPLETE", "state": "SAFE_RECOVERED", "trace_id": "test"}
    h1 = Phase11ProvenanceTracker.compute_sha256(d1)
    h2 = Phase11ProvenanceTracker.compute_sha256(d2)
    assert h1 == h2
