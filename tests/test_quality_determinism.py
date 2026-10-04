"""Unit tests verifying determinism and repeatability of Phase 3 Quality Pipeline."""

from src.quality.pipeline import DocumentQualityPipeline
from src.quality.synthetic import apply_degradation, create_clean_document_fixture


def test_quality_determinism():
    pipeline = DocumentQualityPipeline()
    clean_img = create_clean_document_fixture()

    # Test clean determinism
    res1 = pipeline.assess_page(clean_img, "doc_det_1", "p1")
    res2 = pipeline.assess_page(clean_img, "doc_det_1", "p1")

    for k in res1.features.keys():
        f1 = res1.features[k]
        f2 = res2.features[k]
        assert f1.raw_value == f2.raw_value, f"Discrepancy in feature {k}"
        assert f1.severity == f2.severity, f"Discrepancy in severity {k}"
        assert f1.status == f2.status, f"Discrepancy in status {k}"

    assert len(res1.detected_degradations) == len(res2.detected_degradations)


def test_quality_determinism_degraded():
    pipeline = DocumentQualityPipeline()
    clean_img = create_clean_document_fixture()
    noisy_img = apply_degradation(clean_img, "gaussian_noise", 2, seed=123)

    res1 = pipeline.assess_page(noisy_img, "doc_det_2", "p1")
    res2 = pipeline.assess_page(noisy_img, "doc_det_2", "p1")

    for k in res1.features.keys():
        assert res1.features[k].raw_value == res2.features[k].raw_value
        assert res1.features[k].severity == res2.features[k].severity
