"""src/safety_recovery/schema.py
Data structures and Enums for Phase 11 Safety-Constrained Recovery Architecture.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Any, List, Optional


class Phase11State(str, Enum):
    """Phase 11 6-state Operational Taxonomy."""
    S11_0_SAFE_RECOVERED = "SAFE_RECOVERED"
    S11_1_SAFE_PARTIAL = "SAFE_PARTIAL"
    S11_2_RECOVERY_WITH_RESTORATION = "RECOVERY_WITH_RESTORATION"
    S11_3_HUMAN_REVIEW_REQUIRED = "HUMAN_REVIEW_REQUIRED"
    S11_4_ABSTAIN = "ABSTAIN"
    S11_5_UNSAFE_RECOVERY_REJECTED = "UNSAFE_RECOVERY_REJECTED"


class Phase11Action(str, Enum):
    """Phase 11 Output Actions."""
    EMIT_COMPLETE = "EMIT_COMPLETE"
    EMIT_PARTIAL = "EMIT_PARTIAL"
    ESCALATE_TO_HUMAN = "ESCALATE_TO_HUMAN"
    ABSTAIN_DEFENSIVE = "ABSTAIN_DEFENSIVE"
    REJECT_UNSAFE = "REJECT_UNSAFE"


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


@dataclass
class HumanReviewPackage:
    """Human-in-the-loop escalation payload with precise inspection bounding boxes."""
    document_id: str
    page_id: int
    query_id: str
    candidate_answer: Optional[str]
    evidence_regions: List[List[float]]  # [[ymin, xmin, ymax, xmax], ...]
    confidence: float
    uncertainty_norm: float
    risk_level: RiskLevel
    failure_reason: str
    suggested_action: str
    citations: List[str] = field(default_factory=list)


@dataclass
class SafetyRecoveryDecision:
    """Master output structure for Phase 11 decisions."""
    state: Phase11State
    action: Phase11Action
    confidence: float
    uncertainty_norm: float
    answer_text: Optional[str]
    is_useful: bool
    is_safe: bool
    review_package: Optional[HumanReviewPackage] = None
    passed_layers: List[str] = field(default_factory=list)
    failed_layers: List[str] = field(default_factory=list)
    operating_point: str = "safety_constrained_balanced"
    reason: str = ""
    trace_id: str = ""
