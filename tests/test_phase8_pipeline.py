import pytest
from src.uncertainty.schema import UncertaintyPackage
from src.uncertainty.pipeline import UncertaintyPipeline


def test_uncertainty_pipeline_uncalibrated():
    pipeline = UncertaintyPipeline(method="uncalibrated")
    pkg = pipeline.process(
        document_id="doc_test_1",
        query_id="q_1",
        model_output={"confidence": 0.85},
        retrieval_metadata={"retrieval_margin": 0.5, "retrieval_entropy": 0.2},
        grounding_result={
            "semantic_support_score": 0.8,
            "entity_coverage": 0.9,
            "is_valid_box": True,
            "sufficiency_status": "SUFFICIENT",
            "grounding_status": "GROUNDED",
            "citation_count": 2
        },
        quality_metadata={"overall_quality": 0.85, "blur": 0.1, "noise": 0.1, "skew": 0.0, "contrast": 0.9, "resolution": 0.9}
    )

    assert isinstance(pkg, UncertaintyPackage)
    assert pkg.raw_confidence == 0.85
    assert pkg.calibrated_confidence == 0.85
    assert pkg.decision.decision == "ANSWER"
    assert len(pkg.package_hash) == 64
