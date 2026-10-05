"""
Zero-Leakage AST Audit Test for Phase 7 Evidence Grounding Subsystem.
Verifies that runtime modules under src/evidence/ do not access
oracle ground-truth attributes or test-set labels.
"""

from src.evidence.audit import audit_zero_leakage


def test_phase7_zero_leakage_ast_audit():
    audit_res = audit_zero_leakage("src/evidence")
    assert audit_res["zero_leakage_verified"] is True, (
        f"AST Leakage detected: {audit_res['violations']}"
    )
    assert audit_res["violation_count"] == 0
    assert len(audit_res["files_checked"]) >= 10
