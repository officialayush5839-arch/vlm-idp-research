"""Run Artifact Serialization and Experiment Logging for Phase 2 Baselines."""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from src.baselines.base import BaselineResult


def save_run_artifact(
    result: BaselineResult,
    output_dir: str = "experiments/phase2/artifacts"
) -> Path:
    """Save a single inference execution record to disk as a JSON artifact."""
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    filename = f"{result.run_id}_{result.baseline}_{result.document_id}_{result.question_id}.json"
    target_file = out_path / filename

    with open(target_file, "w", encoding="utf-8") as f:
        json.dump(result.model_dump(), f, indent=2)

    return target_file


def save_experiment_summary(
    results: List[BaselineResult],
    experiment_id: str,
    output_dir: str = "experiments/phase2"
) -> Path:
    """Aggregate a batch of run artifacts into a structured experiment summary report."""
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    summary_file = out_path / f"{experiment_id}_summary.json"
    data = {
        "experiment_id": experiment_id,
        "total_samples": len(results),
        "successful_runs": sum(1 for r in results if r.status == "SUCCESS"),
        "failed_runs": sum(1 for r in results if r.status == "FAILED"),
        "results": [r.model_dump() for r in results]
    }

    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    return summary_file
