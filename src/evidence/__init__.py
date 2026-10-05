"""
Phase 7 Evidence Grounding Subsystem.
Provides verification, spatial validation, answer support assessment,
and cryptographic provenance for document intelligence.
"""

from src.evidence.schema import (
    EvidenceUnit,
    EvidenceSupportResult,
    GroundingResult,
    CitationRecord,
    Phase7EvidencePackage,
    GroundingMetricsResult
)
from src.evidence.region_validator import (
    SpatialRegionValidator,
    compute_iou,
    compute_containment,
    clip_bbox_1000,
    is_valid_bbox_1000
)
from src.evidence.semantic_support import SemanticSupportVerifier
from src.evidence.numeric_verifier import NumericVerifier
from src.evidence.table_verifier import TableVerifier
from src.evidence.evidence_sufficiency import EvidenceSufficiencyEvaluator
from src.evidence.multipage_aggregator import MultiPageAggregator
from src.evidence.grounding_classifier import GroundingClassifier
from src.evidence.citation import CitationGenerator
from src.evidence.provenance import (
    compute_sha256,
    generate_phase7_run_id,
    build_provenance_record,
    get_git_commit
)
from src.evidence.extractor import EvidenceExtractor
from src.evidence.baselines import BASELINE_MAP, get_baseline_config
from src.evidence.pipeline import EvidenceGroundingPipeline
from src.evidence.metrics import (
    compute_region_recall_at_iou,
    compute_evidence_precision,
    compute_evidence_f1,
    compute_mean_iou,
    categorize_grounding_failure,
    paired_bootstrap_test
)
from src.evidence.audit import audit_zero_leakage

__all__ = [
    "EvidenceUnit",
    "EvidenceSupportResult",
    "GroundingResult",
    "CitationRecord",
    "Phase7EvidencePackage",
    "GroundingMetricsResult",
    "SpatialRegionValidator",
    "compute_iou",
    "compute_containment",
    "clip_bbox_1000",
    "is_valid_bbox_1000",
    "SemanticSupportVerifier",
    "NumericVerifier",
    "TableVerifier",
    "EvidenceSufficiencyEvaluator",
    "MultiPageAggregator",
    "GroundingClassifier",
    "CitationGenerator",
    "compute_sha256",
    "generate_phase7_run_id",
    "build_provenance_record",
    "get_git_commit",
    "EvidenceExtractor",
    "BASELINE_MAP",
    "get_baseline_config",
    "EvidenceGroundingPipeline",
    "compute_region_recall_at_iou",
    "compute_evidence_precision",
    "compute_evidence_f1",
    "compute_mean_iou",
    "categorize_grounding_failure",
    "paired_bootstrap_test",
    "audit_zero_leakage"
]
