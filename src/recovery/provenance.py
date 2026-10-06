"""src/recovery/provenance.py
Cryptographic provenance tracking and trace identity management for Phase 10.5.
"""

import hashlib
import json
from typing import Dict, Any, Optional


class RecoveryProvenanceTracker:
    """Manages Phase 10.5 trace identity and prevents collision."""

    @staticmethod
    def generate_trace_id(
        dataset: str,
        domain: str,
        baseline: str,
        document_id: str,
        query_id: str,
        strategy: str,
        condition: str,
        seed: int,
    ) -> str:
        """Format: run_P10_5_{dataset}_{domain}_{baseline}_{doc}_{query}_{strategy}_{condition}_s{seed}"""
        return (
            f"run_P10_5_{dataset.lower()}_{domain.lower()}_{baseline.lower().replace('.', '_').replace('-', '_')}_"
            f"{document_id}_{query_id}_{strategy.lower()}_{condition.lower()}_s{seed}"
        )

    @staticmethod
    def compute_sha256(data: Dict[str, Any]) -> str:
        """Computes deterministic SHA-256 for a trace dict."""
        serialized = json.dumps(data, sort_keys=True)
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()
