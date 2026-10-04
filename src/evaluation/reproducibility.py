"""
Reproducibility, environment capture, and dataset split validation utilities.
Enforces seed determinism and the mandatory Zero-Leakage Invariant.
"""

from __future__ import annotations

import hashlib
import json
import os
import platform
import random
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

import numpy as np


class SplitLeakageError(ValueError):
    """Raised when data leakage occurs across train/val/test partitions."""
    pass


def seed_everything(seed: int = 42) -> None:
    """
    Lock all pseudo-random number generators across Python, NumPy, and PyTorch.
    Ensures computational reproducibility across runs.
    """
    random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    np.random.seed(seed)

    try:
        import torch
        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed(seed)
            torch.cuda.manual_seed_all(seed)
            torch.backends.cudnn.deterministic = True
            torch.backends.cudnn.benchmark = False
    except ImportError:
        pass


def get_git_commit() -> str:
    """Retrieve the current Git commit hash or return 'UNKNOWN_COMMIT'."""
    try:
        commit = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            stderr=subprocess.DEVNULL,
            text=True
        ).strip()
        return commit
    except Exception:
        return "UNKNOWN_COMMIT"


def get_environment_info() -> Dict[str, Any]:
    """Capture full runtime, OS, hardware, and library environment metadata."""
    env_info: Dict[str, Any] = {
        "os": platform.platform(),
        "python_version": sys.version.split()[0],
        "platform_machine": platform.machine(),
        "git_commit": get_git_commit(),
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    }

    try:
        import torch
        env_info["torch_version"] = torch.__version__
        env_info["cuda_available"] = torch.cuda.is_available()
        env_info["cuda_runtime_version"] = torch.version.cuda
        if torch.cuda.is_available():
            env_info["gpu_name"] = torch.cuda.get_device_name(0)
            env_info["gpu_count"] = torch.cuda.device_count()
            env_info["gpu_vram_bytes"] = torch.cuda.get_device_properties(0).total_memory
        else:
            env_info["gpu_name"] = "None"
    except ImportError:
        env_info["torch_version"] = "NOT_INSTALLED"
        env_info["cuda_available"] = False

    return env_info


def create_run_id(prefix: str = "run", seed: Optional[int] = None) -> str:
    """Generate a unique run ID incorporating timestamp and seed."""
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    seed_str = f"_s{seed}" if seed is not None else ""
    return f"{prefix}_{ts}{seed_str}"


def write_run_manifest(
    run_id: str,
    output_dir: str | Path,
    config: Dict[str, Any],
    metrics: Dict[str, Any],
    seed: int = 42,
    status: str = "COMPLETED"
) -> Path:
    """
    Write an immutable JSON run record capturing complete experiment provenance.
    """
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest_file = out_dir / f"{run_id}_manifest.json"

    manifest_data = {
        "run_id": run_id,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "seed": seed,
        "status": status,
        "environment": get_environment_info(),
        "configuration": config,
        "metrics": metrics,
    }

    with open(manifest_file, "w", encoding="utf-8") as f:
        json.dump(manifest_data, f, indent=2)

    return manifest_file


def validate_dataset_splits(
    records: List[Dict[str, Any]],
    source_id_key: str = "source_document_id",
    source_hash_key: str = "source_hash",
    partition_key: str = "partition"
) -> Tuple[bool, Dict[str, Any]]:
    """
    Validate dataset records against the Zero-Leakage Invariant.
    
    Checks:
    1. Every record has a valid partition ('train', 'val', or 'test').
    2. Every record has a valid source identifier.
    3. No two records sharing the same source_document_id belong to different partitions.
    4. No two records sharing the same source_hash belong to different partitions.
    
    Raises:
        SplitLeakageError if leakage or invalid partition assignment is detected.
    """
    allowed_partitions = {"train", "val", "test"}
    doc_to_partition: Dict[str, str] = {}
    hash_to_partition: Dict[str, str] = {}
    partition_counts: Dict[str, int] = {p: 0 for p in allowed_partitions}

    for i, rec in enumerate(records):
        partition = rec.get(partition_key)
        if not partition or partition not in allowed_partitions:
            raise SplitLeakageError(
                f"Record #{i} has invalid partition: '{partition}'. Must be one of {allowed_partitions}."
            )

        source_id = rec.get(source_id_key)
        if not source_id:
            raise SplitLeakageError(f"Record #{i} is missing required source identity key '{source_id_key}'.")

        source_hash = rec.get(source_hash_key)
        if not source_hash:
            raise SplitLeakageError(f"Record #{i} is missing required source hash key '{source_hash_key}'.")

        # Test 1 & 2: Same source document cannot occur across different partitions
        if source_id in doc_to_partition:
            prev_partition = doc_to_partition[source_id]
            if prev_partition != partition:
                raise SplitLeakageError(
                    f"DATA LEAKAGE DETECTED! Source document '{source_id}' is assigned to both "
                    f"'{prev_partition}' and '{partition}' partitions."
                )
        else:
            doc_to_partition[source_id] = partition

        # Test 3: Identical source hashes cannot cross partitions
        if source_hash in hash_to_partition:
            prev_partition = hash_to_partition[source_hash]
            if prev_partition != partition:
                raise SplitLeakageError(
                    f"DATA LEAKAGE DETECTED! Source hash '{source_hash}' appears in both "
                    f"'{prev_partition}' and '{partition}' partitions."
                )
        else:
            hash_to_partition[source_hash] = partition

        partition_counts[partition] += 1

    summary = {
        "total_records": len(records),
        "unique_source_documents": len(doc_to_partition),
        "unique_source_hashes": len(hash_to_partition),
        "partition_counts": partition_counts,
        "status": "VALID_ZERO_LEAKAGE"
    }

    return True, summary
