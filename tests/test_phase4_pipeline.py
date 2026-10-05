"""
Integration Tests for Phase 4 Benchmark Pipeline.
Strictly verifies Section 79 of the Phase 4 specification.
"""

import tempfile
from pathlib import Path
from PIL import Image
import yaml

from src.benchmark.pipeline import BenchmarkPipeline
from src.benchmark.schema import BenchmarkSample


def test_pipeline_smoke_execution():
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)

        # Temporary configs
        matrix_cfg = {
            "models": [
                {"id": "B0", "name": "OCR-Only"},
                {"id": "B2", "name": "VLM-Only"},
            ],
            "degradation_families": [
                {
                    "id": "gaussian_blur",
                    "parameter_name": "sigma",
                    "parameter_values": [0.0, 1.0, 2.0, 4.0, 6.0],
                }
            ],
            "seeds": [42],
        }
        matrix_path = tmp_path / "matrix.yaml"
        with open(matrix_path, "w", encoding="utf-8") as f:
            yaml.dump(matrix_cfg, f)

        bench_cfg = {
            "benchmark_id": "TEST-SMOKE",
            "paths": {
                "raw_data_dir": str(tmp_path / "raw"),
                "degraded_data_dir": str(tmp_path / "degraded"),
                "manifest_dir": str(tmp_path / "manifests"),
                "splits_dir": str(tmp_path / "splits"),
                "artifacts_dir": str(tmp_path / "artifacts"),
                "summaries_dir": str(tmp_path / "summaries"),
                "reports_dir": str(tmp_path / "reports"),
                "index_file": str(tmp_path / "index.json"),
            },
        }
        bench_path = tmp_path / "bench.yaml"
        with open(bench_path, "w", encoding="utf-8") as f:
            yaml.dump(bench_cfg, f)

        exec_cfg = {
            "baselines": {
                "B0": {"mock_mode": True},
                "B2": {"mock_mode": True},
            }
        }
        exec_path = tmp_path / "exec.yaml"
        with open(exec_path, "w", encoding="utf-8") as f:
            yaml.dump(exec_cfg, f)

        pipeline = BenchmarkPipeline(
            matrix_config_path=str(matrix_path),
            benchmark_config_path=str(bench_path),
            execution_config_path=str(exec_path),
        )

        # Create one sample
        img = Image.new("RGB", (300, 200), color=(250, 250, 250))
        sample = BenchmarkSample(
            sample_id="test_p01",
            document_id="doc_pipe_01",
            dataset="DocVQA",
            split="test",
            page_idx=0,
            total_pages=1,
            image=img,
            task_type="vqa",
            question="What is the test question?",
            ground_truth_answers=["Answer"],
            source_sha256="test_sha",
        )

        artifacts, summary = pipeline.run_benchmark(
            clean_samples=[sample], seeds=[42], resume=False
        )

        assert len(artifacts) == 2 * 1 * 5  # 2 models * 1 family * 5 severities = 10 runs
        assert (tmp_path / "index.json").exists()
        assert len(summary["table_b_robustness"]) == 2  # 2 models
