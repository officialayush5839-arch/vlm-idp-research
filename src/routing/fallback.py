"""
Structural Fallback Handler for Phase 5.
Validates candidate model output structure without peeking at semantic ground truth.
Triggers fallback invocation upon schema or execution failure.
"""

from __future__ import annotations

from typing import Optional, Tuple
from src.benchmark.schema import ModelExecutionResult


class StructuralFallbackHandler:
    """
    Evaluates whether a model output adheres to required structural contracts
    (non-empty string, valid execution status, bounded coordinates).
    """

    def __init__(self, fallback_target: str = "B2", enabled: bool = True):
        self.fallback_target = fallback_target
        self.enabled = enabled

    def validate_output(self, result: ModelExecutionResult) -> Tuple[bool, str]:
        """
        Structural inspection of model execution outcome.
        Returns: (is_valid: bool, reason: str)
        """
        # 1. Execution status check
        if result.status == "FAILED":
            err_type = result.error_type or "UnknownError"
            return False, f"Model execution status is FAILED ({err_type})"

        # 2. Non-empty string check
        if not result.answer or not result.answer.strip():
            return False, "Model returned an empty or whitespace-only answer"

        # 3. Bounding box validity check (if coordinates returned)
        for bbox in result.predicted_bboxes:
            if len(bbox) != 4:
                return False, f"Malformed bounding box with {len(bbox)} elements (expected 4)"
            x1, y1, x2, y2 = bbox
            if not (0 <= x1 <= 1000 and 0 <= y1 <= 1000 and 0 <= x2 <= 1000 and 0 <= y2 <= 1000):
                return False, f"Bounding box coordinates out of bounds: [{x1}, {y1}, {x2}, {y2}]"
            if x1 > x2 or y1 > y2:
                return False, f"Inverted bounding box coordinates: [{x1}, {y1}, {x2}, {y2}]"

        return True, "Output structure valid"

    def should_trigger_fallback(self, result: ModelExecutionResult, current_model: str) -> Tuple[bool, Optional[str], str]:
        """
        Determines whether fallback execution should be invoked.
        Returns: (should_fallback: bool, fallback_model: Optional[str], reason: str)
        """
        if not self.enabled:
            return False, None, "Fallback mechanism disabled by configuration"

        if current_model == self.fallback_target:
            return False, None, f"Already executing fallback target {self.fallback_target}; cannot recurse"

        is_valid, reason = self.validate_output(result)
        if not is_valid:
            return True, self.fallback_target, f"Structural validation failure ({reason}); falling back to {self.fallback_target}"

        return False, None, "Output structure valid"
