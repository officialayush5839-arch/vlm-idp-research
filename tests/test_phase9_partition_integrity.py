"""Tests for Phase 9 partition integrity and determinism."""

from pathlib import Path
import json
import pytest
from src.reliability.pipeline import ReliabilityPipeline
from src.reliability.signals import ObservableSignals
from src.reliability.confidence import CalibratedCompositeModel
from src.reliability.abstention import AbstentionPolicy

CORPUS_MANIFEST = Path(__file__).resolve().parent.parent / "experiments" / "phase6" / "indexes" / "corpus_manifest.json"


def test_partition_integrity_val_and_test():
    assert CORPUS_MANIFEST.exists()
    with open(CORPUS_MANIFEST, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    docs = manifest.get("documents", [])
    val_docs = [d for d in docs if d.get("split") == "val"]
    test_docs = [d for d in docs if d.get("split") == "test"]

    assert len(val_docs) == 15, "Validation partition must have exactly 15 documents"
    assert len(test_docs) == 25, "Test partition must have exactly 25 documents"

    # Set disjointness
    val_ids = {d["document_id"] for d in val_docs}
    test_ids = {d["document_id"] for d in test_docs}
    assert len(val_ids.intersection(test_ids)) == 0, "Validation and test partitions must be strictly disjoint"


def test_pipeline_determinism():
    pipeline1 = ReliabilityPipeline()
    pipeline2 = ReliabilityPipeline()

    p3 = {"quality_score": 0.85}
    p6 = {"retrieval_score": 0.75}
    p7 = {"sufficiency_score": 0.90, "spatial_overlap": 0.80, "semantic_similarity": 0.70}
    p8 = {"agreement_score": 0.95, "raw_confidence": 0.85}

    res1 = pipeline1.process("doc_01", "q_01", p3, p6, p7, p8)
    res2 = pipeline2.process("doc_01", "q_01", p3, p6, p7, p8)

    assert res1.decision.action == res2.decision.action
    assert pytest.approx(res1.calibrated_confidence, 1e-6) == res2.calibrated_confidence
    assert pytest.approx(res1.uncertainty_vector.l2_norm, 1e-6) == res2.uncertainty_vector.l2_norm
