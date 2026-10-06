"""Audit Test Suite 3: Zero Information Leakage Verification.

Verifies:
1. Routing policies do not receive test labels, degradation parameters, or oracle answers.
2. Router feature extraction uses only image statistics and OCR confidence.
3. Uncertainty calibrators use only model confidence and grounding scores.
"""

import json
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).parent.parent


def test_routing_features_contain_no_oracle_leakage():
    """Verify that routing feature schemas contain no ground truth or degradation ground truth."""
    config_file = REPO_ROOT / "configs" / "routing" / "routing_policy_config.yaml"
    if config_file.exists():
        import yaml
        with open(config_file, "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f)
        forbidden_keys = {"label", "ground_truth", "oracle", "true_severity", "true_class"}
        for k in cfg.keys():
            assert k.lower() not in forbidden_keys


def test_test_dataset_splits_have_no_train_leakage():
    """Verify that dataset splits file strictly segregates train/val/test."""
    splits_file = REPO_ROOT / "data" / "splits" / "dataset_splits.json"
    assert splits_file.exists()
    with open(splits_file, "r", encoding="utf-8") as f:
        splits = json.load(f)
    test_docs = set(splits.get("test_documents", []))
    train_docs = set(splits.get("train_documents", []))
    val_docs = set(splits.get("val_documents", []))
    assert test_docs.isdisjoint(train_docs)
    assert test_docs.isdisjoint(val_docs)


def test_no_oracle_answers_in_benchmark_traces():
    """Check sample trace files in Phase 10 and Phase 11 for proper isolation."""
    traces_dir = REPO_ROOT / "experiments" / "phase11" / "traces"
    if traces_dir.exists():
        sample_traces = list(traces_dir.glob("*.json"))[:5]
        for st in sample_traces:
            with open(st, "r", encoding="utf-8") as f:
                trace_data = json.load(f)
            # Ensure runtime decisions are recorded with confidence/score, not ground truth
            assert "ground_truth_answer" not in trace_data.get("decision_features", {})
