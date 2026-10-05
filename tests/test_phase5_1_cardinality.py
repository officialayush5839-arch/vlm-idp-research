"""
Tests for Phase 5.1 Trace Cardinality and Trace Completeness (Audit Defect P1-01).
Verifies that multiple conditions across seeds produce the exact expected number
of distinct trace files without collision or truncation.
"""

from pathlib import Path
import tempfile
import shutil
from PIL import Image

from src.benchmark.schema import BenchmarkSample, DegradationCondition
from src.routing.schema import RoutingPolicyType
from src.routing.pipeline import AdaptiveRoutingPipeline


def test_trace_cardinality_no_overwriting():
    """Verify that a batch of distinct conditions produces an exact matching number of trace artifacts."""
    temp_dir = tempfile.mkdtemp()
    try:
        pipeline = AdaptiveRoutingPipeline.create_default(
            phase="phase5_1",
            output_dir=str(Path(temp_dir) / "artifacts"),
            trace_dir=str(Path(temp_dir) / "routing_traces"),
        )

        sample = BenchmarkSample(
            sample_id="sample_cardinality",
            document_id="doc_cardinality",
            dataset="sroie",
            split="test",
            page_idx=0,
            question="Total?",
            answers=["100"],
            source_sha256="dummy_cardinality_hash",
        )

        families = ["gaussian_blur", "gaussian_noise", "skew_rotation"]
        severities = [1, 2, 3]
        seeds = [42, 43]

        total_expected = len(families) * len(severities) * len(seeds)
        dummy_img = Image.new("RGB", (64, 64), color=(255, 255, 255))

        generated_ids = []
        for fam in families:
            for sev in severities:
                for s in seeds:
                    cond = DegradationCondition(
                        family=fam, severity=sev, parameter_name="param", parameter_value=float(sev), seed=s
                    )
                    art = pipeline.process_sample(
                        sample=sample,
                        degraded_image=dummy_img,
                        policy=RoutingPolicyType.R1_FIXED_BEST,
                        condition=cond,
                        save_artifact=True,
                    )
                    generated_ids.append(art.run_id)

        # Verify artifacts directory count
        art_files = list((Path(temp_dir) / "artifacts").glob("*.json"))
        trace_files = list((Path(temp_dir) / "routing_traces").glob("*.json"))

        assert len(art_files) == total_expected
        assert len(trace_files) == total_expected
        assert len(set(generated_ids)) == total_expected

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)
