"""
Phase 4 Controlled Degradation Benchmark Orchestrator Pipeline.
Coordinates degradation generation, independent quality capture, baseline execution,
task evaluation, and artifact persistence.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional
import yaml
from PIL import Image

from src.benchmark.aggregator import BenchmarkAggregator
from src.benchmark.degradation_runner import DegradationRunner
from src.benchmark.evaluator import BenchmarkEvaluator
from src.benchmark.manifest import ManifestManager, compute_sha256
from src.benchmark.model_runner import ModelRunner
from src.benchmark.quality_capture import QualityCaptureHook
from src.benchmark.reconciliation import BaselineReconciler
from src.benchmark.schema import (
    BenchmarkRunArtifact,
    BenchmarkSample,
    DegradationCondition,
    ReconciliationRecord,
)


class BenchmarkPipeline:
    """End-to-end benchmark execution and evaluation orchestrator."""

    def __init__(
        self,
        matrix_config_path: str = "configs/phase4/experiment_matrix.yaml",
        benchmark_config_path: str = "configs/phase4/benchmark_config.yaml",
        execution_config_path: str = "configs/phase4/execution_config.yaml",
    ):
        with open(matrix_config_path, "r", encoding="utf-8") as f:
            self.matrix_cfg = yaml.safe_load(f)
        with open(benchmark_config_path, "r", encoding="utf-8") as f:
            self.benchmark_cfg = yaml.safe_load(f)
        with open(execution_config_path, "r", encoding="utf-8") as f:
            self.execution_cfg = yaml.safe_load(f)

        self.manifest_manager = ManifestManager(
            raw_dir=self.benchmark_cfg["paths"]["raw_data_dir"],
            manifest_dir=self.benchmark_cfg["paths"]["manifest_dir"],
            splits_dir=self.benchmark_cfg["paths"]["splits_dir"],
        )
        self.degradation_runner = DegradationRunner(
            cache_dir=self.benchmark_cfg["paths"]["degraded_data_dir"]
        )
        self.quality_hook = QualityCaptureHook()
        self.model_runner = ModelRunner(self.execution_cfg.get("baselines"))
        self.evaluator = BenchmarkEvaluator()
        self.reconciler = BaselineReconciler()

        self.artifacts_dir = Path(self.benchmark_cfg["paths"]["artifacts_dir"])
        self.summaries_dir = Path(self.benchmark_cfg["paths"]["summaries_dir"])
        self.index_file = Path(self.benchmark_cfg["paths"]["index_file"])

        self.artifacts_dir.mkdir(parents=True, exist_ok=True)
        self.summaries_dir.mkdir(parents=True, exist_ok=True)
        self.index_file.parent.mkdir(parents=True, exist_ok=True)

    def run_reconciliation(
        self, clean_samples: List[BenchmarkSample]
    ) -> List[ReconciliationRecord]:
        """
        Executes clean baseline reconciliation (S0) across B0, B1, B2, B0-U.
        """
        s0_results: Dict[str, Dict[str, float]] = {}

        models = ["B0", "B1", "B2", "B0-U"]
        for m in models:
            successes = 0
            f1s: List[float] = []
            anlss: List[float] = []
            for sample in clean_samples:
                res = self.model_runner.run_model(m, sample, run_id=f"reconcile_{m}", seed=42)
                if res.status == "SUCCESS":
                    successes += 1
                metrics = self.evaluator.evaluate(sample, res)
                f1s.append(metrics.token_f1)
                anlss.append(metrics.anls)

            n_samples = max(1, len(clean_samples))
            s0_results[m] = {
                "success_rate": float(successes / n_samples),
                "F1": float(sum(f1s) / n_samples),
                "ANLS": float(sum(anlss) / n_samples),
            }

        records = self.reconciler.reconcile(s0_results)
        self.reconciler.generate_markdown_report(
            records, Path(self.benchmark_cfg["paths"]["reports_dir"]) / "baseline_reconciliation.md"
        )
        return records

    def run_benchmark(
        self,
        clean_samples: Optional[List[BenchmarkSample]] = None,
        seeds: Optional[List[int]] = None,
        max_samples_per_dataset: Optional[int] = None,
        resume: bool = True,
    ) -> Tuple[List[BenchmarkRunArtifact], Dict[str, Any]]:
        """
        Runs the full controlled degradation benchmark matrix.
        """
        if clean_samples is None:
            clean_samples = self.manifest_manager.generate_standard_evaluation_corpus()

        if max_samples_per_dataset is not None:
            clean_samples = clean_samples[:max_samples_per_dataset]

        active_seeds = seeds or self.matrix_cfg.get("seeds", [42])
        models = [m["id"] for m in self.matrix_cfg.get("models", [])]
        families = self.matrix_cfg.get("degradation_families", [])

        artifacts: List[BenchmarkRunArtifact] = []
        index_entries: List[Dict[str, Any]] = []

        total_conditions = (
            len(clean_samples) * len(models) * len(families) * 5 * len(active_seeds)
        )
        print(f"Starting Phase 4 Controlled Benchmark ({total_conditions} conditions)...")

        # First, ensure clean baseline reconciliation passes
        reconciliation_records = self.run_reconciliation(clean_samples)
        reconcile_pass = all(r.status == "PASS" for r in reconciliation_records)
        if not reconcile_pass:
            raise RuntimeError("Baseline reconciliation failed! S0 clean measurements deviate from Phase 2/2.5 reference.")

        for clean_sample in clean_samples:
            for seed in active_seeds:
                for fam_info in families:
                    fam_id = fam_info["id"]
                    param_name = fam_info["parameter_name"]
                    param_values = fam_info["parameter_values"]

                    for severity in range(5):
                        param_val = param_values[severity]
                        condition = DegradationCondition(
                            family=fam_id,
                            severity=severity,
                            parameter_name=param_name,
                            parameter_value=param_val,
                            seed=seed,
                        )

                        # Generate degraded sample
                        deg_sample, derived_sha = self.degradation_runner.generate_degraded_sample(
                            clean_sample, condition
                        )

                        # Observational quality capture (Phase 3 independent measurement)
                        quality_vector = self.quality_hook.capture(
                            deg_sample.image,
                            doc_id=deg_sample.document_id,
                            page_idx=deg_sample.page_idx,
                        )

                        for model_id in models:
                            exp_id = (
                                f"E4-{deg_sample.dataset}-{model_id}-{fam_id.upper()}"
                                f"-S{severity}-SEED{seed}"
                            )
                            artifact_file = self.artifacts_dir / f"run_{exp_id}_{clean_sample.sample_id}.json"

                            if resume and artifact_file.exists():
                                try:
                                    with open(artifact_file, "r", encoding="utf-8") as f:
                                        art = BenchmarkRunArtifact.model_validate_json(f.read())
                                        artifacts.append(art)
                                        index_entries.append({
                                            "experiment_id": exp_id,
                                            "dataset": art.dataset,
                                            "sample_id": art.sample_id,
                                            "model": art.model,
                                            "degradation": art.degradation_family,
                                            "severity": art.severity,
                                            "seed": art.seed,
                                            "status": art.status,
                                            "artifact_path": str(artifact_file),
                                        })
                                        continue
                                except Exception:
                                    pass  # Corrupt artifact, re-run

                            # Execute model
                            exec_result = self.model_runner.run_model(
                                model_id, deg_sample, run_id=exp_id, seed=seed
                            )

                            # Evaluate task metrics
                            metrics_result = self.evaluator.evaluate(deg_sample, exec_result)

                            artifact = BenchmarkRunArtifact(
                                experiment_id=exp_id,
                                benchmark_version=self.benchmark_cfg.get("benchmark_version", "1.0.0"),
                                dataset=deg_sample.dataset,
                                sample_id=deg_sample.sample_id,
                                document_id=deg_sample.document_id,
                                page_idx=deg_sample.page_idx,
                                split=deg_sample.split,
                                model=model_id,
                                degradation_family=fam_id,
                                severity=severity,
                                seed=seed,
                                input={
                                    "source_sha256": clean_sample.source_sha256,
                                    "derived_sha256": derived_sha,
                                },
                                degradation_params={
                                    "family": fam_id,
                                    "severity": severity,
                                    "parameter_name": param_name,
                                    "parameter_value": param_val,
                                },
                                model_metadata={
                                    "model_name": exec_result.model_name,
                                    "revision": exec_result.revision_sha,
                                    "prompt_version": exec_result.prompt_version,
                                    "prompt_hash": exec_result.prompt_hash,
                                    "device": exec_result.device,
                                },
                                prediction=exec_result.answer,
                                ground_truth=deg_sample.ground_truth_answers,
                                metrics={
                                    "exact_match": metrics_result.exact_match,
                                    "token_f1": metrics_result.token_f1,
                                    "anls": metrics_result.anls,
                                    "cer": metrics_result.cer,
                                    "wer": metrics_result.wer,
                                    "grounding_iou": metrics_result.grounding_iou,
                                    "primary_metric": metrics_result.primary_metric_name,
                                    "primary_value": metrics_result.primary_metric_value,
                                },
                                quality_assessment=quality_vector,
                                runtime={
                                    "latency_ms": exec_result.latency_ms,
                                    "device": exec_result.device,
                                },
                                status=exec_result.status,
                                error_type=exec_result.error_type,
                                error_message=exec_result.error_message,
                            )

                            with open(artifact_file, "w", encoding="utf-8") as f:
                                f.write(artifact.model_dump_json(indent=2))

                            artifacts.append(artifact)
                            index_entries.append({
                                "experiment_id": exp_id,
                                "dataset": artifact.dataset,
                                "sample_id": artifact.sample_id,
                                "model": artifact.model,
                                "degradation": artifact.degradation_family,
                                "severity": artifact.severity,
                                "seed": artifact.seed,
                                "status": artifact.status,
                                "artifact_path": str(artifact_file),
                            })

        # Save index.json
        with open(self.index_file, "w", encoding="utf-8") as f:
            json.dump({"total_runs": len(index_entries), "index": index_entries}, f, indent=2)

        # Tabulate summary using aggregator
        aggregator = BenchmarkAggregator(artifacts)
        table_a = aggregator.compute_table_a_clean_baseline()
        table_b = aggregator.compute_table_b_robustness_grid()
        table_c = aggregator.compute_table_c_relative_degradation(table_b)
        table_d = aggregator.compute_table_d_quality_performance_relationship()
        table_e = aggregator.compute_table_e_statistical_comparison()

        summary_data = {
            "benchmark_id": self.benchmark_cfg.get("benchmark_id", "E4-CONTROLLED-DEGRADATION"),
            "total_artifacts": len(artifacts),
            "reconciliation": [r.model_dump() for r in reconciliation_records],
            "table_a_clean": table_a,
            "table_b_robustness": table_b,
            "table_c_relative_degradation": table_c,
            "table_d_quality_correlation": table_d,
            "table_e_statistical_tests": table_e,
        }

        summary_file = self.summaries_dir / "E4_BENCHMARK_summary.json"
        with open(summary_file, "w", encoding="utf-8") as f:
            json.dump(summary_data, f, indent=2)

        return artifacts, summary_data
