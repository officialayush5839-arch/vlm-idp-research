"""Tests for Phase 9 zero-leakage AST static audit."""

from pathlib import Path
import pytest
from src.reliability.audit import ZeroLeakageAuditor

SRC_RELIABILITY_DIR = Path(__file__).resolve().parent.parent / "src" / "reliability"


def test_zero_leakage_audit_clean():
    violations = ZeroLeakageAuditor.audit_reliability_package(SRC_RELIABILITY_DIR)
    assert len(violations) == 0, f"Zero leakage audit found forbidden symbol violations: {violations}"
