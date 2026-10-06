"""Phase 9 schema tests."""

import pytest
from src.reliability.schema import (
    ReliabilityAction,
    FailureMode,
    UncertaintyVector,
    ReliabilityDecision,
    ReliabilityPackage,
    FailureModeResult,
)


def test_reliability_action_values():
    actions = {a.value for a in ReliabilityAction}
    assert actions == {"ACCEPT", "ACCEPT_WITH_WARNING", "ESCALATE", "ABSTAIN"}


def test_failure_mode_values():
    assert len(FailureMode) == 8
    assert FailureMode.F01_RETRIEVAL_FAILURE.value == "F01_RETRIEVAL_FAILURE"
    assert FailureMode.F08_MODEL_DISAGREEMENT.value == "F08_MODEL_DISAGREEMENT"


def test_uncertainty_vector_normalization_and_array():
    vec = UncertaintyVector(
        u_retrieval=0.1,
        u_semantic=0.2,
        u_spatial=0.3,
        u_numeric=0.4,
        u_table=0.5,
        u_sufficiency=0.6,
        u_quality=0.7,
        u_agreement=0.8,
    )
    arr = vec.to_array()
    assert len(arr) == 8
    assert arr[0] == 0.1
    assert arr[7] == 0.8
    assert 0.0 <= vec.l2_norm <= 1.0


def test_uncertainty_vector_clipping():
    vec = UncertaintyVector(
        u_retrieval=-0.5,
        u_semantic=1.5,
        u_spatial=0.5,
        u_numeric=0.5,
        u_table=0.5,
        u_sufficiency=0.5,
        u_quality=0.5,
        u_agreement=0.5,
    )
    arr = vec.to_array()
    assert arr[0] == 0.0
    assert arr[1] == 1.0


def test_reliability_decision_and_package():
    vec = UncertaintyVector.zeros()
    decision = ReliabilityDecision(
        action=ReliabilityAction.ACCEPT,
        confidence=0.92,
        uncertainty_norm=vec.l2_norm,
        operating_point="balanced",
        reason="Low aggregate uncertainty across all modalities",
    )
    package = ReliabilityPackage(
        doc_id="doc_001",
        query_id="q_001",
        decision=decision,
        uncertainty_vector=vec,
        raw_confidence=0.90,
        calibrated_confidence=0.92,
    )
    d = package.to_dict()
    assert d["doc_id"] == "doc_001"
    assert d["decision"]["action"] == "ACCEPT"
    assert d["decision"]["confidence"] == 0.92
