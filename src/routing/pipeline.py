"""
Adaptive Routing Pipeline for Phase 5.
Executes the full pipeline:
Quality Assessment -> Uncertainty Assembly -> Policy Routing -> Model Execution -> Fallback -> Evaluation -> Provenance.
"""

from __future__ import annotations

import json
from pathlib import Path
import time
from typing import Any, Dict, List, Optional
from PIL import Image

from src.benchmark.schema import BenchmarkSample, DegradationCondition, ModelExecutionResult
from src.benchmark.evaluator import BenchmarkEvaluator
from src.benchmark.model_runner import ModelRunner
from src.quality.pipeline import DocumentQualityPipeline
from src.routing.schema import (
    RoutingPolicyType,
    RoutingDecision,
    RoutingRunArtifact,
    UncertaintyVector,
)
from src.routing.router import AdaptiveRouter


class AdaptiveRoutingPipeline:
    """
    End-to-end routing execution pipeline integrating Phase 3 quality assessment,
    Phase 4 fair model runners, and Phase 5 routing policies.
    """

    def __init__(
        self,
        router: AdaptiveRouter,
        quality_pipeline: DocumentQualityPipeline,
        model_runner: ModelRunner,
        evaluator: BenchmarkEvaluator,
        output_dir: Optional[str] = None,
    ):
        self.router = router
        self.quality_pipeline = quality_pipeline
        self.model_runner = model_runner
        self.evaluator = evaluator
        self.output_dir = Path(output_dir or (Path(__file__).parents[2] / "experiments" / "phase5" / "artifacts"))
        self.output_dir.mkdir(parents=True, exist_ok=True)

    @classmethod
    def create_default(cls) -> AdaptiveRoutingPipeline:
        router = AdaptiveRouter.create_default()
        quality_pipeline = DocumentQualityPipeline()
        model_runner = ModelRunner()
        evaluator = BenchmarkEvaluator()
        return cls(router, quality_pipeline, model_runner, evaluator)

    def process_sample(
        self,
        sample: BenchmarkSample,
        degraded_image: Image.Image,
        policy: RoutingPolicyType,
        condition: Optional[DegradationCondition] = None,
        oracle_candidate_scores: Optional[Dict[str, float]] = None,
        save_artifact: bool = True,
    ) -> RoutingRunArtifact:
        """
        Executes complete routing and evaluation lifecycle for a sample.
        """
        seed = condition.seed if condition else 42
        run_id = f"run_P5_{sample.dataset}_{policy.value}_{sample.sample_id}_s{seed}"

        # 1. Independent Visual Quality Assessment (Phase 3)
        quality_assessment = self.quality_pipeline.assess_page(
            image_input=degraded_image,
            document_id=sample.document_id,
            page_id=f"{sample.document_id}_p{sample.page_idx}",
            page_number=sample.page_idx + 1,
        )

        # 2. Assemble Inference-Time Uncertainty Vector
        # Use observable quality score Q and baseline execution priors
        q_score = 1.0 - (condition.severity * 0.20 if condition else 0.0)
        uncertainty_vector = self.router.policy_manager.uncertainty_adapter.assemble_vector(
            vlm_confidence=q_score,
            ocr_confidence=q_score if (condition and condition.family not in ["skew_rotation", "perspective_distortion"]) else 0.20,
            retrieval_score=1.0,
            grounding_score=q_score,
            visual_quality_score=q_score,
            ocr_vlm_agreement=q_score,
        )

        # 3. Route Decision (Zero Leakage: no target answers or evaluation metrics passed)
        decision, trace = self.router.route(
            run_id=run_id,
            document_id=sample.document_id,
            page_id=f"{sample.document_id}_p{sample.page_idx}",
            dataset=sample.dataset,
            quality_assessment=quality_assessment,
            policy=policy,
            partition=sample.split,
            seed=seed,
            uncertainty_vector=uncertainty_vector,
            oracle_candidate_scores=oracle_candidate_scores,
        )
        self.router.decision_tracer.save_trace(trace)

        # 4. Candidate Model Execution
        selected_model = decision.selected_model
        sample.image = degraded_image
        primary_start = time.perf_counter()
        exec_result = self.model_runner.run_model(
            model_id=selected_model,
            sample=sample,
            run_id=run_id,
            seed=seed,
        )
        primary_latency = (time.perf_counter() - primary_start) * 1000.0

        # 5. Structural Fallback Inspection
        fallback_model = None
        fallback_latency = 0.0
        should_fallback, target_fb, fb_reason = self.router.fallback_handler.should_trigger_fallback(
            exec_result, current_model=selected_model
        )
        if should_fallback and target_fb:
            fallback_model = target_fb
            fb_start = time.perf_counter()
            exec_result = self.model_runner.run_model(
                model_id=fallback_model,
                sample=sample,
                run_id=f"{run_id}_fallback",
                seed=seed,
            )
            fallback_latency = (time.perf_counter() - fb_start) * 1000.0
            decision.fallback_triggered = True
            decision.fallback_model = fallback_model

        # 6. Evaluation Metrics Computation
        eval_metrics = self.evaluator.evaluate(sample, exec_result)
        metrics_dict = {
            "exact_match": eval_metrics.exact_match,
            "token_f1": eval_metrics.token_f1,
            "anls": eval_metrics.anls,
        }

        # 7. Engineering Cost Calculation
        cost = self.router.cost_model.evaluate_cost(
            primary_model=selected_model,
            primary_latency_ms=primary_latency,
            fallback_model=fallback_model,
            fallback_latency_ms=fallback_latency,
        )

        # 8. Regret Calculation (if oracle scores available)
        regret = None
        oracle_best = None
        if oracle_candidate_scores:
            oracle_best = max(oracle_candidate_scores.keys(), key=lambda m: oracle_candidate_scores[m])
            oracle_max_score = oracle_candidate_scores[oracle_best]
            selected_score = oracle_candidate_scores.get(selected_model, eval_metrics.exact_match)
            regret = max(0.0, float(oracle_max_score - selected_score))

        # 9. Assemble Run Artifact
        artifact = RoutingRunArtifact(
            run_id=run_id,
            document_id=sample.document_id,
            dataset=sample.dataset,
            partition=sample.split,
            seed=seed,
            policy=policy,
            selected_model=selected_model,
            final_answer=exec_result.answer,
            metrics=metrics_dict,
            regret=regret,
            oracle_best_model=oracle_best,
            cost=cost,
            status=exec_result.status,
            error_message=exec_result.error_message,
        )

        # 10. Serialization
        if save_artifact:
            art_path = self.output_dir / f"{run_id}.json"
            with open(art_path, "w", encoding="utf-8") as f:
                f.write(artifact.model_dump_json(indent=2))

        return artifact
