"""
Tests for Phase 5.1 Trace Identity Uniqueness (Audit Defect P1-01).
Verifies that run_id includes degradation family, severity, and seed,
guaranteeing complete trace cardinality without filesystem overwrites.
"""

import pytest
from src.routing.schema import RoutingPolicyType
from src.benchmark.schema import BenchmarkSample, DegradationCondition
from src.routing.pipeline import AdaptiveRoutingPipeline
from PIL import Image


def test_phase5_1_run_id_distinct_across_conditions():
    """Verify that distinct degradation conditions produce unique run_ids."""
    sample = BenchmarkSample(
        sample_id="doc_001_sroie",
        document_id="doc_001",
        dataset="sroie",
        split="test",
        page_idx=0,
        question="What is the total amount?",
        answers=["15.00"],
        source_sha256="dummy_hash_001",
    )

    conditions = [
        DegradationCondition(family="gaussian_blur", severity=s, parameter_name="sigma", parameter_value=float(s), seed=42)
        for s in range(5)
    ] + [
        DegradationCondition(family="gaussian_noise", severity=s, parameter_name="var", parameter_value=float(s), seed=42)
        for s in range(1, 5)
    ]

    pipeline = AdaptiveRoutingPipeline.create_default(phase="phase5_1")
    dummy_img = Image.new("RGB", (100, 100), color=(255, 255, 255))

    run_ids = set()
    for cond in conditions:
        art = pipeline.process_sample(
            sample=sample,
            degraded_image=dummy_img,
            policy=RoutingPolicyType.R1_FIXED_BEST,
            condition=cond,
            save_artifact=False,
        )
        assert art.run_id not in run_ids, f"Duplicate run_id encountered: {art.run_id}"
        run_ids.add(art.run_id)
        assert f"_{cond.family}_sev{cond.severity}_s{cond.seed}" in art.run_id
        assert art.degradation_family == cond.family
        assert art.severity == cond.severity

    assert len(run_ids) == len(conditions)


def test_phase5_1_run_id_format_specification():
    """Verify run_id matches the exact required regex pattern."""
    import re
    sample = BenchmarkSample(
        sample_id="sample_42",
        document_id="doc_99",
        dataset="docvqa",
        split="test",
        page_idx=0,
        question="Invoice date?",
        answers=["2026-01-01"],
        source_sha256="dummy_hash_042",
    )
    cond = DegradationCondition(family="motion_blur", severity=3, parameter_name="angle", parameter_value=45, seed=123)
    pipeline = AdaptiveRoutingPipeline.create_default(phase="phase5_1")
    dummy_img = Image.new("RGB", (64, 64), color=(200, 200, 200))

    art = pipeline.process_sample(
        sample=sample,
        degraded_image=dummy_img,
        policy=RoutingPolicyType.R2_RULE_BASED,
        condition=cond,
        save_artifact=False,
    )

    expected_pattern = r"^run_P5_1_docvqa_R2_RULE_BASED_sample_42_motion_blur_sev3_s123$"
    assert re.match(expected_pattern, art.run_id) is not None
