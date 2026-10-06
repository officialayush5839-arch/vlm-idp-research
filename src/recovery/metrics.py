"""src/recovery/metrics.py
Safe Useful Coverage (SUC) and Unsafe Recovery Rate (URR) metrics.
"""

from typing import List, Dict, Any
from src.recovery.schema import RecoveryDecision, RecoveryState, RecoveryAction


class RecoveryMetricsCalculator:
    """Computes specialized Phase 10.5 metrics for safety-preserving recovery."""

    @staticmethod
    def compute_metrics(
        decisions: List[RecoveryDecision],
        reference_targets: List[str],
        predictions: List[str],
    ) -> Dict[str, float]:
        n = len(decisions)
        if n == 0:
            return {}

        # Correctness check
        is_correct = [
            str(p).strip().lower() == str(g).strip().lower()
            for p, g in zip(predictions, reference_targets)
        ]

        # Useful outputs: EMIT_COMPLETE, EMIT_PARTIAL, or RESTORE_AND_RETRY
        useful_mask = [
            d.action in (
                RecoveryAction.EMIT_COMPLETE,
                RecoveryAction.EMIT_PARTIAL,
                RecoveryAction.RESTORE_AND_RETRY,
            )
            for d in decisions
        ]
        num_useful = sum(useful_mask)

        # Safe useful outputs: useful AND correct
        safe_useful_count = sum(
            1 for u, c in zip(useful_mask, is_correct) if u and c
        )
        suc = safe_useful_count / n

        # Unsafe Recovery Rate (URR): emitted an answer BUT was incorrect
        unsafe_recovered_count = sum(
            1 for u, c in zip(useful_mask, is_correct) if u and not c
        )
        urr = unsafe_recovered_count / n

        # Raw Coverage
        coverage = num_useful / n

        # Selective Accuracy among emitted answers
        selective_acc = (safe_useful_count / num_useful) if num_useful > 0 else 0.0

        # State distributions
        state_counts = {}
        for d in decisions:
            s_name = d.state.value if hasattr(d.state, "value") else str(d.state)
            state_counts[s_name] = state_counts.get(s_name, 0) + 1

        state_dist = {f"pct_{k}": round(v / n, 4) for k, v in state_counts.items()}

        res = {
            "safe_useful_coverage": round(suc, 4),
            "unsafe_recovery_rate": round(urr, 4),
            "coverage": round(coverage, 4),
            "selective_accuracy": round(selective_acc, 4),
            "total_samples": n,
            "num_useful": num_useful,
            "num_safe_useful": safe_useful_count,
            "num_unsafe": unsafe_recovered_count,
        }
        res.update(state_dist)
        return res
