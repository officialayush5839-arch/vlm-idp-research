import pytest
from src.uncertainty.provenance import generate_trace_id


def test_trace_identity_format_and_uniqueness():
    t1 = generate_trace_id("docvqa", "A5_evidence_aware", "doc_01", "q_1", "clean", 42)
    t2 = generate_trace_id("docvqa", "A5_evidence_aware", "doc_01", "q_1", "clean", 123)
    t3 = generate_trace_id("docvqa", "A5_evidence_aware", "doc_01", "q_2", "clean", 42)
    t4 = generate_trace_id("docvqa", "A5_evidence_aware", "doc_02", "q_1", "clean", 42)

    assert t1.startswith("run_P8_docvqa_A5_evidence_aware_doc_01_q_1_clean_s42")
    assert t1 != t2
    assert t1 != t3
    assert t1 != t4
