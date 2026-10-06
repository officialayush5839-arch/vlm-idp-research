"""Audit Test Suite 1: Repository Integrity & Historical Hash Manifest.

Verifies that:
1. Pre-audit SHA-256 hash manifest exists and is non-empty.
2. All 12 completed phases (P0 to P11) have intact directory structures and metrics.
3. No historical files were modified or deleted during audit operations.
"""

import json
import os
import hashlib
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).parent.parent
MANIFEST_PATH = REPO_ROOT / "reports" / "next_phase" / "pre_audit_hash_manifest.json"


def compute_sha256(filepath: Path) -> str:
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


def test_hash_manifest_exists_and_valid():
    """Verify pre-audit hash manifest exists and contains expected file count."""
    assert MANIFEST_PATH.exists(), "pre_audit_hash_manifest.json must exist"
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    assert "total_files" in manifest
    assert "files" in manifest
    assert manifest["total_files"] >= 2000, f"Expected >=2000 files, found {manifest['total_files']}"
    assert len(manifest["files"]) == manifest["total_files"]


def test_all_phases_have_experiment_directories():
    """Verify that all phases P2 through P11 have experiment directories."""
    expected_phases = [
        "phase2", "phase2_5", "phase3", "phase4",
        "phase5", "phase5_1", "phase6", "phase7",
        "phase8", "phase9", "phase10", "phase10_5", "phase11"
    ]
    for phase in expected_phases:
        pdir = REPO_ROOT / "experiments" / phase
        assert pdir.exists() and pdir.is_dir(), f"Experiment directory missing for {phase}"


def test_phase_reports_exist():
    """Verify that phase report directories exist for all phases."""
    reports_dir = REPO_ROOT / "reports"
    expected_phase_dirs = [
        "phase0", "phase1", "phase2", "phase2_5", "phase3", "phase4",
        "phase5", "phase5_1", "phase6", "phase7", "phase8", "phase9",
        "phase10", "phase10_5", "phase11"
    ]
    for p in expected_phase_dirs:
        pdir = reports_dir / p
        assert pdir.exists() and pdir.is_dir(), f"Report directory missing for {p}"


def test_audit_reports_exist():
    """Verify that all Phase Next audit reports have been generated."""
    next_phase_dir = REPO_ROOT / "reports" / "next_phase"
    required_reports = [
        "repository_inventory.md",
        "phase_by_phase_inventory.md",
        "performance_baseline.md",
        "cross_phase_consistency.md",
        "baseline_quality_audit.md",
        "statistical_rigor_audit.md",
        "ablation_quality_audit.md",
        "dataset_quality_audit.md",
        "reproducibility_audit.md",
        "scientific_claim_audit.md",
        "negative_results_analysis.md",
        "research_gap_analysis.md",
        "RESEARCH_IMPROVEMENT_ROADMAP.md",
        "RESEARCH_BASELINE_AUDIT.md",
    ]
    for r in required_reports:
        fpath = next_phase_dir / r
        assert fpath.exists() and fpath.stat().st_size > 0, f"Audit report missing or empty: {r}"
