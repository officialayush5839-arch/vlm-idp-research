"""
Tests for Phase 5.1 Static Zero-Leakage Code Audit (Audit Defect P1-02).
Runs AST static analyzer across all routing source files to certify zero leakage.
"""

from pathlib import Path
import tempfile
import shutil

from src.routing.audit import ZeroLeakageRouterAuditor


def test_zero_leakage_audit_phase5_1_clean():
    """Verify that all production files under src/routing pass the static zero-leakage audit."""
    auditor = ZeroLeakageRouterAuditor()
    routing_dir = str(Path(__file__).resolve().parents[1] / "src" / "routing")
    res = auditor.audit_directory(routing_dir)

    assert res["status"] == "PASS", f"Leakage violations detected in src/routing: {res['violations']}"
    assert len(res["violations"]) == 0
    assert res["files_scanned"] >= 8


def test_zero_leakage_audit_detects_attribute_leakage():
    """Verify that the auditor catches attribute leakage such as condition_severity or target_class."""
    temp_dir = tempfile.mkdtemp()
    try:
        bad_code = '''
def route_with_leakage(sample, condition):
    # Forbidden attribute access
    sev = condition_severity
    return "B2"
'''
        bad_file = Path(temp_dir) / "leaking_router.py"
        bad_file.write_text(bad_code, encoding="utf-8")

        auditor = ZeroLeakageRouterAuditor()
        res = auditor.audit_file(str(bad_file))
        assert res["status"] == "FAIL"
        assert any("condition_severity" in v for v in res["violations"])
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)
