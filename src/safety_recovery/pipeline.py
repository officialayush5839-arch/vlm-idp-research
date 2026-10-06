"""src/safety_recovery/pipeline.py
Phase 11 Master Safety Recovery Pipeline.
Implements and orchestrates Baselines B11-0 through B11-6.
"""

from typing import Dict, Any, Optional
from src.reliability.signals import ObservableSignals
from src.safety_recovery.schema import (
    Phase11State,
    Phase11Action,
    SafetyRecoveryDecision,
)
from src.safety_recovery.gate import SafetyConstrainedGate
from src.safety_recovery.verification import VerificationStack
from src.safety_recovery.human_escalation import HumanEscalationController
from src.recovery.pipeline import RecoveryPipeline


class Phase11SafetyPipeline:
    """Evaluates candidate baselines B11-0 through B11-6."""

    def __init__(self):
        self.p10_5_pipeline = RecoveryPipeline()
        self.verifier = VerificationStack()
        self.safety_gate = SafetyConstrainedGate(verification_stack=self.verifier)

    def evaluate_sample(
        self,
        baseline_id: str,
        signals: ObservableSignals,
        candidate_answer: str = "ans",
        document_id: str = "doc_eval",
        query_id: str = "q_eval",
    ) -> SafetyRecoveryDecision:
        unc_norm = round(1.0 - signals.raw_confidence, 4)

        # Baseline B11-0: Phase 10 Reference Abstention
        if baseline_id == "B11-0":
            dec_p10 = self.p10_5_pipeline.evaluate_sample("B10.5-0", signals, candidate_answer)
            if dec_p10.is_useful:
                return SafetyRecoveryDecision(
                    state=Phase11State.S11_0_SAFE_RECOVERED,
                    action=Phase11Action.EMIT_COMPLETE,
                    confidence=dec_p10.confidence,
                    uncertainty_norm=dec_p10.uncertainty_norm,
                    answer_text=candidate_answer,
                    is_useful=True,
                    is_safe=True,
                    reason="B11-0: Primary answer accepted",
                )
            else:
                return SafetyRecoveryDecision(
                    state=Phase11State.S11_4_ABSTAIN,
                    action=Phase11Action.ABSTAIN_DEFENSIVE,
                    confidence=dec_p10.confidence,
                    uncertainty_norm=dec_p10.uncertainty_norm,
                    answer_text=None,
                    is_useful=False,
                    is_safe=True,
                    reason="B11-0: Defensive abstention",
                )

        # Baseline B11-1: Phase 10.5 Combined Recovery (B10.5-5)
        if baseline_id == "B11-1":
            dec_p10_5 = self.p10_5_pipeline.evaluate_sample("B10.5-5", signals, candidate_answer)
            if dec_p10_5.is_useful:
                act = Phase11Action.EMIT_PARTIAL if "partial" in dec_p10_5.reason.lower() else Phase11Action.EMIT_COMPLETE
                st = Phase11State.S11_1_SAFE_PARTIAL if act == Phase11Action.EMIT_PARTIAL else Phase11State.S11_0_SAFE_RECOVERED
                return SafetyRecoveryDecision(
                    state=st,
                    action=act,
                    confidence=dec_p10_5.confidence,
                    uncertainty_norm=dec_p10_5.uncertainty_norm,
                    answer_text=dec_p10_5.answer_text,
                    is_useful=True,
                    is_safe=dec_p10_5.is_safe,
                    reason=f"B11-1: {dec_p10_5.reason}",
                )
            else:
                return SafetyRecoveryDecision(
                    state=Phase11State.S11_4_ABSTAIN,
                    action=Phase11Action.ABSTAIN_DEFENSIVE,
                    confidence=dec_p10_5.confidence,
                    uncertainty_norm=dec_p10_5.uncertainty_norm,
                    answer_text=None,
                    is_useful=False,
                    is_safe=True,
                    reason=f"B11-1: {dec_p10_5.reason}",
                )

        # Baseline B11-2: Strict Evidence-Only Recovery
        if baseline_id == "B11-2":
            if signals.sufficiency_score >= 0.70 and signals.spatial_score >= 0.60:
                return SafetyRecoveryDecision(
                    state=Phase11State.S11_0_SAFE_RECOVERED,
                    action=Phase11Action.EMIT_COMPLETE,
                    confidence=signals.raw_confidence,
                    uncertainty_norm=unc_norm,
                    answer_text=candidate_answer,
                    is_useful=True,
                    is_safe=True,
                    reason="B11-2: Strict evidence criteria met",
                )
            else:
                return SafetyRecoveryDecision(
                    state=Phase11State.S11_4_ABSTAIN,
                    action=Phase11Action.ABSTAIN_DEFENSIVE,
                    confidence=signals.raw_confidence,
                    uncertainty_norm=unc_norm,
                    answer_text=None,
                    is_useful=False,
                    is_safe=True,
                    reason="B11-2: Evidence threshold failed",
                )

        # Baseline B11-3: Confidence-Gated Recovery
        if baseline_id == "B11-3":
            if signals.raw_confidence >= 0.80:
                return SafetyRecoveryDecision(
                    state=Phase11State.S11_0_SAFE_RECOVERED,
                    action=Phase11Action.EMIT_COMPLETE,
                    confidence=signals.raw_confidence,
                    uncertainty_norm=unc_norm,
                    answer_text=candidate_answer,
                    is_useful=True,
                    is_safe=True,
                    reason="B11-3: Confidence cutoff passed",
                )
            else:
                return SafetyRecoveryDecision(
                    state=Phase11State.S11_4_ABSTAIN,
                    action=Phase11Action.ABSTAIN_DEFENSIVE,
                    confidence=signals.raw_confidence,
                    uncertainty_norm=unc_norm,
                    answer_text=None,
                    is_useful=False,
                    is_safe=True,
                    reason="B11-3: Confidence below cutoff",
                )

        # Baseline B11-4: Confidence + Evidence + Numeric Verification
        if baseline_id == "B11-4":
            if (
                signals.raw_confidence >= 0.80
                and signals.sufficiency_score >= 0.60
                and signals.numeric_discrepancy <= 0.18
            ):
                return SafetyRecoveryDecision(
                    state=Phase11State.S11_0_SAFE_RECOVERED,
                    action=Phase11Action.EMIT_COMPLETE,
                    confidence=signals.raw_confidence,
                    uncertainty_norm=unc_norm,
                    answer_text=candidate_answer,
                    is_useful=True,
                    is_safe=True,
                    reason="B11-4: Confidence, evidence, and numeric checks passed",
                )
            else:
                return SafetyRecoveryDecision(
                    state=Phase11State.S11_4_ABSTAIN,
                    action=Phase11Action.ABSTAIN_DEFENSIVE,
                    confidence=signals.raw_confidence,
                    uncertainty_norm=unc_norm,
                    answer_text=None,
                    is_useful=False,
                    is_safe=True,
                    reason="B11-4: Numeric or evidence verification failed",
                )

        # Baseline B11-5: Confidence + Evidence + Human Escalation
        if baseline_id == "B11-5":
            if signals.raw_confidence >= 0.82 and signals.sufficiency_score >= 0.60:
                return SafetyRecoveryDecision(
                    state=Phase11State.S11_0_SAFE_RECOVERED,
                    action=Phase11Action.EMIT_COMPLETE,
                    confidence=signals.raw_confidence,
                    uncertainty_norm=unc_norm,
                    answer_text=candidate_answer,
                    is_useful=True,
                    is_safe=True,
                    reason="B11-5: Certified recovery emitted",
                )
            else:
                pkg = HumanEscalationController.create_package(
                    document_id, query_id, candidate_answer, signals, ["confidence_or_evidence"]
                )
                return SafetyRecoveryDecision(
                    state=Phase11State.S11_3_HUMAN_REVIEW_REQUIRED,
                    action=Phase11Action.ESCALATE_TO_HUMAN,
                    confidence=signals.raw_confidence,
                    uncertainty_norm=unc_norm,
                    answer_text=None,
                    is_useful=False,
                    is_safe=True,
                    review_package=pkg,
                    reason="B11-5: Escalated to human review",
                )

        # Baseline B11-6: Proposed Safety-Constrained Recovery System
        if baseline_id == "B11-6":
            return self.safety_gate.evaluate(
                signals=signals,
                candidate_answer=candidate_answer,
                document_id=document_id,
                query_id=query_id,
            )

        raise ValueError(f"Unknown baseline: {baseline_id}")
