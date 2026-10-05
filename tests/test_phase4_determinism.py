"""
Unit Tests for Phase 4 Benchmark Determinism and Repeatability.
Strictly verifies Sections 58, 60, and 76 of the Phase 4 specification.
"""

from PIL import Image
from src.benchmark.evaluator import BenchmarkEvaluator
from src.benchmark.model_runner import ModelRunner
from src.benchmark.schema import BenchmarkSample


def test_model_and_evaluation_determinism():
    runner = ModelRunner()
    evaluator = BenchmarkEvaluator()

    img = Image.new("RGB", (300, 300), color=(250, 250, 250))
    sample = BenchmarkSample(
        sample_id="det_01",
        document_id="doc_det",
        dataset="DocVQA",
        split="test",
        page_idx=0,
        total_pages=1,
        image=img,
        task_type="vqa",
        question="What is the invoice total?",
        ground_truth_answers=["$1,000.00"],
        source_sha256="det_hash",
    )

    models = ["B0", "B1", "B2", "B0-U"]
    for m in models:
        res1 = runner.run_model(m, sample, run_id="run_det_1", seed=42)
        res2 = runner.run_model(m, sample, run_id="run_det_2", seed=42)

        assert res1.answer == res2.answer
        assert res1.status == res2.status
        assert res1.prompt_hash == res2.prompt_hash

        ev1 = evaluator.evaluate(sample, res1)
        ev2 = evaluator.evaluate(sample, res2)

        assert ev1.exact_match == ev2.exact_match
        assert ev1.token_f1 == ev2.token_f1
        assert ev1.anls == ev2.anls
