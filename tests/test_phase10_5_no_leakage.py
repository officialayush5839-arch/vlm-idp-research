"""tests/test_phase10_5_no_leakage.py
Zero-leakage static AST and runtime leakage test suite for src/recovery/.
"""

from src.recovery.audit import ZeroLeakageAuditor


def test_zero_leakage_ast_audit():
    violations = ZeroLeakageAuditor.audit_directory("src/recovery")
    assert violations == [], f"Zero-leakage violations detected in src/recovery: {violations}"
