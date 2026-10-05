import pytest
from src.uncertainty.audit import run_static_leakage_audit


def test_static_leakage_audit():
    audit_result = run_static_leakage_audit()
    assert audit_result["status"] == "PASS"
    assert len(audit_result["violations"]) == 0
    assert audit_result["files_checked_count"] > 0
