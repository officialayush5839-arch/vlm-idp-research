"""src/safety_recovery/metrics.py
Phase 11 Safety and Utility Evaluation Metrics.
Computes URR (Unsafe Recovery Rate), SUC (Safe Useful Coverage), coverage, selective accuracy, and human escalation rates.
"""

from typing import List, Dict, Any
from src.safety_recovery.schema import SafetyRecoveryDecision, Phase11Action, Phase11State


class Phase11MetricsCalculator:
    """Computes comprehensive metrics for Phase 11 evaluation."""

    @staticmethod
    def compute_metrics(
        decisions: List[SafetyRecoveryDecision],
        reference_targets: List[str],
        predictions: List[str],
    ) -> Dict[str, float]:
        n = len(decisions)
        if n == 0:
            return {}

        is_correct = [
            str(p).strip().lower() == str(g).strip().lower()
            for p, g in zip(predictions, reference_targets)
        ]

        # Automatically emitted answers (EMIT_COMPLETE or EMIT_PARTIAL)
        emitted_mask = [
            d.action in (Phase11Action.EMIT_COMPLETE, Phase11Action.EMIT_PARTIAL)
            for d in decisions
        ]
        num_emitted = sum(emitted_mask)

        # Safe useful outputs (emitted AND correct)
        safe_useful_count = sum(
            1 for e, c in zip(emitted_mask, is_correct) if e and c
        )
        suc = safe_useful_count / n

        # Unsafe answers (emitted AND incorrect)
        unsafe_count = sum(
            1 for e, c in zip(emitted_mask, is_correct) if e and not c
        )

        # Primary URR: Unsafe answers / total evaluations
        urr = unsafe_count / n

        # Conditional URR: Unsafe answers / total emitted answers
        conditional_urr = (unsafe_count / num_emitted) if num_emitted > 0 else 0.0

        # Coverage: Fraction of queries answered automatically
        coverage = num_emitted / n

        # Selective accuracy among emitted answers
        selective_acc = (safe_useful_count / num_emitted) if num_emitted > 0 else 0.0

        # Human escalation rate
        escalated_count = sum(
            1 for d in decisions if d.action == Phase11Action.ESCALATE_TO_HUMAN
        )
        escalation_rate = escalated_count / n

        # Abstention rate
        abstained_count = sum(
            1 for d in decisions if d.action in (Phase11Action.ABSTAIN_DEFENSIVE, Phase11Action.REJECT_UNSAFE)
        )
        abstention_rate = abstained_count / n

        return {
            "safe_useful_coverage": round(suc, 4),
            "unsafe_recovery_rate": round(urr, 4),
            "conditional_urr": round(conditional_urr, 4),
            "coverage": round(coverage, 4),
            "selective_accuracy": round(selective_acc, 4),
            "human_escalation_rate": round(escalation_rate, 4),
            "abstention_rate": round(abstention_rate, 4),
            "total_samples": n,
            "num_emitted": num_emitted,
            "num_safe_useful": safe_useful_count,
            "num_unsafe": unsafe_count,
            "num_escalated": escalated_count,
            "num_abstained": abstained_count,
        }
