"""tests/test_phase11_schema.py
Unit tests for Phase 11 schema, state taxonomy, and data models.
"""

from src.safety_recovery.schema import (
    Phase11State,
    Phase11Action,
    RiskLevel,
    HumanReviewPackage,
    SafetyRecoveryDecision,
)


def test_phase11_states():
    assert Phase11State.S11_0_SAFE_RECOVERED.value == "SAFE_RECOVERED"
    assert Phase11State.S11_1_SAFE_PARTIAL.value == "SAFE_PARTIAL"
    assert Phase11State.S11_2_RECOVERY_WITH_RESTORATION.value == "RECOVERY_WITH_RESTORATION"
    assert Phase11State.S11_3_HUMAN_REVIEW_REQUIRED.value == "HUMAN_REVIEW_REQUIRED"
    assert Phase11State.S11_4_ABSTAIN.value == "ABSTAIN"
    assert Phase11State.S11_5_UNSAFE_RECOVERY_REJECTED.value == "UNSAFE_RECOVERY_REJECTED"


def test_human_review_package():
    pkg = HumanReviewPackage(
        document_id="doc_01",
        page_id=1,
        query_id="q_01",
        candidate_answer="Test",
        evidence_regions=[[0.1, 0.1, 0.5, 0.5]],
        confidence=0.75,
        uncertainty_norm=0.25,
        risk_level=RiskLevel.MEDIUM,
        failure_reason="Test reason",
        suggested_action="Review",
    )
    assert pkg.page_id == 1
    assert pkg.risk_level == RiskLevel.MEDIUM
    assert len(pkg.evidence_regions) == 1
