"""
Unit tests for Phase 6 Trace Identity and Cardinality.
Verifies that all retrieval executions generate unique, fully traceable run identifiers.
"""

from src.retrieval.provenance import generate_phase6_run_id


def test_unique_trace_cardinality():
    datasets = ["synthetic_multipage", "docvqa"]
    methods = ["B6-0", "B6-1", "B6-2", "B6-3", "B6-4", "B6-5"]
    seeds = [42, 123, 999]
    num_queries = 10

    run_ids = set()
    total_calls = 0

    for ds in datasets:
        for m in methods:
            for s in seeds:
                for q_idx in range(num_queries):
                    doc_id = f"doc_{q_idx // 2}"
                    q_id = f"q_{q_idx}"
                    rid = generate_phase6_run_id(ds, m, doc_id, q_id, s)
                    run_ids.add(rid)
                    total_calls += 1

    # Ensure zero collisions: number of unique IDs equals total combinations
    assert len(run_ids) == total_calls
