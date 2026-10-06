"""Audit test suite for Phase 9 static and adversarial runtime leakage."""

from pathlib import Path
import pytest
from src.reliability.audit import ZeroLeakageAuditor
from src.reliability.pipeline import ReliabilityPipeline

SRC_RELIABILITY_DIR = Path("src/reliability")


def test_static_ast_audit():
    violations = ZeroLeakageAuditor.audit_reliability_package(SRC_RELIABILITY_DIR)
    assert len(violations) == 0, f"Found AST violations: {violations}"


def test_adversarial_runtime_leakage():
    pipeline = ReliabilityPipeline()

    res_clean = pipeline.process(
        doc_id="doc_audit",
        query_id="q_audit",
        phase3_output={"quality_score": 0.85},
        phase6_output={"retrieval_score": 0.80},
        phase7_output={"sufficiency_score": 0.90, "spatial_overlap": 0.85},
        phase8_output={"agreement_score": 0.95, "raw_confidence": 0.88},
    )

    res_injected = pipeline.process(
        doc_id="doc_audit",
        query_id="q_audit",
        phase3_output={"quality_score": 0.85, "gold_label": "FORBIDDEN"},
        phase6_output={"retrieval_score": 0.80, "oracle_rank": 1},
        phase7_output={"sufficiency_score": 0.90, "spatial_overlap": 0.85, "ground_truth": "TEST_GT"},
        phase8_output={"agreement_score": 0.95, "raw_confidence": 0.88, "test_score": 1.0},
        metadata={"gold_answer": "FORBIDDEN_ANSWER", "test_split": "test"},
    )

    assert res_clean.decision.action == res_injected.decision.action
    assert res_clean.calibrated_confidence == res_injected.calibrated_confidence
    assert res_clean.uncertainty_vector.to_array() == res_injected.uncertainty_vector.to_array()
