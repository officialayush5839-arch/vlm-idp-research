"""
Tests for Phase 5 Structural Fallback Handler.
Verifies fallback on malformed/empty model outputs without peeking at semantic ground truth.
"""

import pytest
from src.benchmark.schema import ModelExecutionResult
from src.routing.fallback import StructuralFallbackHandler


def test_structural_fallback_valid_output():
    handler = StructuralFallbackHandler(fallback_target="B2", enabled=True)
    res = ModelExecutionResult(
        model_id="B0",
        model_name="PaddleOCR",
        revision_sha="abc1234",
        answer="Valid Extracted Invoice Text",
        status="SUCCESS",
    )
    is_valid, reason = handler.validate_output(res)
    assert is_valid is True
    assert reason == "Output structure valid"


def test_structural_fallback_detects_empty_answer():
    handler = StructuralFallbackHandler(fallback_target="B2", enabled=True)
    res = ModelExecutionResult(
        model_id="B0",
        model_name="PaddleOCR",
        revision_sha="abc1234",
        answer="",  # Malformed empty answer
        status="SUCCESS",
    )
    is_valid, reason = handler.validate_output(res)
    assert is_valid is False
    assert "empty" in reason.lower()


def test_structural_fallback_detects_failure_status():
    handler = StructuralFallbackHandler(fallback_target="B2", enabled=True)
    res = ModelExecutionResult(
        model_id="B1",
        model_name="OCR+VLM",
        revision_sha="abc1234",
        answer="Partial",
        status="FAILED",
        error_type="OOMError",
        error_message="CUDA out of memory",
    )
    is_valid, reason = handler.validate_output(res)
    assert is_valid is False
    assert "status is failed" in reason.lower()


def test_structural_fallback_detects_out_of_bounds_bboxes():
    handler = StructuralFallbackHandler(fallback_target="B2", enabled=True)
    res = ModelExecutionResult(
        model_id="B0-U",
        model_name="Unlimited-OCR",
        revision_sha="abc1234",
        answer="Extracted text",
        predicted_bboxes=[[0, 0, 1200, 500]],  # 1200 > 1000
        status="SUCCESS",
    )
    is_valid, reason = handler.validate_output(res)
    assert is_valid is False
    assert "bounding box coordinate" in reason.lower()
