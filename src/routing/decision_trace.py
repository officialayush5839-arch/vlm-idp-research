"""
Decision Trace Logger for Phase 5 Adaptive Routing.
Produces immutable, auditable traces of every routing decision.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional
import uuid

from src.routing.schema import RoutingDecision, RoutingTrace


class RoutingDecisionTracer:
    """
    Logs and serializes individual routing decision traces for provenance and analysis.
    """

    def __init__(self, trace_dir: Optional[str] = None):
        if trace_dir is None:
            trace_dir = str(Path(__file__).parents[2] / "experiments" / "phase5" / "routing_traces")
        self.trace_dir = Path(trace_dir)
        self.trace_dir.mkdir(parents=True, exist_ok=True)

    def record_trace(self, decision: RoutingDecision) -> RoutingTrace:
        """
        Creates an immutable RoutingTrace object from a RoutingDecision.
        """
        trace_id = f"trace_{uuid.uuid4().hex[:12]}"
        return RoutingTrace(
            trace_id=trace_id,
            run_id=decision.run_id,
            document_id=decision.document_id,
            candidate_models=decision.candidate_models,
            selected_model=decision.selected_model,
            decision_reason=decision.decision_reason,
            policy_version=decision.router_version,
            router_confidence=decision.routing_confidence,
            fallback_triggered=decision.fallback_triggered,
            timestamp_utc=decision.timestamp_utc,
        )

    def save_trace(self, trace: RoutingTrace) -> str:
        """
        Serializes trace to JSON disk artifact. Returns absolute file path.
        """
        out_path = self.trace_dir / f"{trace.run_id}_trace.json"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(trace.model_dump_json(indent=2))
        return str(out_path)
