"""
Execution Provenance Tracking and Collision Prevention for Phase 8.
Generates deterministic trace IDs, enforces idempotency, and halts on trace collision.
"""

import os
import json
import hashlib
from typing import Dict, Any, Tuple


class TraceCollisionError(RuntimeError):
    """Raised when an attempt is made to overwrite a trace with divergent execution content."""
    pass


def generate_trace_id(
    dataset: str,
    baseline: str,
    doc_id: str,
    query_id: str,
    condition: str,
    seed: int
) -> str:
    """
    Generate standard collision-free Phase 8 execution trace identifier.
    Format: run_P8_{dataset}_{baseline}_{doc_id}_{query_id}_{condition}_s{seed}
    """
    clean_dataset = str(dataset).replace(" ", "_").lower()
    clean_baseline = str(baseline).replace(" ", "_")
    clean_doc = str(doc_id).replace(" ", "_")
    clean_query = str(query_id).replace(" ", "_")
    clean_cond = str(condition).replace(" ", "_")

    return f"run_P8_{clean_dataset}_{clean_baseline}_{clean_doc}_{clean_query}_{clean_cond}_s{seed}"


def save_provenance_trace(
    payload: Dict[str, Any],
    output_dir: str
) -> Tuple[str, str]:
    """
    Save execution trace to disk with collision detection and SHA-256 fingerprinting.
    Returns (file_path, sha256_hash).
    """
    os.makedirs(output_dir, exist_ok=True)
    trace_id = payload.get("trace_id", "trace_unknown")
    filename = f"{trace_id}.json"
    filepath = os.path.join(output_dir, filename)

    content_str = json.dumps(payload, indent=2, sort_keys=True)
    content_sha = hashlib.sha256(content_str.encode("utf-8")).hexdigest()

    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            existing_data = json.load(f)
        existing_str = json.dumps(existing_data, indent=2, sort_keys=True)
        existing_sha = hashlib.sha256(existing_str.encode("utf-8")).hexdigest()

        if existing_sha != content_sha:
            raise TraceCollisionError(
                f"Provenance collision detected for trace {trace_id} at {filepath}! "
                f"Existing hash={existing_sha}, New hash={content_sha}"
            )
        return filepath, content_sha

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content_str)

    return filepath, content_sha
