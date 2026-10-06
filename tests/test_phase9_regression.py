"""Tests for Phase 9 regression against frozen Phase 8 interfaces."""

from pathlib import Path
import json
import pytest
from src.reliability.signals import ObservableSignals
from src.reliability.pipeline import ReliabilityPipeline


def test_phase8_models_exist_and_readable():
    models_dir = Path(__file__).resolve().parent.parent / "experiments" / "phase8" / "models"
    manifest_file = models_dir / "manifest.json"
    assert manifest_file.exists()
    with open(manifest_file, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    assert "calibrator" in manifest or "calibrator_type" in manifest or len(manifest) > 0


def test_reliability_pipeline_backward_compatibility():
    # Ensure pipeline seamlessly processes simulated Phase 8 signals
    p3 = {"quality_score": 0.72}
    p6 = {"retrieval_score": 0.65}
    p7 = {"sufficiency_score": 0.80, "spatial_overlap": 0.60}
    p8 = {"agreement_score": 0.85, "raw_confidence": 0.78}

    pipeline = ReliabilityPipeline()
    pkg = pipeline.process(
        doc_id="doc_mp_001",
        query_id="q_001",
        phase3_output=p3,
        phase6_output=p6,
        phase7_output=p7,
        phase8_output=p8,
    )

    assert pkg.doc_id == "doc_mp_001"
    assert pkg.decision.action in ("ACCEPT", "ACCEPT_WITH_WARNING", "ESCALATE", "ABSTAIN")
    assert 0.0 <= pkg.calibrated_confidence <= 1.0
