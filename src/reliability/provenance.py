"""src/reliability/provenance.py
Trace ID generation and collision prevention for Phase 9 experiments.
Pattern: run_P9_{dataset}_{baseline}_{doc}_{query}_{condition}_s{seed}
"""

import hashlib
import json
from pathlib import Path
from typing import Dict, Any, Set


class ProvenanceTracker:
    """Manages unique trace IDs and experiment provenance."""

    def __init__(self, trace_dir: Optional[Path] = None):
        self.trace_dir = trace_dir or (
            Path(__file__).resolve().parent.parent.parent / "experiments" / "phase9" / "traces"
        )
        self.seen_trace_ids: Set[str] = set()

    @staticmethod
    def generate_trace_id(
        dataset: str,
        baseline: str,
        doc_id: str,
        query_id: str,
        condition: str,
        seed: int,
    ) -> str:
        # Standardized format
        clean_dataset = str(dataset).replace(" ", "_").lower()
        clean_baseline = str(baseline).replace("-", "_").upper()
        clean_doc = str(doc_id).replace(" ", "_")
        clean_query = str(query_id).replace(" ", "_")
        clean_cond = str(condition).replace(" ", "_").lower()
        return f"run_P9_{clean_dataset}_{clean_baseline}_{clean_doc}_{clean_query}_{clean_cond}_s{seed}"

    def register_trace(self, trace_id: str, trace_data: Dict[str, Any]) -> Path:
        if trace_id in self.seen_trace_ids:
            raise ValueError(f"Trace ID collision detected in-memory: {trace_id}")

        self.trace_dir.mkdir(parents=True, exist_ok=True)
        trace_path = self.trace_dir / f"{trace_id}.json"

        if trace_path.exists():
            raise FileExistsError(f"Trace file already exists on disk: {trace_path}")

        # Compute deterministic checksum of trace content
        trace_copy = dict(trace_data)
        trace_copy["trace_id"] = trace_id
        content_bytes = json.dumps(trace_copy, sort_keys=True, indent=2).encode("utf-8")
        sha256 = hashlib.sha256(content_bytes).hexdigest()
        trace_copy["sha256"] = sha256

        with open(trace_path, "w", encoding="utf-8") as f:
            json.dump(trace_copy, f, indent=2)

        self.seen_trace_ids.add(trace_id)
        return trace_path
