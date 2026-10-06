"""src/reliability/failure_modes.py
Failure mode diagnostic classifier adhering to the 8-class failure taxonomy:
- F01: RETRIEVAL_FAILURE
- F02: VISUAL_DEGRADATION
- F03: INSUFFICIENT_EVIDENCE
- F04: NUMERIC_CONFLICT
- F05: TABLE_ALIGNMENT_FAILURE
- F06: SPATIAL_GROUNDING_FAILURE
- F07: CROSS_PAGE_CONFLICT
- F08: MODEL_DISAGREEMENT
"""

from typing import Optional, Dict, Any, List, Tuple
from src.reliability.schema import FailureMode, FailureModeResult, UncertaintyVector


class FailureModeClassifier:
    """Diagnoses primary and secondary failure modes from the 8D uncertainty vector."""

    def diagnose(
        self,
        uncertainty_vector: UncertaintyVector,
        confidence: float,
        context_metadata: Optional[Dict[str, Any]] = None,
    ) -> FailureModeResult:
        u_arr = uncertainty_vector.to_array()
        
        # Map indices to FailureMode
        mode_mapping: List[Tuple[FailureMode, float]] = [
            (FailureMode.F01_RETRIEVAL_FAILURE, uncertainty_vector.u_retrieval),
            (FailureMode.F07_CROSS_PAGE_CONFLICT, uncertainty_vector.u_semantic),  # proxy
            (FailureMode.F06_SPATIAL_GROUNDING_FAILURE, uncertainty_vector.u_spatial),
            (FailureMode.F04_NUMERIC_CONFLICT, uncertainty_vector.u_numeric),
            (FailureMode.F05_TABLE_ALIGNMENT_FAILURE, uncertainty_vector.u_table),
            (FailureMode.F03_INSUFFICIENT_EVIDENCE, uncertainty_vector.u_sufficiency),
            (FailureMode.F02_VISUAL_DEGRADATION, uncertainty_vector.u_quality),
            (FailureMode.F08_MODEL_DISAGREEMENT, uncertainty_vector.u_agreement),
        ]

        # Sort modes by uncertainty descending
        sorted_modes = sorted(mode_mapping, key=lambda x: x[1], reverse=True)

        primary_mode = None
        secondary_mode = None

        # A mode is flagged if uncertainty exceeds 0.40
        if sorted_modes[0][1] >= 0.40:
            primary_mode = sorted_modes[0][0]
        if len(sorted_modes) > 1 and sorted_modes[1][1] >= 0.35:
            secondary_mode = sorted_modes[1][0]

        deficit = max(0.0, 1.0 - confidence)

        diagnostics = {
            "top_signals": [(m.value, round(score, 4)) for m, score in sorted_modes[:3]],
            "uncertainty_l2": uncertainty_vector.l2_norm,
        }

        return FailureModeResult(
            primary_failure=primary_mode,
            secondary_failure=secondary_mode,
            confidence_deficit=deficit,
            diagnostics=diagnostics,
        )
