"""src/safety_recovery/gate.py
Safety-Constrained Recovery Gating Controller G_safe(x).
Maps observable signals and candidate answers to Phase 11 decisions.
"""

from typing import Tuple, Optional
from src.reliability.signals import ObservableSignals
from src.safety_recovery.schema import (
    Phase11State,
    Phase11Action,
    SafetyRecoveryDecision,
)
from src.safety_recovery.verification import VerificationStack
from src.safety_recovery.human_escalation import HumanEscalationController


class SafetyConstrainedGate:
    """Deterministic safety gate G_safe(x) -> {RECOVER, PARTIAL, HUMAN, ABSTAIN}."""

    def __init__(
        self,
        verification_stack: Optional[VerificationStack] = None,
        tau_safe_recovery: float = 0.82,
        tau_partial_recovery: float = 0.74,
    ):
        self.verifier = verification_stack or VerificationStack(tau_safe_confidence=tau_safe_recovery)
        self.tau_safe_recovery = tau_safe_recovery
        self.tau_partial_recovery = tau_partial_recovery

    def evaluate(
        self,
        signals: ObservableSignals,
        candidate_answer: str,
        document_id: str = "doc_eval",
        query_id: str = "q_eval",
    ) -> SafetyRecoveryDecision:
        unc_norm = round(1.0 - signals.raw_confidence, 4)

        # Step 1: Run 7-layer verification
        all_passed, passed_layers, failed_layers = self.verifier.verify_all_layers(
            signals, candidate_answer
        )

        # Condition A: Full Safe Recovery (All 7 layers verified, high confidence)
        if all_passed and signals.raw_confidence >= self.tau_safe_recovery:
            return SafetyRecoveryDecision(
                state=Phase11State.S11_0_SAFE_RECOVERED,
                action=Phase11Action.EMIT_COMPLETE,
                confidence=signals.raw_confidence,
                uncertainty_norm=unc_norm,
                answer_text=candidate_answer,
                is_useful=True,
                is_safe=True,
                passed_layers=passed_layers,
                failed_layers=failed_layers,
                reason="All 7 verification layers successfully validated",
            )

        # Condition B: Safe Partial Recovery (Spatial/Numeric pass, moderate confidence)
        if (
            "layer2_spatial_grounding" in passed_layers
            and "layer4_numeric_consistency" in passed_layers
            and signals.raw_confidence >= self.tau_partial_recovery
        ):
            words = candidate_answer.split()
            partial_text = " ".join(words[:max(1, len(words) // 2)]) if len(words) > 1 else candidate_answer
            return SafetyRecoveryDecision(
                state=Phase11State.S11_1_SAFE_PARTIAL,
                action=Phase11Action.EMIT_PARTIAL,
                confidence=signals.raw_confidence,
                uncertainty_norm=unc_norm,
                answer_text=partial_text,
                is_useful=True,
                is_safe=True,
                passed_layers=passed_layers,
                failed_layers=failed_layers,
                reason="Partial evidence certified under spatial and numeric constraints",
            )

        # Condition C: Human Review Required (Borderline ambiguity; safety constraint prioritizes human review)
        if signals.raw_confidence >= 0.40 and signals.quality_score >= 0.25:
            review_pkg = HumanEscalationController.create_package(
                document_id=document_id,
                query_id=query_id,
                candidate_answer=candidate_answer,
                signals=signals,
                failed_layers=failed_layers,
            )
            return SafetyRecoveryDecision(
                state=Phase11State.S11_3_HUMAN_REVIEW_REQUIRED,
                action=Phase11Action.ESCALATE_TO_HUMAN,
                confidence=signals.raw_confidence,
                uncertainty_norm=unc_norm,
                answer_text=None,
                is_useful=False,
                is_safe=True,
                review_package=review_pkg,
                passed_layers=passed_layers,
                failed_layers=failed_layers,
                reason=f"Verification failed on {len(failed_layers)} layers; escalated to human review for zero-hallucination guarantee",
            )

        # Condition D: Defensive Abstention / Rejection
        return SafetyRecoveryDecision(
            state=Phase11State.S11_4_ABSTAIN,
            action=Phase11Action.ABSTAIN_DEFENSIVE,
            confidence=signals.raw_confidence,
            uncertainty_norm=unc_norm,
            answer_text=None,
            is_useful=False,
            is_safe=True,
            passed_layers=passed_layers,
            failed_layers=failed_layers,
            reason="Severe degradation and low confidence; abstaining defensively",
        )
