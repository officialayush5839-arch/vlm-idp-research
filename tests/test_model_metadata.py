"""Unit Tests for Model Metadata Freeze and Attributes."""

from src.vlm.schema import ModelMetadata
from src.vlm.loader import VLMLoader


def test_model_metadata_defaults():
    """Verify default model metadata parameters match frozen protocol."""
    loader = VLMLoader()
    meta = loader.metadata

    assert meta.model_name == "Qwen2.5-VL-7B-Instruct"
    assert meta.huggingface_repo == "Qwen/Qwen2.5-VL-7B-Instruct"
    assert len(meta.revision) == 40
    assert meta.parameter_count == "7.61B"
    assert meta.license_name == "Apache-2.0"
