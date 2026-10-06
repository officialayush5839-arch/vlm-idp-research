"""src/robustness/evaluation.py
Domain-stratified robustness evaluation orchestrator.
"""

from typing import Dict, Any, List
from src.robustness.schema import DomainID, RobustnessEvaluationResult
from src.robustness.robustness_metrics import RobustnessMetricsCalculator
from src.reliability.metrics import ReliabilityMetricsCalculator
from src.reliability.schema import ReliabilityAction


class RobustnessEvaluator:
    """Computes comprehensive domain-stratified metrics and robustness gaps."""

    @staticmethod
    def evaluate_domain_performance(
        domain_id: DomainID,
        baseline_id: str,
        seed: int,
        confidences: List[float],
        predictions: List[str],
        ground_truth: List[str],
        actions: List[ReliabilityAction],
        in_domain_acc_ref: float,
    ) -> RobustnessEvaluationResult:
        metrics = ReliabilityMetricsCalculator.compute(
            confidences=confidences,
            predictions=predictions,
            ground_truth=ground_truth,
            actions=actions,
        )

        sel_acc = metrics.get("selective_accuracy", 0.0)
        gap = RobustnessMetricsCalculator.compute_robustness_gap(in_domain_acc_ref, sel_acc)
        rel_deg = RobustnessMetricsCalculator.compute_relative_degradation(in_domain_acc_ref, sel_acc)

        return RobustnessEvaluationResult(
            domain_id=domain_id,
            baseline_id=baseline_id,
            seed=seed,
            coverage=metrics.get("coverage", 1.0),
            selective_accuracy=sel_acc,
            selective_unsupported_rate=metrics.get("selective_unsupported_rate", 0.0),
            aurc=metrics.get("aurc", 0.0),
            abstention_f1=metrics.get("abstention_f1", 0.0),
            robustness_gap=round(gap, 4),
            relative_degradation=round(rel_deg, 4),
        )
