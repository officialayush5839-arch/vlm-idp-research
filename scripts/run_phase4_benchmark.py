"""
Phase 4 Controlled Degradation Benchmark Execution Script.
Runs the complete authorized experiment matrix across 4 models x 9 degradation families x 5 severities x 5 seeds.
Executes clean reconciliation, observational quality capture, task evaluation, statistical bootstrap, and artifact persistence.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
import time

# Ensure project root is on sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.benchmark.manifest import ManifestManager
from src.benchmark.pipeline import BenchmarkPipeline
from src.core.logging import get_logger

logger = get_logger("phase4_benchmark")


def main():
    print("=" * 70)
    print("PHASE 4 — CONTROLLED DEGRADATION BENCHMARK EXECUTION")
    print("=" * 70)

    t_start = time.perf_counter()

    pipeline = BenchmarkPipeline(
        matrix_config_path="configs/phase4/experiment_matrix.yaml",
        benchmark_config_path="configs/phase4/benchmark_config.yaml",
        execution_config_path="configs/phase4/execution_config.yaml",
    )

    # 1. Manifest and Corpus Initialization
    print("\n--- 1. Generating / Loading Standard Evaluation Corpus ---")
    manifest_mgr = ManifestManager()
    samples = manifest_mgr.generate_standard_evaluation_corpus()
    print(f"Corpus Loaded: {len(samples)} distinct research document samples.")
    for s in samples:
        print(f"  [{s.dataset}] {s.document_id} (Page {s.page_idx + 1}/{s.total_pages}) - Task: {s.task_type}")

    # 2. Pilot & Clean Baseline Reconciliation
    print("\n--- 2. Executing Clean Baseline Reconciliation (S0) ---")
    reconciliation_records = pipeline.run_reconciliation(samples)
    for r in reconciliation_records:
        print(f"  Model {r.model:5s} | {r.metric_name:12s} | Hist: {r.historical_value:.4f} | Measured: {r.phase4_s0_value:.4f} | Diff: {r.difference:.4f} -> [{r.status}]")

    all_pass = all(r.status == "PASS" for r in reconciliation_records)
    if not all_pass:
        print("\n[CRITICAL ERROR] Clean baseline reconciliation failed! Halting Phase 4 execution.")
        sys.exit(1)
    print("Clean Baseline Reconciliation: CONFIRMED PASS across all models.")

    # 3. Full Matrix Execution
    print("\n--- 3. Executing Full Controlled Degradation Benchmark Matrix ---")
    seeds = [42, 123, 456, 789, 101112]
    artifacts, summary = pipeline.run_benchmark(
        clean_samples=samples,
        seeds=seeds,
        resume=True,
    )

    elapsed_s = time.perf_counter() - t_start

    print(f"\n--- 4. Benchmark Execution Summary ---")
    print(f"Total Individual Run Artifacts Generated: {len(artifacts)}")
    print(f"Total Elapsed Time: {elapsed_s:.2f} seconds")
    print(f"Average Processing Time per Condition: {(elapsed_s / max(1, len(artifacts))) * 1000.0:.2f} ms")

    print("\n--- 5. Key Research Robustness Results (Token F1 across Severities) ---")
    print(f"{'Model':8s} | {'Degradation Family':24s} | {'S0':6s} | {'S1':6s} | {'S2':6s} | {'S3':6s} | {'S4':6s}")
    print("-" * 75)
    for row in summary["table_b_robustness"]:
        print(
            f"{row['model']:8s} | {row['degradation_family']:24s} | "
            f"{row['S0']:6.2f} | {row['S1']:6.2f} | {row['S2']:6.2f} | {row['S3']:6.2f} | {row['S4']:6.2f}"
        )

    print("\n--- 6. Statistical Hypothesis Testing (Paired Bootstrap B=10,000) ---")
    for row in summary["table_e_statistical_tests"]:
        print(
            f"  {row['model']:6s} | {row['comparison']:22s} | Delta: {row['observed_delta']:+.4f} | "
            f"95% CI: [{row['ci_95'][0]:+.4f}, {row['ci_95'][1]:+.4f}] | "
            f"Cliff's d: {row['cliffs_delta']:+.4f} ({row['effect_size']}) | Status: {row['status']}"
        )

    print("\n" + "=" * 70)
    print("PHASE 4 BENCHMARK COMPLETED SUCCESSFULLY")
    print("=" * 70)


if __name__ == "__main__":
    main()
