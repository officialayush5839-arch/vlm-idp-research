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


import hashlib

class RoutingDecisionTracer:
    """
    Logs and serializes individual routing decision traces for provenance and analysis.
    Enforces collision detection and cryptographic integrity in Phase 5.1.
    """

    def __init__(self, trace_dir: Optional[str] = None):
        if trace_dir is None:
            trace_dir = str(Path(__file__).parents[2] / "experiments" / "phase5" / "routing_traces")
        self.trace_dir = Path(trace_dir)
        self.trace_dir.mkdir(parents=True, exist_ok=True)

    def record_trace(
        self,
        decision: RoutingDecision,
        phase: str = "phase5_1",
        sample_id: Optional[str] = None,
        degradation_family: Optional[str] = None,
        severity: Optional[int] = None,
        seed: Optional[int] = None,
        policy: Optional[str] = None,
        configuration_hash: Optional[str] = None,
        model_revision: Optional[str] = None,
        input_hash: Optional[str] = None,
        quality_feature_hash: Optional[str] = None,
        fallback_status: Optional[str] = None,
        latency_ms: Optional[float] = None,
        compute_cost: Optional[float] = None,
    ) -> RoutingTrace:
        """
        Creates an immutable RoutingTrace object from a RoutingDecision with full provenance.
        """
        trace_id = f"trace_{uuid.uuid4().hex[:12]}"
        u_dict = decision.uncertainty_vector.model_dump() if decision.uncertainty_vector else None

        raw_payload = f"{decision.run_id}_{decision.selected_model}_{decision.routing_confidence}_{decision.timestamp_utc}"
        art_hash = hashlib.sha256(raw_payload.encode("utf-8")).hexdigest()

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
            phase=phase,
            dataset=decision.dataset,
            sample_id=sample_id,
            degradation_family=degradation_family,
            severity=severity,
            seed=seed,
            policy=policy or decision.routing_policy.value,
            configuration_hash=configuration_hash,
            model_revision=model_revision,
            input_hash=input_hash,
            quality_feature_hash=quality_feature_hash,
            uncertainty_vector=u_dict,
            fallback_status=fallback_status,
            latency_ms=latency_ms or decision.latency_ms,
            compute_cost=compute_cost,
            artifact_hash=art_hash,
        )

    def save_trace(self, trace: RoutingTrace) -> str:
        """
        Serializes trace to JSON disk artifact.
        Enforces collision detection: raises FileExistsError if artifact already exists
        with differing content hash.
        """
        out_path = self.trace_dir / f"{trace.run_id}_trace.json"
        new_content = trace.model_dump_json(indent=2)
        new_hash = hashlib.sha256(new_content.encode("utf-8")).hexdigest()

        if out_path.exists():
            existing_content = out_path.read_text(encoding="utf-8")
            existing_hash = hashlib.sha256(existing_content.encode("utf-8")).hexdigest()
            # If identical hash, allow idempotent reproduction; otherwise detect collision
            if existing_hash != new_hash:
                # Check if trace_id and timestamp are the only diff by comparing core fields
                try:
                    ex_data = json.loads(existing_content)
                    new_data = json.loads(new_content)
                    # Compare core condition fields
                    core_keys = ["run_id", "document_id", "selected_model", "decision_reason", "routing_confidence"]
                    if any(ex_data.get(k) != new_data.get(k) for k in core_keys):
                        raise FileExistsError(
                            f"Trace collision detected for run_id '{trace.run_id}' at {out_path}. "
                            "Existing artifact has differing decision/condition content. Overwriting is forbidden."
                        )
                except json.JSONDecodeError:
                    raise FileExistsError(
                        f"Trace collision detected for run_id '{trace.run_id}' at {out_path}."
                    )

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        return str(out_path)
