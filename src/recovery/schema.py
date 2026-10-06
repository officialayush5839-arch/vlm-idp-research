"""src/recovery/schema.py
Data structures and Enums for Phase 10.5 Safety-Preserving Recovery Subsystem.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Any, List, Optional


class RecoveryState(str, Enum):
    """6-state Recovery Taxonomy."""
    R0_SAFE_COMPLETE = "SAFE_COMPLETE"
    R1_SAFE_PARTIAL = "SAFE_PARTIAL"
    R2_RECOVERABLE_WITH_RESTORATION = "RECOVERABLE_WITH_RESTORATION"
    R3_HUMAN_ESCALATION = "HUMAN_ESCALATION"
    R4_UNSAFE_TO_ANSWER = "UNSAFE_TO_ANSWER"
    R5_IRRECOVERABLE = "IRRECOVERABLE"


class RecoveryAction(str, Enum):
    """Actions performed by the recovery subsystem."""
    EMIT_COMPLETE = "EMIT_COMPLETE"
    EMIT_PARTIAL = "EMIT_PARTIAL"
    RESTORE_AND_RETRY = "RESTORE_AND_RETRY"
    ESCALATE_TO_HUMAN = "ESCALATE_TO_HUMAN"
    ABSTAIN_UNSAFE = "ABSTAIN_UNSAFE"
    REJECT_IRRECOVERABLE = "REJECT_IRRECOVERABLE"


@dataclass
class InspectionRegion:
    """Bounding box region flagged for prioritized human review."""
    page_id: int
    bbox: List[float]  # [ymin, xmin, ymax, xmax] normalized
    defect_type: str
    uncertainty_score: float
    description: str


@dataclass
class PartialEvidenceResult:
    """Represents a partial answer grounded in verified evidence."""
    complete_candidate: str
    extracted_subspan: str
    is_partial: bool
    grounding_score: float
    verified_citation_ids: List[str] = field(default_factory=list)


@dataclass
class RecoveryDecision:
    """Subsystem output containing decision, state, and verified artifacts."""
    state: RecoveryState
    action: RecoveryAction
    confidence: float
    uncertainty_norm: float
    answer_text: Optional[str]
    is_useful: bool
    is_safe: bool
    inspection_regions: List[InspectionRegion] = field(default_factory=list)
    recovery_strategy: str = "none"
    operating_point: str = "balanced"
    reason: str = ""
