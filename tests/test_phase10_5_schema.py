"""tests/test_phase10_5_schema.py
Unit tests for Phase 10.5 recovery schema and state transitions.
"""

import pytest
from src.recovery.schema import (
    RecoveryState,
    RecoveryAction,
    InspectionRegion,
    PartialEvidenceResult,
    RecoveryDecision,
)


def test_recovery_state_values():
    assert RecoveryState.R0_SAFE_COMPLETE.value == "SAFE_COMPLETE"
    assert RecoveryState.R1_SAFE_PARTIAL.value == "SAFE_PARTIAL"
    assert RecoveryState.R2_RECOVERABLE_WITH_RESTORATION.value == "RECOVERABLE_WITH_RESTORATION"
    assert RecoveryState.R3_HUMAN_ESCALATION.value == "HUMAN_ESCALATION"
    assert RecoveryState.R4_UNSAFE_TO_ANSWER.value == "UNSAFE_TO_ANSWER"
    assert RecoveryState.R5_IRRECOVERABLE.value == "IRRECOVERABLE"


def test_inspection_region_instantiation():
    reg = InspectionRegion(
        page_id=1,
        bbox=[0.1, 0.2, 0.5, 0.8],
        defect_type="blur",
        uncertainty_score=0.75,
        description="Region blurred",
    )
    assert reg.page_id == 1
    assert len(reg.bbox) == 4
    assert reg.defect_type == "blur"


def test_recovery_decision_defaults():
    decision = RecoveryDecision(
        state=RecoveryState.R0_SAFE_COMPLETE,
        action=RecoveryAction.EMIT_COMPLETE,
        confidence=0.95,
        uncertainty_norm=0.05,
        answer_text="Test Answer",
        is_useful=True,
        is_safe=True,
    )
    assert decision.is_useful is True
    assert decision.is_safe is True
    assert decision.inspection_regions == []
