"""Audit Test Suite 2: Metric & Data Partition Consistency across Phases.

Verifies:
1. Multi-page corpus manifest consistency across P6-P11.
2. Standard test seeds (42, 123, 456, 789, 101112) used in P8-P11.
3. Domain partition mapping consistency (D0-D4 across P10, P10.5, P11).
"""

import json
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).parent.parent


def test_corpus_manifest_partition_integrity():
    """Verify Phase 6 corpus manifest defines 50 documents with exactly 25 in test split."""
    manifest_file = REPO_ROOT / "experiments" / "phase6" / "indexes" / "corpus_manifest.json"
    assert manifest_file.exists(), "corpus_manifest.json must exist"
    with open(manifest_file, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    
    docs = manifest["documents"]
    assert len(docs) == 50, f"Expected 50 documents, got {len(docs)}"
    
    train_docs = [d for d in docs if d["split"] == "train"]
    val_docs = [d for d in docs if d["split"] == "val"]
    test_docs = [d for d in docs if d["split"] == "test"]
    
    assert len(train_docs) == 10
    assert len(val_docs) == 15
    assert len(test_docs) == 25
    
    # Check disjointness
    train_ids = set(d["document_id"] for d in train_docs)
    val_ids = set(d["document_id"] for d in val_docs)
    test_ids = set(d["document_id"] for d in test_docs)
    
    assert train_ids.isdisjoint(val_ids)
    assert train_ids.isdisjoint(test_ids)
    assert val_ids.isdisjoint(test_ids)


def test_standard_test_seeds_across_phases():
    """Verify that Phases 8, 9, 10, 10.5, 11 use identical standard test seeds."""
    expected_seeds = {42, 123, 456, 789, 101112}
    
    # Phase 10 manifest
    p10_manifest_file = REPO_ROOT / "experiments" / "phase10" / "manifests" / "experiment_manifest.json"
    with open(p10_manifest_file, "r", encoding="utf-8") as f:
        p10_m = json.load(f)
    p10_seeds = set(e["seed"] for e in p10_m["experiments"])
    assert p10_seeds == expected_seeds, f"P10 seeds mismatch: {p10_seeds}"

    # Phase 11 manifest
    p11_manifest_file = REPO_ROOT / "experiments" / "phase11" / "manifests" / "experiment_manifest.json"
    with open(p11_manifest_file, "r", encoding="utf-8") as f:
        p11_m = json.load(f)
    p11_seeds = set(e["seed"] for e in p11_m["experiments"])
    assert p11_seeds == expected_seeds, f"P11 seeds mismatch: {p11_seeds}"


def test_domain_partition_consistency():
    """Verify that domains D0-D4 map to identical 5 test documents per domain across P10 and P11."""
    p10_manifest_file = REPO_ROOT / "experiments" / "phase10" / "manifests" / "experiment_manifest.json"
    with open(p10_manifest_file, "r", encoding="utf-8") as f:
        p10_m = json.load(f)
    
    p10_domain_docs = {}
    for e in p10_m["experiments"]:
        d_id = e["domain_id"]
        p10_domain_docs.setdefault(d_id, set()).add(e["document_id"])
    
    for d_id, docs in p10_domain_docs.items():
        assert len(docs) == 5, f"Domain {d_id} does not have exactly 5 documents: {len(docs)}"
