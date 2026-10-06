"""src/safety_recovery/provenance.py
Cryptographic provenance and trace identity management for Phase 11.
"""

import hashlib
import json
from typing import Dict, Any


class Phase11ProvenanceTracker:
    """Generates unique trace IDs and computes cryptographic fingerprints."""

    @staticmethod
    def generate_trace_id(
        dataset: str,
        baseline: str,
        document_id: str,
        query_id: str,
        domain: str,
        seed: int,
    ) -> str:
        """Format: run_P11_{dataset}_{baseline}_{doc}_{query}_{domain}_s{seed}"""
        return (
            f"run_P11_{dataset.lower()}_{baseline.lower().replace('.', '_').replace('-', '_')}_"
            f"{document_id}_{query_id}_{domain.lower()}_s{seed}"
        )

    @staticmethod
    def compute_sha256(data: Dict[str, Any]) -> str:
        """Computes deterministic SHA-256 for a trace dict."""
        serialized = json.dumps(data, sort_keys=True)
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()
