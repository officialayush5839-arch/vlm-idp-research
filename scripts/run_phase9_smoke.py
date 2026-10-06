"""Smoke test script for Phase 9 Reliability Pipeline."""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.reliability.pipeline import ReliabilityPipeline
from src.reliability.schema import ReliabilityAction


def run_smoke():
    print("[Phase 9 Smoke] Initializing ReliabilityPipeline...")
    pipeline = ReliabilityPipeline()

    p3_sample = {"quality_score": 0.88}
    p6_sample = {"retrieval_score": 0.82}
    p7_sample = {
        "sufficiency_score": 0.90,
        "spatial_overlap": 0.85,
        "semantic_similarity": 0.88,
        "numeric_discrepancy": 0.0,
        "table_alignment_score": 0.95,
    }
    p8_sample = {"raw_confidence": 0.87, "agreement_score": 0.92}

    pkg = pipeline.process(
        doc_id="doc_mp_001",
        query_id="q_001",
        phase3_output=p3_sample,
        phase6_output=p6_sample,
        phase7_output=p7_sample,
        phase8_output=p8_sample,
    )

    print(f"[Phase 9 Smoke] Action: {pkg.decision.action.value}")
    print(f"[Phase 9 Smoke] Calibrated Confidence: {pkg.calibrated_confidence:.4f}")
    print(f"[Phase 9 Smoke] Uncertainty Norm: {pkg.uncertainty_vector.l2_norm:.4f}")
    print(f"[Phase 9 Smoke] Primary Failure Diagnosed: {pkg.failure_mode.primary_failure}")

    assert pkg.decision.action in ReliabilityAction
    assert 0.0 <= pkg.calibrated_confidence <= 1.0
    print("[Phase 9 Smoke] Smoke test PASSED successfully!")


if __name__ == "__main__":
    run_smoke()
