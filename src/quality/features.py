"""
Unified Feature Registry and Orchestration Engine.
Coordinates all individual visual feature extractors with strict failure isolation.
"""

from __future__ import annotations

import time
from typing import Any, Dict, Tuple
import numpy as np

from src.core.logging import get_logger
from src.quality.blur import measure_blur
from src.quality.compression import measure_compression
from src.quality.config import QualityConfig
from src.quality.contrast import measure_contrast
from src.quality.glare import measure_glare
from src.quality.illumination import measure_illumination
from src.quality.noise import measure_noise
from src.quality.occlusion import measure_occlusion
from src.quality.perspective import measure_perspective
from src.quality.preprocessing import PreprocessedPage
from src.quality.resolution import measure_resolution
from src.quality.schema import FeatureResult, FeatureStatus
from src.quality.skew import measure_skew

logger = get_logger(__name__)

FEATURE_EXTRACTORS = {
    "blur": measure_blur,
    "noise": measure_noise,
    "skew": measure_skew,
    "glare": measure_glare,
    "contrast": measure_contrast,
    "resolution": measure_resolution,
    "compression": measure_compression,
    "illumination": measure_illumination,
    "occlusion": measure_occlusion,
    "perspective": measure_perspective,
}


def extract_all_features(
    preprocessed: PreprocessedPage,
    config: QualityConfig,
) -> Tuple[Dict[str, FeatureResult], float]:
    """
    Executes all enabled quality feature extractors on the preprocessed page.
    Guarantees failure isolation: an exception in one extractor will mark that feature
    FAILED but allow all other features to complete successfully.

    Args:
        preprocessed: PreprocessedPage container
        config: Loaded QualityConfig

    Returns:
        (features_dict, total_feature_extraction_ms)
    """
    t0 = time.perf_counter()
    features: Dict[str, FeatureResult] = {}

    for name, extractor_fn in FEATURE_EXTRACTORS.items():
        # Check if enabled in config
        flag_info = config.feature_flags.get(name, {})
        if not flag_info.get("enabled", True):
            features[name] = FeatureResult(
                status=FeatureStatus.NOT_AVAILABLE,
                message=f"Feature {name} is disabled in pipeline configuration.",
            )
            continue

        # Get feature-specific params and cutoffs
        spec = config.feature_specs.get(name, {})
        from src.quality.detector import FEATURE_TO_FAMILY
        family_name = FEATURE_TO_FAMILY.get(name, name)
        thresh_info = config.severity_thresholds.get(family_name, config.severity_thresholds.get(name, {}))
        merged_params = {**spec, **thresh_info}

        try:
            res = extractor_fn(preprocessed.gray, merged_params)
            features[name] = res
        except Exception as e:
            logger.warning(f"Feature extractor '{name}' encountered an error: {e}")
            features[name] = FeatureResult(
                status=FeatureStatus.FAILED,
                message=f"Extraction error: {str(e)}",
            )
            if config.fail_fast:
                raise

    elapsed_ms = (time.perf_counter() - t0) * 1000.0
    return features, elapsed_ms
