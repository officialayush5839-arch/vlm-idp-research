"""
Task Evaluator for Computing Benchmark Metrics.
Reuses frozen evaluation metrics from Phase 2 and coordinates from Phase 1.
"""

from __future__ import annotations

from typing import List, Optional, Tuple
from src.benchmark.schema import BenchmarkSample, EvaluationMetricsResult, ModelExecutionResult
from src.evaluation.metrics import (
    compute_anls,
    compute_cer,
    compute_exact_match,
    compute_token_f1,
    compute_wer,
)
from src.ingestion.coordinates import compute_iou


class BenchmarkEvaluator:
    """Evaluates model predictions against task ground truth."""

    def __init__(self, iou_threshold: float = 0.50):
        self.iou_threshold = iou_threshold

    def evaluate(
        self,
        sample: BenchmarkSample,
        execution_result: ModelExecutionResult,
    ) -> EvaluationMetricsResult:
        """Computes comprehensive task metrics for a single model execution."""
        pred = execution_result.answer
        gt_answers = sample.ground_truth_answers

        em = compute_exact_match(pred, gt_answers)
        f1 = compute_token_f1(pred, gt_answers)
        anls = compute_anls(pred, gt_answers)

        primary_gt = gt_answers[0] if gt_answers else ""
        cer = compute_cer(pred, primary_gt) if primary_gt else None
        wer = compute_wer(pred, primary_gt) if primary_gt else None

        # Grounding IoU
        best_iou: Optional[float] = None
        if execution_result.predicted_bboxes and sample.ground_truth_bboxes:
            ious: List[float] = []
            for pred_b in execution_result.predicted_bboxes:
                for gt_b in sample.ground_truth_bboxes:
                    ious.append(compute_iou(pred_b, gt_b))
            best_iou = max(ious) if ious else 0.0
        elif sample.ground_truth_bboxes and not execution_result.predicted_bboxes:
            best_iou = None  # Model does not produce bounding boxes

        # Determine primary metric
        if sample.task_type in ["visual_question_answering", "vqa"]:
            primary_name = "ANLS"
            primary_val = anls
        else:
            primary_name = "F1"
            primary_val = f1

        return EvaluationMetricsResult(
            exact_match=em,
            token_f1=f1,
            anls=anls,
            cer=cer,
            wer=wer,
            grounding_iou=best_iou,
            primary_metric_name=primary_name,
            primary_metric_value=primary_val,
        )
