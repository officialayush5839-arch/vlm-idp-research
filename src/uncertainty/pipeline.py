"""
Master Uncertainty and Abstention Pipeline for Phase 8.
Orchestrates signal extraction, feature aggregation, post-hoc calibration,
and selective abstention decision-making into a unified UncertaintyPackage.
"""

import hashlib
import json
from typing import Dict, Any, Optional
from src.uncertainty.schema import UncertaintyFeatures, UncertaintyPackage, AbstentionDecision
from src.uncertainty.calibration import CalibrationManager
from src.uncertainty.abstention import AbstentionPolicy
from src.uncertainty.features import FeatureAggregator
from src.uncertainty.signals import SignalExtractor


class UncertaintyPipeline:
    """
    End-to-end pipeline for evaluating document prediction uncertainty and selective abstention.
    """

    def __init__(
        self,
        method: str = "uncalibrated",
        cal_manager: Optional[CalibrationManager] = None,
        default_threshold: float = 0.5,
        config: Optional[Dict[str, Any]] = None
    ):
        self.method = method
        self.cal_manager = cal_manager or CalibrationManager(method=method, config=config)
        self.policy = AbstentionPolicy(default_threshold=default_threshold)
        self.feature_aggregator = FeatureAggregator(config=config)
        self.signal_extractor = SignalExtractor()

    def process(
        self,
        document_id: str,
        query_id: str,
        model_output: Dict[str, Any],
        retrieval_metadata: Optional[Dict[str, Any]] = None,
        grounding_result: Optional[Dict[str, Any]] = None,
        quality_metadata: Optional[Dict[str, Any]] = None,
        page_count: int = 1,
        threshold: Optional[float] = None,
        target_coverage: float = 1.0,
        provenance: Optional[Dict[str, Any]] = None
    ) -> UncertaintyPackage:
        """
        Process a single prediction query through the uncertainty quantification pipeline.
        """
        model_conf = float(model_output.get("confidence", 1.0))
        ret_scores = (retrieval_metadata or {}).get("page_scores", [])
        reg_scores = (retrieval_metadata or {}).get("region_scores", [])
        r_margin = (retrieval_metadata or {}).get("retrieval_margin")
        r_entropy = (retrieval_metadata or {}).get("retrieval_entropy")

        q_meta = quality_metadata or {}
        overall_q = float(q_meta.get("overall_quality", 1.0))

        features: UncertaintyFeatures = self.signal_extractor.extract_features(
            model_confidence=model_conf,
            page_retrieval_scores=ret_scores,
            region_retrieval_scores=reg_scores,
            phase7_support_result=grounding_result,
            phase7_grounding_result=grounding_result,
            citations_count=int((grounding_result or {}).get("citation_count", 1)),
            quality_features=q_meta,
            overall_quality=overall_q,
            page_count=page_count
        )
        if r_margin is not None:
            features.retrieval_margin = float(r_margin)
        if r_entropy is not None:
            features.retrieval_entropy = float(r_entropy)

        comp_conf = self.feature_aggregator.compute_composite_confidence(features)
        features.composite_raw_confidence = comp_conf

        raw_conf = float(features.model_confidence)
        if self.method == "evidence_aware":
            effective_raw = float(features.composite_raw_confidence)
        else:
            effective_raw = raw_conf

        cal_conf = self.cal_manager.predict(effective_raw)

        decision: AbstentionDecision = self.policy.decide(
            confidence=cal_conf,
            features=features,
            threshold=threshold,
            target_coverage=target_coverage
        )

        prov = provenance or {}
        pkg_id = f"pkg_{document_id}_{query_id}_{self.method}"

        # Cryptographic package hash
        hash_payload = (
            f"{pkg_id}|{document_id}|{query_id}|{raw_conf}|{cal_conf}|"
            f"{decision.decision}|{decision.threshold}|{self.method}"
        )
        pkg_hash = hashlib.sha256(hash_payload.encode("utf-8")).hexdigest()

        return UncertaintyPackage(
            package_id=pkg_id,
            document_id=str(document_id),
            query_id=str(query_id),
            raw_confidence=round(float(raw_conf), 6),
            calibrated_confidence=round(float(cal_conf), 6),
            features=features,
            decision=decision,
            calibration_method=self.method,
            provenance=prov,
            package_hash=pkg_hash
        )
