"""tests/test_phase11_human_escalation.py
Unit tests verifying human escalation review package generation and inspection regions.
"""

from src.safety_recovery.human_escalation import HumanEscalationController
from src.safety_recovery.schema import RiskLevel
from src.reliability.signals import ObservableSignals


def test_human_escalation_package_generation():
    sig = ObservableSignals(
        quality_score=0.40,
        spatial_score=0.35,
        raw_confidence=0.50,
    )
    pkg = HumanEscalationController.create_package(
        document_id="doc_mp_028",
        query_id="q_doc_mp_028",
        candidate_answer="Extracted Date",
        signals=sig,
        failed_layers=["layer2_spatial_grounding", "layer7_calibrated_confidence"],
        page_id=2,
    )
    assert pkg.document_id == "doc_mp_028"
    assert pkg.page_id == 2
    assert pkg.risk_level in (RiskLevel.HIGH, RiskLevel.CRITICAL)
    assert len(pkg.evidence_regions) >= 1
    assert "layer2_spatial_grounding" in pkg.failure_reason
