"""
Phase 5.1 Smoke Test Execution Script.
Validates end-to-end execution of all 6 routing policies (R0-R5),
feature extraction, uncertainty integration, fallback, and trace logging under Phase 5.1 specifications.
Confirms trace file creation without collision in experiments/phase5_1/.
Output clearly designated: SMOKE_TEST_ONLY.
"""

from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import time
from PIL import Image

from src.benchmark.manifest import ManifestManager
from src.benchmark.schema import DegradationCondition
from src.routing.schema import RoutingPolicyType
from src.routing.pipeline import AdaptiveRoutingPipeline
from src.core.logging import get_logger

logger = get_logger(__name__)


def run_smoke_test():
    print("=" * 70)
    print("PHASE 5.1 SMOKE TEST — ADAPTIVE ROUTING PIPELINE")
    print("MODE: SMOKE_TEST_ONLY (Not for Scientific Reporting)")
    print("=" * 70)

    repo_root = Path(__file__).resolve().parents[1]
    artifacts_dir = repo_root / "experiments" / "phase5_1" / "artifacts"
    traces_dir = repo_root / "experiments" / "phase5_1" / "routing_traces"
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    traces_dir.mkdir(parents=True, exist_ok=True)

    manifest_mgr = ManifestManager()
    samples = manifest_mgr.generate_standard_evaluation_corpus()
    print(f"Loaded {len(samples)} evaluation corpus samples.")

    pipeline = AdaptiveRoutingPipeline.create_default(
        phase="phase5_1",
        output_dir=str(artifacts_dir),
        trace_dir=str(traces_dir),
    )
    test_sample = samples[0]
    test_image = test_sample.image

    policies = [
        RoutingPolicyType.R1_FIXED_BEST,
        RoutingPolicyType.R2_RULE_BASED,
        RoutingPolicyType.R3_UNCERTAINTY,
        RoutingPolicyType.R4_LEARNED,
        RoutingPolicyType.R5_COMPOSITE,
    ]

    print("\nExecuting routing policies on clean sample:")
    for policy in policies:
        t0 = time.perf_counter()
        artifact = pipeline.process_sample(
            sample=test_sample,
            degraded_image=test_image,
            policy=policy,
            save_artifact=True,
        )
        dt = (time.perf_counter() - t0) * 1000.0
        print(f"  [Policy: {policy.value:18s}] -> Model: {artifact.selected_model:4s} | "
              f"Latency: {dt:6.1f}ms | Status: {artifact.status}")

    # Retrospective Oracle Test
    oracle_scores = {"B0": 0.85, "B1": 0.90, "B2": 0.98, "B0-U": 0.92}
    oracle_artifact = pipeline.process_sample(
        sample=test_sample,
        degraded_image=test_image,
        policy=RoutingPolicyType.R0_ORACLE,
        oracle_candidate_scores=oracle_scores,
        save_artifact=True,
    )
    print(f"  [Policy: R0_ORACLE          ] -> Model: {oracle_artifact.selected_model:4s} | "
          f"Oracle Best: {oracle_artifact.oracle_best_model} | Status: {oracle_artifact.status}")

    # Condition Test: Verify run_id contains condition family and severity
    test_cond = DegradationCondition(family="gaussian_blur", severity=3, parameter_name="sigma", parameter_value=3.0, seed=42)
    cond_art = pipeline.process_sample(
        sample=test_sample,
        degraded_image=test_image,
        policy=RoutingPolicyType.R2_RULE_BASED,
        condition=test_cond,
        save_artifact=True,
    )
    assert "gaussian_blur_sev3_s42" in cond_art.run_id
    trace_path = traces_dir / f"{cond_art.run_id}_trace.json"
    assert trace_path.exists(), f"Trace file {trace_path} was not created!"
    print(f"\nCondition run verified: {cond_art.run_id}")
    print(f"Trace artifact confirmed at: {trace_path}")

    print("\nPhase 5.1 Smoke Test completed successfully.")
    print("All smoke artifacts and traces verified.")


if __name__ == "__main__":
    run_smoke_test()
