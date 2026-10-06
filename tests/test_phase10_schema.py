"""Unit tests for Phase 10 schemas, domain registry, and distribution profiling."""

import pytest
from src.robustness.schema import (
    DomainID,
    ObservableDistributionProfile,
    DistributionShiftMetrics,
    RobustnessEvaluationResult,
)
from src.robustness.domain_registry import DomainRegistry
from src.robustness.distribution_profile import DistributionProfiler
from src.robustness.shift_detector import ShiftDetector


def test_domain_registry_loading():
    registry = DomainRegistry()
    domains = registry.list_domains()
    assert len(domains) == 5
    assert DomainID.D0_IN_DOMAIN in domains
    assert DomainID.D4_COMBINED_SHIFT in domains

    doc_dom = registry.get_domain_for_doc("doc_mp_026")
    assert doc_dom == DomainID.D0_IN_DOMAIN


def test_distribution_profiler_and_shift_detector():
    doc_indices = [
        {
            "pages": [
                {"raw_text": "sample text with words", "regions": [1, 2], "quality_score": 0.9},
                {"raw_text": "more words on page two", "regions": [3, 4], "quality_score": 0.85},
            ]
        }
    ]

    profile_d0 = DistributionProfiler.profile_documents(DomainID.D0_IN_DOMAIN, doc_indices)
    assert profile_d0.mean_page_count == 2.0
    assert profile_d0.mean_visual_quality == 0.875

    # Degraded target profile
    target_profile = ObservableDistributionProfile(
        domain_id=DomainID.D2_VISUAL_STYLE_SHIFT,
        mean_page_count=2.0,
        mean_token_count=10.0,
        mean_text_density=0.01,
        mean_region_density=2.0,
        mean_table_count=0.3,
        mean_whitespace_ratio=0.99,
        mean_visual_quality=0.30,
    )

    shift = ShiftDetector.detect_shift(profile_d0, target_profile)
    assert isinstance(shift, DistributionShiftMetrics)
    assert shift.wasserstein_distance > 0.0
    assert shift.shift_classification in ("MODERATE_SHIFT", "SIGNIFICANT_SHIFT")
