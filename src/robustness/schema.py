"""src/robustness/schema.py
Schemas and dataclasses for Phase 10 Robustness, Cross-Domain Generalization & Distribution-Shift Evaluation.
"""

from dataclasses import dataclass, asdict
from enum import Enum
from typing import Dict, Any, List, Optional


class DomainID(str, Enum):
    D0_IN_DOMAIN = "D0_in_domain"
    D1_LAYOUT_SHIFT = "D1_layout_shift"
    D2_VISUAL_STYLE_SHIFT = "D2_visual_style_shift"
    D3_STRUCTURE_SHIFT = "D3_structure_shift"
    D4_COMBINED_SHIFT = "D4_combined_shift"


@dataclass
class ObservableDistributionProfile:
    """Observable structural and visual characteristics of a document distribution."""
    domain_id: DomainID
    mean_page_count: float
    mean_token_count: float
    mean_text_density: float
    mean_region_density: float
    mean_table_count: float
    mean_whitespace_ratio: float
    mean_visual_quality: float

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["domain_id"] = self.domain_id.value
        return d


@dataclass
class DistributionShiftMetrics:
    """Quantitative divergence between a shifted domain and reference validation profile."""
    domain_id: DomainID
    standardized_mean_diff: float
    wasserstein_distance: float
    population_stability_index: float
    shift_classification: str  # "STABLE" | "MODERATE_SHIFT" | "SIGNIFICANT_SHIFT"


@dataclass
class RobustnessEvaluationResult:
    """Domain-stratified robustness evaluation metrics."""
    domain_id: DomainID
    baseline_id: str
    seed: int
    coverage: float
    selective_accuracy: float
    selective_unsupported_rate: float
    aurc: float
    abstention_f1: float
    robustness_gap: float
    relative_degradation: float
