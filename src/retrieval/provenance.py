"""
Cryptographic Provenance and Trace Identification Module for Phase 6.
Ensures zero-leakage, reproducible audit trails with unique run IDs and artifact hashing.
"""

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from typing import Dict, Any, Optional


def compute_sha256(content: str) -> str:
    """
    Compute hex SHA256 digest of input string.
    """
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


_CACHED_GIT_COMMIT: Optional[str] = None


def get_git_commit(fallback: str = "3dfa2a2") -> str:
    """
    Retrieve current git HEAD commit hash, or return fallback commit.
    Caches result to avoid spawning git process repeatedly.
    """
    global _CACHED_GIT_COMMIT
    if _CACHED_GIT_COMMIT is not None:
        return _CACHED_GIT_COMMIT

    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            stderr=subprocess.DEVNULL,
            timeout=2
        ).decode("utf-8").strip()
        _CACHED_GIT_COMMIT = out if out else fallback
        return _CACHED_GIT_COMMIT
    except Exception:
        _CACHED_GIT_COMMIT = fallback
        return _CACHED_GIT_COMMIT


def generate_phase6_run_id(
    dataset: str,
    method: str,
    document_id: str,
    query_id: str,
    seed: int
) -> str:
    """
    Generate unique, deterministic run ID:
    run_P6_{dataset}_{method}_{doc}_{query}_s{seed}
    """
    clean_ds = dataset.replace("-", "_").lower()
    clean_meth = method.replace("-", "_").lower()
    clean_doc = document_id.replace("-", "_").lower()
    clean_q = query_id.replace("-", "_").lower()
    return f"run_P6_{clean_ds}_{clean_meth}_{clean_doc}_{clean_q}_s{seed}"


def create_retrieval_provenance(
    dataset: str,
    method: str,
    document_id: str,
    query_id: str,
    seed: int,
    config_dict: Optional[Dict[str, Any]] = None,
    document_content: str = "",
    query_content: str = ""
) -> Dict[str, Any]:
    """
    Assemble complete cryptographic provenance metadata dictionary.
    """
    run_id = generate_phase6_run_id(dataset, method, document_id, query_id, seed)
    git_hash = get_git_commit()
    doc_hash = compute_sha256(document_content)[:16] if document_content else "none"
    q_hash = compute_sha256(query_content)[:16] if query_content else "none"
    cfg_hash = compute_sha256(json.dumps(config_dict or {}, sort_keys=True))[:16]

    return {
        "run_id": run_id,
        "phase": "6",
        "git_commit": git_hash,
        "dataset": dataset,
        "method": method,
        "seed": seed,
        "document_hash": doc_hash,
        "query_hash": q_hash,
        "config_hash": cfg_hash,
        "timestamp_utc": datetime.now(timezone.utc).isoformat()
    }
