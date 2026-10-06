"""tests/test_phase10_5_trace_collision.py
Unit tests verifying that no trace collision occurs across baseline-condition tuples.
"""

from src.recovery.provenance import RecoveryProvenanceTracker


def test_trace_id_uniqueness():
    seeds = [42, 123, 456]
    baselines = ["B10.5-0", "B10.5-1", "B10.5-2", "B10.5-5"]
    domains = ["D0_in_domain", "D2_visual_style_shift", "D4_combined_shift"]

    ids = set()
    for s in seeds:
        for b in baselines:
            for d in domains:
                tid = RecoveryProvenanceTracker.generate_trace_id(
                    dataset="docvqa",
                    domain=d,
                    baseline=b,
                    document_id="doc_mp_026",
                    query_id="q_doc_mp_026",
                    strategy="default",
                    condition="standard",
                    seed=s,
                )
                assert tid not in ids, f"Collision detected for trace ID: {tid}"
                ids.add(tid)
