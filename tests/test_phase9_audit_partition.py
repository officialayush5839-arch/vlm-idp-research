"""Audit test suite for Phase 9 partition integrity and leak prevention."""

from pathlib import Path
import json
import pytest

MANIFEST_PATH = Path("experiments/phase6/indexes/corpus_manifest.json")
CALIBRATION_CFG = Path("configs/phase9/calibration_config.yaml")
EVALUATION_CFG = Path("configs/phase9/evaluation_config.yaml")


def test_partition_split_manifest():
    assert MANIFEST_PATH.exists()
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    docs = manifest.get("documents", [])
    val_docs = [d for d in docs if d.get("split") == "val"]
    test_docs = [d for d in docs if d.get("split") == "test"]

    assert len(val_docs) == 15, "Validation partition must have exactly 15 documents"
    assert len(test_docs) == 25, "Test partition must have exactly 25 documents"

    val_set = {d["document_id"] for d in val_docs}
    test_set = {d["document_id"] for d in test_docs}
    assert len(val_set.intersection(test_set)) == 0, "Partitions must be completely disjoint"


def test_config_partition_declarations():
    import yaml
    with open(CALIBRATION_CFG, "r", encoding="utf-8") as f:
        calib_cfg = yaml.safe_load(f)
    with open(EVALUATION_CFG, "r", encoding="utf-8") as f:
        eval_cfg = yaml.safe_load(f)

    assert calib_cfg["calibration"]["dataset_split"] == "val"
    assert eval_cfg["evaluation"]["split"] == "test"
