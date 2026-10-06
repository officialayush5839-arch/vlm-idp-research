"""Tests for Phase 12 Zero Information Leakage."""

import pytest
from src.phase12.audit import run_static_ast_leakage_audit, run_runtime_adversarial_audit


def test_static_ast_leakage():
    findings = run_static_ast_leakage_audit()
    assert len(findings) == 0, f"Static leakage findings: {findings}"


def test_runtime_adversarial_leakage():
    findings = run_runtime_adversarial_audit()
    assert len(findings) == 0, f"Runtime leakage findings: {findings}"
