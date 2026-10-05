"""
Unit tests for Phase 7 Provenance and Trace Identification.
"""

from src.evidence.provenance import (
    compute_sha256,
    compute_evidence_unit_hash,
    generate_phase7_run_id,
    build_provenance_record,
    get_git_commit
)


def test_compute_sha256():
    h1 = compute_sha256("test_string")
    h2 = compute_sha256("test_string")
    assert h1 == h2
    assert len(h1) == 64


def test_compute_evidence_unit_hash():
    h = compute_evidence_unit_hash(
        document_id="doc_1",
        page_id=2,
        region_id="reg_a",
        bbox_1000=(100, 100, 500, 500),
        text="Sample text content"
    )
    assert len(h) == 64


def test_generate_phase7_run_id():
    run_id = generate_phase7_run_id(
        dataset="DocVQA",
        baseline="B7-5",
        document_id="doc-42",
        query_id="q-10",
        condition="severe_blur",
        seed=42
    )
    assert run_id == "run_P7_docvqa_b7_5_doc_42_q_10_severe_blur_s42"


def test_build_provenance_record():
    rec = build_provenance_record(
        dataset="docvqa",
        baseline="B7-5",
        document_id="doc1",
        query_id="q1",
        condition="clean",
        seed=42,
        extra_metadata={"notes": "test"}
    )
    assert rec["phase"] == "PHASE_7"
    assert "record_hash" in rec
    assert rec["git_commit"] != ""
