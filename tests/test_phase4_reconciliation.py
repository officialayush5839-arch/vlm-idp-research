"""
Unit Tests for Baseline Reconciliation.
Strictly verifies Sections 33, 34, and 75 of the Phase 4 specification.
"""

from src.benchmark.reconciliation import BaselineReconciler


def test_baseline_reconciliation_pass():
    historical = {
        "B0": {"F1": 1.00, "ANLS": 1.00},
        "B1": {"F1": 1.00, "ANLS": 1.00},
        "B2": {"F1": 1.00, "ANLS": 1.00},
        "B0-U": {"F1": 1.00, "ANLS": 1.00},
    }
    reconciler = BaselineReconciler(tolerance=0.05, historical_references=historical)
    s0_results = {
        "B0": {"F1": 1.00, "ANLS": 1.00},
        "B1": {"F1": 0.99, "ANLS": 0.98},
        "B2": {"F1": 1.00, "ANLS": 0.99},
        "B0-U": {"F1": 0.98, "ANLS": 0.97},
    }
    records = reconciler.reconcile(s0_results)
    assert len(records) == 8
    assert all(r.status == "PASS" for r in records)


def test_baseline_reconciliation_detects_mismatch():
    historical = {
        "B0": {"F1": 1.00, "ANLS": 1.00},
        "B1": {"F1": 1.00, "ANLS": 1.00},
        "B2": {"F1": 1.00, "ANLS": 1.00},
        "B0-U": {"F1": 1.00, "ANLS": 1.00},
    }
    reconciler = BaselineReconciler(tolerance=0.05, historical_references=historical)
    s0_results = {
        "B0": {"F1": 0.80, "ANLS": 0.80},  # Drastic mismatch > 0.05 tolerance
        "B1": {"F1": 1.00, "ANLS": 1.00},
        "B2": {"F1": 1.00, "ANLS": 1.00},
        "B0-U": {"F1": 1.00, "ANLS": 1.00},
    }
    records = reconciler.reconcile(s0_results)
    b0_records = [r for r in records if r.model == "B0"]
    assert any(r.status == "FAIL" for r in b0_records)
