"""
Unit Tests for No Data Leakage and Phase Boundary Compliance.
Strictly verifies Sections 3, 7, 14, 68, and 78 of the Phase 4 specification.
"""

import ast
from pathlib import Path


def test_no_adaptive_routing_in_phase4_source():
    """Static analysis to guarantee zero adaptive routing or model escalation logic in src/benchmark/."""
    benchmark_dir = Path("src/benchmark")
    forbidden_terms = [
        "adaptive_routing",
        "route_model",
        "switch_model",
        "uncertainty_routing",
        "review_required",
        "escalate",
        "proposed_architecture",
        "fallback_router",
    ]

    for py_file in benchmark_dir.glob("*.py"):
        with open(py_file, "r", encoding="utf-8") as f:
            code = f.read().lower()
            for term in forbidden_terms:
                assert term not in code, f"Forbidden Phase 5+ concept '{term}' found in {py_file}"


def test_no_ground_truth_passed_to_model_inference():
    """Verify that ModelRunner does not pass ground truth answers to baseline inference."""
    from src.benchmark.model_runner import ModelRunner
    from src.benchmark.schema import BenchmarkSample
    from PIL import Image

    runner = ModelRunner()
    img = Image.new("RGB", (200, 200), color=(255, 255, 255))
    sample = BenchmarkSample(
        sample_id="blind_test",
        document_id="doc_blind",
        dataset="DocVQA",
        split="test",
        page_idx=0,
        total_pages=1,
        image=img,
        task_type="vqa",
        question="What is the total?",
        ground_truth_answers=["SECRET_GT_ANSWER_XYZ"],
        source_sha256="hash123",
    )

    # In mock mode or real mode, prompt or execution must never leak the secret GT answer
    res_b1 = runner.run_model("B1", sample, run_id="b1_blind", seed=42)
    res_b2 = runner.run_model("B2", sample, run_id="b2_blind", seed=42)

    # The prompt should only contain question and document content, not ground_truth_answers
    assert "SECRET_GT_ANSWER_XYZ" not in (res_b1.prompt_version or "")
    assert "SECRET_GT_ANSWER_XYZ" not in (res_b2.prompt_version or "")
