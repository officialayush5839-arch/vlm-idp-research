"""
Unit tests for Cryptographic Provenance and Run ID generation.
"""

from src.retrieval.provenance import (
    generate_phase6_run_id,
    create_retrieval_provenance,
    compute_sha256
)


def test_generate_phase6_run_id():
    run_id = generate_phase6_run_id(
        dataset="synthetic-multipage",
        method="B6-5",
        document_id="doc-42",
        query_id="q-007",
        seed=123
    )
    assert run_id == "run_P6_synthetic_multipage_b6_5_doc_42_q_007_s123"


def test_create_retrieval_provenance():
    prov = create_retrieval_provenance(
        dataset="docvqa",
        method="B6-1",
        document_id="doc_1",
        query_id="q_1",
        seed=42,
        config_dict={"alpha": 0.6},
        document_content="test document",
        query_content="test query"
    )

    assert prov["run_id"] == "run_P6_docvqa_b6_1_doc_1_q_1_s42"
    assert prov["phase"] == "6"
    assert "git_commit" in prov
    assert len(prov["document_hash"]) == 16
    assert len(prov["query_hash"]) == 16
    assert len(prov["config_hash"]) == 16


def test_provenance_collision_prevention():
    id1 = generate_phase6_run_id("docvqa", "B6-1", "doc1", "q1", 42)
    id2 = generate_phase6_run_id("docvqa", "B6-2", "doc1", "q1", 42)
    id3 = generate_phase6_run_id("docvqa", "B6-1", "doc1", "q1", 123)
    assert id1 != id2
    assert id1 != id3
