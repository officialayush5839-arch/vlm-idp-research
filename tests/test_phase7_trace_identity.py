"""
Unit tests for Phase 7 Trace Identity and Collision Resistance.
"""

from src.evidence.provenance import generate_phase7_run_id


def test_trace_identity_uniqueness():
    datasets = ["docvqa", "mmlongbench"]
    baselines = ["B7-0", "B7-1", "B7-5"]
    docs = ["doc1", "doc2"]
    queries = ["q1", "q2"]
    conditions = ["clean", "blur"]
    seeds = [42, 123]

    seen = set()
    total = 0

    for ds in datasets:
        for b in baselines:
            for d in docs:
                for q in queries:
                    for c in conditions:
                        for s in seeds:
                            run_id = generate_phase7_run_id(ds, b, d, q, c, s)
                            assert run_id not in seen, f"Collision detected for {run_id}"
                            seen.add(run_id)
                            total += 1

    assert len(seen) == total
