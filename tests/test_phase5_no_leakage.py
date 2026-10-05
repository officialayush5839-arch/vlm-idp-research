"""
Tests for Phase 5 Zero-Leakage Verification and Decision Tracing.
Verifies static AST audit against ground-truth/label leakage into routing decisions.
"""

from pathlib import Path
import pytest
from src.routing.schema import RoutingDecision, RoutingPolicyType
from src.routing.decision_trace import RoutingDecisionTracer
from src.routing.audit import ZeroLeakageRouterAuditor


def test_decision_tracer_serialization(tmp_path):
    tracer = RoutingDecisionTracer(trace_dir=str(tmp_path))
    decision = RoutingDecision(
        run_id="run_trace_01",
        document_id="doc_trace_01",
        page_id="doc_trace_01_p0",
        dataset="DocVQA",
        partition="test",
        routing_policy=RoutingPolicyType.R2_RULE_BASED,
        selected_model="B2",
        routing_confidence=0.90,
        decision_reason="Severe skew detected",
        candidate_models=["B0", "B1", "B2", "B0-U"],
    )
    trace = tracer.record_trace(decision)
    assert trace.selected_model == "B2"

    saved_path = tracer.save_trace(trace)
    assert Path(saved_path).exists()


def test_zero_leakage_audit_clean_routing_codebase():
    auditor = ZeroLeakageRouterAuditor()
    routing_src_dir = str(Path(__file__).parents[1] / "src" / "routing")
    audit_report = auditor.audit_directory(routing_src_dir)

    assert audit_report["status"] == "PASS"
    assert len(audit_report["violations"]) == 0


def test_zero_leakage_audit_detects_forbidden_identifiers(tmp_path):
    auditor = ZeroLeakageRouterAuditor()
    leaky_file = tmp_path / "leaky_code.py"
    leaky_file.write_text(
        "def leaky_route(features, ground_truth_answers):\n"
        "    if 'total' in ground_truth_answers:\n"
        "        return 'B0'\n"
        "    return 'B2'\n",
        encoding="utf-8"
    )

    audit_report = auditor.audit_file(str(leaky_file))
    assert audit_report["status"] == "FAIL"
    assert any("ground_truth_answers" in v for v in audit_report["violations"])
