"""src/reliability/metrics.py
Evaluation metrics for selective prediction, abstention, calibration, and reliability.
"""

from typing import List, Dict, Any
import numpy as np
from src.reliability.schema import ReliabilityAction
from src.reliability.risk import RiskCoverageCalculator


class ReliabilityMetricsCalculator:
    """Computes comprehensive Phase 9 evaluation metrics."""

    @staticmethod
    def compute(
        confidences: List[float],
        predictions: List[str],
        ground_truth: List[str],
        actions: List[ReliabilityAction],
    ) -> Dict[str, float]:
        n = len(predictions)
        if n == 0:
            return {}

        is_correct = [
            str(p).strip().lower() == str(g).strip().lower()
            for p, g in zip(predictions, ground_truth)
        ]

        # Accepted actions are ACCEPT and ACCEPT_WITH_WARNING
        accepted_mask = [
            a in (ReliabilityAction.ACCEPT, ReliabilityAction.ACCEPT_WITH_WARNING)
            for a in actions
        ]
        num_accepted = sum(accepted_mask)
        coverage = num_accepted / n

        if num_accepted > 0:
            accepted_correct = [c for c, m in zip(is_correct, accepted_mask) if m]
            selective_acc = sum(accepted_correct) / num_accepted
            selective_risk = 1.0 - selective_acc
        else:
            selective_acc = 0.0
            selective_risk = 0.0

        # Abstention precision / recall against incorrect answers
        incorrect_mask = [not c for c in is_correct]
        abstained_mask = [
            a in (ReliabilityAction.ABSTAIN, ReliabilityAction.ESCALATE)
            for a in actions
        ]

        num_abstained = sum(abstained_mask)
        num_incorrect = sum(incorrect_mask)

        # True Positives for abstention: was incorrect AND abstained
        tp_abstain = sum(1 for inc, abs_ in zip(incorrect_mask, abstained_mask) if inc and abs_)

        abstain_precision = (tp_abstain / num_abstained) if num_abstained > 0 else 0.0
        abstain_recall = (tp_abstain / num_incorrect) if num_incorrect > 0 else 1.0
        if abstain_precision + abstain_recall > 0:
            abstain_f1 = (
                2.0 * abstain_precision * abstain_recall / (abstain_precision + abstain_recall)
            )
        else:
            abstain_f1 = 0.0

        # Risk-coverage curve & AURC
        curve = RiskCoverageCalculator.compute_curve(confidences, is_correct)

        # Expected Calibration Error (ECE)
        bins = 10
        bin_edges = np.linspace(0, 1, bins + 1)
        ece = 0.0
        for i in range(bins):
            b_min, b_max = bin_edges[i], bin_edges[i + 1]
            in_bin = [
                idx
                for idx, c in enumerate(confidences)
                if (b_min <= c < b_max) or (i == bins - 1 and b_min <= c <= b_max)
            ]
            if in_bin:
                bin_acc = sum(is_correct[idx] for idx in in_bin) / len(in_bin)
                bin_conf = sum(confidences[idx] for idx in in_bin) / len(in_bin)
                ece += (len(in_bin) / n) * abs(bin_acc - bin_conf)

        # Brier Score
        brier = float(
            np.mean([(c - (1.0 if corr else 0.0)) ** 2 for c, corr in zip(confidences, is_correct)])
        )

        return {
            "coverage": round(coverage, 4),
            "selective_accuracy": round(selective_acc, 4),
            "selective_unsupported_rate": round(selective_risk, 4),
            "aurc": round(curve.aurc, 4),
            "e_aurc": round(curve.e_aurc, 4),
            "abstention_precision": round(abstain_precision, 4),
            "abstention_recall": round(abstain_recall, 4),
            "abstention_f1": round(abstain_f1, 4),
            "expected_calibration_error": round(ece, 4),
            "brier_score": round(brier, 4),
        }
