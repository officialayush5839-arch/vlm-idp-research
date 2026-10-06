"""scripts/run_phase10_5_analysis.py
Independent trace verification and cryptographic audit for Phase 10.5.
Recomputes metrics across all 750 individual trace files from experiments/phase10_5/traces/.
Validates SHA-256 hashes and cross-checks summary totals.
"""

import os
import glob
import json
import hashlib
import numpy as np

def audit_traces():
    print("=== Running Phase 10.5 Independent Trace Audit ===")
    trace_files = glob.glob("experiments/phase10_5/traces/*.json")
    print(f"Discovered {len(trace_files)} trace files.")
    assert len(trace_files) == 750, f"Expected 750 traces, found {len(trace_files)}"

    baselines = {}
    corrupted_hashes = 0

    for tf in trace_files:
        with open(tf, "r", encoding="utf-8") as f:
            data = json.load(f)

        stored_hash = data.get("sha256")
        data_copy = {k: v for k, v in data.items() if k != "sha256"}
        computed_hash = hashlib.sha256(json.dumps(data_copy, sort_keys=True).encode("utf-8")).hexdigest()

        if stored_hash != computed_hash:
            corrupted_hashes += 1

        b_id = data["baseline"]
        dom = data["domain"]
        k = (b_id, dom)
        if k not in baselines:
            baselines[k] = {"total": 0, "useful": 0, "safe_useful": 0, "unsafe": 0}

        baselines[k]["total"] += 1
        if data["is_useful"]:
            baselines[k]["useful"] += 1
            if data["is_correct"]:
                baselines[k]["safe_useful"] += 1
            else:
                baselines[k]["unsafe"] += 1

    print(f"Hash validation complete. Corrupted traces: {corrupted_hashes}")
    assert corrupted_hashes == 0, f"Found {corrupted_hashes} corrupted trace files!"

    # Cross check with summary JSON
    with open("experiments/phase10_5/results/recovery_benchmark_summary.json", "r", encoding="utf-8") as f:
        summary = json.load(f)

    max_diff = 0.0
    for (b_id, dom), counts in baselines.items():
        sum_m = summary[b_id][dom]
        computed_suc = counts["safe_useful"] / counts["total"]
        reported_suc = sum_m["safe_useful_coverage"]
        diff = abs(computed_suc - reported_suc)
        if diff > max_diff:
            max_diff = diff

    print(f"Maximum discrepancy between independent audit and summary: {max_diff}")
    assert max_diff <= 1e-10, f"Audit discrepancy {max_diff} exceeded tolerance!"
    print("Trace verification audit: 100% PASSED.")


if __name__ == "__main__":
    audit_traces()
