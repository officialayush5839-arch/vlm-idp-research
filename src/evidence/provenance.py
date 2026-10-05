"""
Cryptographic Provenance and Trace Identification Module for Phase 7 Evidence Grounding.
Ensures zero-leakage, reproducible audit trails with unique run IDs, artifact hashing,
and deterministic evidence fingerprints.
"""

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from typing import Dict, Any, Optional, Tuple


def compute_sha256(content: str) -> str:
    """
    Compute hex SHA256 digest of input string.
    """
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def compute_evidence_unit_hash(
    document_id: str,
    page_id: int,
    region_id: str,
    bbox_1000: Tuple[int, int, int, int],
    text: str
) -> str:
    """
    Compute deterministic SHA-256 fingerprint for an atomic evidence unit.
    """
    norm_text = " ".join(text.strip().split())
    raw_payload = f"{document_id}|{page_id}|{region_id}|{bbox_1000}|{norm_text}"
    return compute_sha256(raw_payload)


_CACHED_GIT_COMMIT: Optional[str] = None


def get_git_commit(fallback: str = "afdd599") -> str:
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


def generate_phase7_run_id(
    dataset: str,
    baseline: str,
    document_id: str,
    query_id: str,
    condition: str,
    seed: int
) -> str:
    """
    Generate unique, deterministic trace run ID:
    run_P7_{dataset}_{baseline}_{doc}_{query}_{condition}_s{seed}
    """
    clean_ds = dataset.replace("-", "_").lower()
    clean_base = baseline.replace("-", "_").lower()
    clean_doc = document_id.replace("-", "_").lower()
    clean_q = query_id.replace("-", "_").lower()
    clean_cond = condition.replace("-", "_").lower()
    return f"run_P7_{clean_ds}_{clean_base}_{clean_doc}_{clean_q}_{clean_cond}_s{seed}"


def build_provenance_record(
    dataset: str,
    baseline: str,
    document_id: str,
    query_id: str,
    condition: str,
    seed: int,
    extra_metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Construct a complete provenance record for a Phase 7 run.
    """
    run_id = generate_phase7_run_id(dataset, baseline, document_id, query_id, condition, seed)
    rec: Dict[str, Any] = {
        "run_id": run_id,
        "phase": "PHASE_7",
        "dataset": dataset,
        "baseline": baseline,
        "document_id": document_id,
        "query_id": query_id,
        "condition": condition,
        "seed": seed,
        "git_commit": get_git_commit(),
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    }
    if extra_metadata:
        rec.update(extra_metadata)
    rec["record_hash"] = compute_sha256(json.dumps(rec, sort_keys=True))
    return rec
