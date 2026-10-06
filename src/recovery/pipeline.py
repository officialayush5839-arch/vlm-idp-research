"""src/recovery/pipeline.py
Master Recovery Pipeline and Baselines (B10.5-0 through B10.5-5).
"""

from typing import Dict, Any, Optional
from src.recovery.schema import (
    RecoveryState,
    RecoveryAction,
    RecoveryDecision,
    InspectionRegion,
)
from src.recovery.eligibility import RecoveryEligibilityGate
from src.recovery.preprocessing import VisualPreprocessingRecovery
from src.recovery.retrieval_recovery import RetrievalRecoveryRetrier
from src.recovery.partial_evidence import PartialEvidenceExtractor
from src.recovery.escalation import HumanEscalationManager
from src.recovery.safety_gate import EvidenceSafetyGate
from src.reliability.signals import ObservableSignals
from src.reliability.baselines import BaselineB9_5_Proposed
from src.reliability.schema import ReliabilityAction


class RecoveryPipeline:
    """Orchestrates candidate baselines B10.5-0 through B10.5-5."""

    def __init__(self):
        self.proposed_reliability = BaselineB9_5_Proposed()
        self.eligibility_gate = RecoveryEligibilityGate()
        self.preprocessor = VisualPreprocessingRecovery()
        self.retrier = RetrievalRecoveryRetrier()
        self.partial_extractor = PartialEvidenceExtractor()
        self.escalation_mgr = HumanEscalationManager()
        self.safety_gate = EvidenceSafetyGate()

    def evaluate_sample(
        self,
        baseline_id: str,
        signals: ObservableSignals,
        candidate_answer: str = "ans",
    ) -> RecoveryDecision:
        # First evaluate Phase 9 / Phase 10 baseline reliability decision
        primary_decision = self.proposed_reliability.evaluate(signals)

        # If primary pipeline ACCEPTED, then state is R0 (SAFE_COMPLETE)
        if primary_decision.action in (ReliabilityAction.ACCEPT, ReliabilityAction.ACCEPT_WITH_WARNING):
            return RecoveryDecision(
                state=RecoveryState.R0_SAFE_COMPLETE,
                action=RecoveryAction.EMIT_COMPLETE,
                confidence=primary_decision.confidence,
                uncertainty_norm=primary_decision.uncertainty_norm,
                answer_text=candidate_answer,
                is_useful=True,
                is_safe=True,
                operating_point="primary_accepted",
                reason=primary_decision.reason,
            )

        # Baseline B10.5-0: Reference Abstention (no recovery attempted)
        if baseline_id == "B10.5-0":
            return RecoveryDecision(
                state=RecoveryState.R4_UNSAFE_TO_ANSWER,
                action=RecoveryAction.ABSTAIN_UNSAFE,
                confidence=primary_decision.confidence,
                uncertainty_norm=primary_decision.uncertainty_norm,
                answer_text=None,
                is_useful=False,
                is_safe=True,
                operating_point="reference_abstention",
                reason="B10.5-0 Reference: Abstaining without recovery",
            )

        # Baseline B10.5-4: Escalation Pathway Only
        if baseline_id == "B10.5-4":
            regions = self.escalation_mgr.generate_inspection_regions(signals)
            return RecoveryDecision(
                state=RecoveryState.R3_HUMAN_ESCALATION,
                action=RecoveryAction.ESCALATE_TO_HUMAN,
                confidence=primary_decision.confidence,
                uncertainty_norm=primary_decision.uncertainty_norm,
                answer_text=None,
                is_useful=False,
                is_safe=True,
                inspection_regions=regions,
                operating_point="escalation_only",
                reason="B10.5-4 Escalation: Human inspection regions flagged",
            )

        # Check recovery eligibility
        is_eligible, elig_reason = self.eligibility_gate.evaluate_eligibility(signals)
        if not is_eligible:
            return RecoveryDecision(
                state=RecoveryState.R5_IRRECOVERABLE,
                action=RecoveryAction.REJECT_IRRECOVERABLE,
                confidence=primary_decision.confidence,
                uncertainty_norm=primary_decision.uncertainty_norm,
                answer_text=None,
                is_useful=False,
                is_safe=True,
                operating_point="ineligible",
                reason=elig_reason,
            )

        # Baseline B10.5-1: Preprocessing Recovery Only
        if baseline_id == "B10.5-1":
            restored_signals = self.preprocessor.apply_recovery(signals)
            safe, safe_reason = self.safety_gate.verify_safety(restored_signals)
            if safe and restored_signals.raw_confidence >= 0.55:
                return RecoveryDecision(
                    state=RecoveryState.R2_RECOVERABLE_WITH_RESTORATION,
                    action=RecoveryAction.RESTORE_AND_RETRY,
                    confidence=restored_signals.raw_confidence,
                    uncertainty_norm=1.0 - restored_signals.quality_score,
                    answer_text=candidate_answer,
                    is_useful=True,
                    is_safe=True,
                    recovery_strategy="preprocessing_restoration",
                    reason="Restoration succeeded and satisfied safety gate",
                )
            else:
                return RecoveryDecision(
                    state=RecoveryState.R4_UNSAFE_TO_ANSWER,
                    action=RecoveryAction.ABSTAIN_UNSAFE,
                    confidence=restored_signals.raw_confidence,
                    uncertainty_norm=1.0 - restored_signals.quality_score,
                    answer_text=None,
                    is_useful=False,
                    is_safe=True,
                    recovery_strategy="preprocessing_restoration",
                    reason=f"Restoration failed safety verification: {safe_reason}",
                )

        # Baseline B10.5-2: Retrieval Retry Only
        if baseline_id == "B10.5-2":
            retry_signals = self.retrier.retry(signals)
            safe, safe_reason = self.safety_gate.verify_safety(retry_signals)
            if safe and retry_signals.raw_confidence >= 0.55:
                return RecoveryDecision(
                    state=RecoveryState.R0_SAFE_COMPLETE,
                    action=RecoveryAction.EMIT_COMPLETE,
                    confidence=retry_signals.raw_confidence,
                    uncertainty_norm=1.0 - retry_signals.retrieval_score,
                    answer_text=candidate_answer,
                    is_useful=True,
                    is_safe=True,
                    recovery_strategy="retrieval_retry",
                    reason="Retrieval retry succeeded and satisfied safety gate",
                )
            else:
                return RecoveryDecision(
                    state=RecoveryState.R4_UNSAFE_TO_ANSWER,
                    action=RecoveryAction.ABSTAIN_UNSAFE,
                    confidence=retry_signals.raw_confidence,
                    uncertainty_norm=1.0 - retry_signals.retrieval_score,
                    answer_text=None,
                    is_useful=False,
                    is_safe=True,
                    recovery_strategy="retrieval_retry",
                    reason=f"Retrieval retry failed safety verification: {safe_reason}",
                )

        # Baseline B10.5-3: Partial Evidence Pathway Only
        if baseline_id == "B10.5-3":
            part_res = self.partial_extractor.extract_partial(candidate_answer, signals)
            if part_res.is_partial and len(part_res.extracted_subspan) > 0:
                return RecoveryDecision(
                    state=RecoveryState.R1_SAFE_PARTIAL,
                    action=RecoveryAction.EMIT_PARTIAL,
                    confidence=signals.raw_confidence,
                    uncertainty_norm=1.0 - part_res.grounding_score,
                    answer_text=part_res.extracted_subspan,
                    is_useful=True,
                    is_safe=True,
                    recovery_strategy="partial_evidence",
                    reason="Partial evidence verified and emitted",
                )
            else:
                return RecoveryDecision(
                    state=RecoveryState.R4_UNSAFE_TO_ANSWER,
                    action=RecoveryAction.ABSTAIN_UNSAFE,
                    confidence=signals.raw_confidence,
                    uncertainty_norm=primary_decision.uncertainty_norm,
                    answer_text=None,
                    is_useful=False,
                    is_safe=True,
                    recovery_strategy="partial_evidence",
                    reason="Could not extract verified partial evidence",
                )

        # Baseline B10.5-5: Proposed Combined Recovery System
        if baseline_id == "B10.5-5":
            # 1. First attempt visual restoration if visual quality is the primary defect
            if signals.quality_score < 0.60:
                restored_signals = self.preprocessor.apply_recovery(signals)
                safe, _ = self.safety_gate.verify_safety(restored_signals)
                if safe and restored_signals.raw_confidence >= 0.55:
                    return RecoveryDecision(
                        state=RecoveryState.R2_RECOVERABLE_WITH_RESTORATION,
                        action=RecoveryAction.RESTORE_AND_RETRY,
                        confidence=restored_signals.raw_confidence,
                        uncertainty_norm=1.0 - restored_signals.quality_score,
                        answer_text=candidate_answer,
                        is_useful=True,
                        is_safe=True,
                        recovery_strategy="preprocessing_restoration",
                        reason="Combined system: visual restoration succeeded",
                    )

            # 2. If retrieval margin was low, retry retrieval with window expansion
            if signals.retrieval_score < 0.65:
                retry_signals = self.retrier.retry(signals)
                safe, _ = self.safety_gate.verify_safety(retry_signals)
                if safe and retry_signals.raw_confidence >= 0.55:
                    return RecoveryDecision(
                        state=RecoveryState.R0_SAFE_COMPLETE,
                        action=RecoveryAction.EMIT_COMPLETE,
                        confidence=retry_signals.raw_confidence,
                        uncertainty_norm=1.0 - retry_signals.retrieval_score,
                        answer_text=candidate_answer,
                        is_useful=True,
                        is_safe=True,
                        recovery_strategy="retrieval_retry",
                        reason="Combined system: retrieval retry succeeded",
                    )

            # 3. If full answer cannot be certified, extract verified partial evidence
            part_res = self.partial_extractor.extract_partial(candidate_answer, signals)
            if part_res.is_partial and len(part_res.extracted_subspan) > 0:
                return RecoveryDecision(
                    state=RecoveryState.R1_SAFE_PARTIAL,
                    action=RecoveryAction.EMIT_PARTIAL,
                    confidence=signals.raw_confidence,
                    uncertainty_norm=1.0 - part_res.grounding_score,
                    answer_text=part_res.extracted_subspan,
                    is_useful=True,
                    is_safe=True,
                    recovery_strategy="partial_evidence",
                    reason="Combined system: verified partial evidence emitted",
                )

            # 4. If moderate uncertainty persists, escalate to human with inspection regions
            if signals.raw_confidence >= 0.40:
                regions = self.escalation_mgr.generate_inspection_regions(signals)
                return RecoveryDecision(
                    state=RecoveryState.R3_HUMAN_ESCALATION,
                    action=RecoveryAction.ESCALATE_TO_HUMAN,
                    confidence=signals.raw_confidence,
                    uncertainty_norm=primary_decision.uncertainty_norm,
                    answer_text=None,
                    is_useful=False,
                    is_safe=True,
                    inspection_regions=regions,
                    recovery_strategy="escalation",
                    reason="Combined system: escalated to human review with inspection regions",
                )

            # 5. Otherwise abstain as unsafe to answer
            return RecoveryDecision(
                state=RecoveryState.R4_UNSAFE_TO_ANSWER,
                action=RecoveryAction.ABSTAIN_UNSAFE,
                confidence=signals.raw_confidence,
                uncertainty_norm=primary_decision.uncertainty_norm,
                answer_text=None,
                is_useful=False,
                is_safe=True,
                recovery_strategy="none",
                reason="Combined system: safety thresholds not met",
            )

        raise ValueError(f"Unknown baseline: {baseline_id}")
