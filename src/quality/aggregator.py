"""
Document-Level Quality Aggregator.
Computes descriptive multi-page summary statistics while preserving individual page fidelity.
"""

from __future__ import annotations

import time
from typing import Any, Dict, List, Tuple
import numpy as np

from src.quality.schema import DocumentQualityAssessment, PageQualityAssessment


def aggregate_document_quality(
    document_id: str,
    pages: List[PageQualityAssessment],
    algorithm_version: str,
    config_hash: str,
    timestamp_utc: str,
) -> DocumentQualityAssessment:
    """
    Aggregates page-level quality assessments into a DocumentQualityAssessment artifact.
    Identifies the worst page and computes descriptive distribution statistics.

    Args:
        document_id: Document identifier
        pages: List of PageQualityAssessment objects
        algorithm_version: Active algorithm version string
        config_hash: Cryptographic configuration hash
        timestamp_utc: Execution timestamp string

    Returns:
        DocumentQualityAssessment object
    """
    if not pages:
        raise ValueError(f"Cannot aggregate quality for document {document_id} with 0 pages.")

    worst_page_id = None
    worst_page_num = None
    highest_sev = 0
    highest_family = None

    # Collect per-feature values across pages
    feature_values: Dict[str, List[float]] = {}

    for page in pages:
        # Check detected degradations for highest severity
        for deg in page.detected_degradations:
            if deg.severity > highest_sev:
                highest_sev = deg.severity
                highest_family = deg.family
                worst_page_id = page.page_id
                worst_page_num = page.page_number

        for feat_name, feat_res in page.features.items():
            if feat_res.normalized_value is not None:
                if feat_name not in feature_values:
                    feature_values[feat_name] = []
                feature_values[feat_name].append(feat_res.normalized_value)

    # If no degradations detected across pages, default worst page to first page
    if worst_page_id is None:
        worst_page_id = pages[0].page_id
        worst_page_num = pages[0].page_number

    # Compute descriptive summary statistics
    stats: Dict[str, Any] = {}
    for feat_name, vals in feature_values.items():
        if vals:
            stats[feat_name] = {
                "mean": round(float(np.mean(vals)), 4),
                "median": round(float(np.median(vals)), 4),
                "min": round(float(np.min(vals)), 4),
                "max": round(float(np.max(vals)), 4),
                "std": round(float(np.std(vals)), 4),
            }

    overall_status = "SUCCESS" if all(p.status == "SUCCESS" for p in pages) else "PARTIAL_SUCCESS"

    return DocumentQualityAssessment(
        document_id=document_id,
        page_count=len(pages),
        pages=pages,
        summary_statistics=stats,
        worst_page_id=worst_page_id,
        worst_page_number=worst_page_num,
        highest_severity_detected=highest_sev,
        highest_severity_family=highest_family,
        algorithm_version=algorithm_version,
        config_hash=config_hash,
        timestamp_utc=timestamp_utc,
        status=overall_status,
    )
