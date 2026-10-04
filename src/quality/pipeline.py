"""
Top-level Document Quality and Degradation Assessment Pipeline.
Orchestrates preprocessing, feature extraction, degradation detection, and multi-page aggregation.
Strictly decoupled from downstream OCR, VLM inference, and adaptive routing decisions.
"""

from __future__ import annotations

import datetime
from pathlib import Path
import time
from typing import Any, Dict, List, Optional, Union
import numpy as np
from PIL import Image

from src.core.logging import get_logger
from src.ingestion.schema import Document
from src.quality.aggregator import aggregate_document_quality
from src.quality.config import QualityConfig, load_phase3_quality_config
from src.quality.detector import detect_degradations
from src.quality.features import extract_all_features
from src.quality.preprocessing import preprocess_image_input
from src.quality.schema import (
    DocumentQualityAssessment,
    FeatureStatus,
    PageQualityAssessment,
    RuntimeBreakdown,
)

logger = get_logger(__name__)


class DocumentQualityPipeline:
    """
    Independent document quality and visual degradation assessment engine.
    Computes deterministic feature vectors without relying on downstream OCR/VLM models.
    """

    def __init__(self, config: Optional[QualityConfig] = None):
        self.config = config or load_phase3_quality_config()
        self.algorithm_version = self.config.algorithm_version
        self.config_hash = self.config.config_hash
        logger.info(
            f"Initialized DocumentQualityPipeline (version={self.algorithm_version}, "
            f"config_hash={self.config_hash})"
        )

    def assess_page(
        self,
        image_input: Union[Image.Image, np.ndarray, str, Path],
        document_id: str,
        page_id: str,
        page_number: int = 1,
    ) -> PageQualityAssessment:
        """
        Assess visual quality and degradations for a single document page image.

        Args:
            image_input: PIL Image, numpy array, or file path
            document_id: Unique document identifier
            page_id: Unique page identifier
            page_number: 1-indexed page sequence number

        Returns:
            PageQualityAssessment schema instance
        """
        t0 = time.perf_counter()
        timestamp_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()

        # 1. Preprocessing
        t_pre_start = time.perf_counter()
        max_dim = self.config.preprocessing.get("max_dimension", 2048)
        preprocessed = preprocess_image_input(image_input, max_dimension=max_dim)
        t_pre_ms = (time.perf_counter() - t_pre_start) * 1000.0

        # 2. Feature Extraction
        features, t_feat_ms = extract_all_features(preprocessed, self.config)

        # 3. Degradation Detection
        detections, t_det_ms = detect_degradations(features, self.config)

        total_elapsed_ms = (time.perf_counter() - t0) * 1000.0

        # Determine overall execution status
        failed_features = [f for f, r in features.items() if r.status == FeatureStatus.FAILED]
        if not failed_features:
            exec_status = "SUCCESS"
        elif len(failed_features) < len(features):
            exec_status = "PARTIAL_SUCCESS"
        else:
            exec_status = "FAILED"

        runtime = RuntimeBreakdown(
            preprocessing_ms=round(t_pre_ms, 2),
            feature_extraction_ms=round(t_feat_ms, 2),
            detection_ms=round(t_det_ms, 2),
            aggregation_ms=0.0,
            total_latency_ms=round(total_elapsed_ms, 2),
            memory_mb=None,  # Measured and logged separately where available
        )

        return PageQualityAssessment(
            document_id=document_id,
            page_id=page_id,
            page_number=page_number,
            width=preprocessed.width,
            height=preprocessed.height,
            features=features,
            detected_degradations=detections,
            overall_quality_score=None,  # NOT_DEFINED per Phase 0 Protocol Section 13
            overall_quality_status="NOT_DEFINED",
            runtime=runtime,
            algorithm_version=self.algorithm_version,
            config_hash=self.config_hash,
            timestamp_utc=timestamp_utc,
            status=exec_status,
        )

    def assess_document(self, document: Document) -> DocumentQualityAssessment:
        """
        Assess quality across all pages of an ingested Document object.

        Args:
            document: Document model from src.ingestion.schema

        Returns:
            DocumentQualityAssessment schema instance
        """
        timestamp_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
        page_results: List[PageQualityAssessment] = []

        for page in document.pages:
            res = self.assess_page(
                image_input=page.image_path,
                document_id=document.document_id,
                page_id=page.page_id,
                page_number=page.page_number,
            )
            page_results.append(res)

        return aggregate_document_quality(
            document_id=document.document_id,
            pages=page_results,
            algorithm_version=self.algorithm_version,
            config_hash=self.config_hash,
            timestamp_utc=timestamp_utc,
        )
