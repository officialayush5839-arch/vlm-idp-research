"""Unit tests verifying Zero Data and Label Leakage for Phase 3 Quality Pipeline."""

import inspect
from src.quality.pipeline import DocumentQualityPipeline
from src.quality.synthetic import create_clean_document_fixture


def test_no_leakage_interface_signature():
    """Verify that assess_page signature does NOT accept degradation labels or model results."""
    sig = inspect.signature(DocumentQualityPipeline.assess_page)
    param_names = list(sig.parameters.keys())

    forbidden_params = [
        "degradation",
        "degradation_label",
        "ground_truth",
        "ocr",
        "ocr_result",
        "vlm",
        "vlm_result",
        "split",
        "partition",
        "severity",
    ]
    for param in forbidden_params:
        assert param not in param_names, f"Leakage violation: forbidden parameter '{param}' found in assess_page"


def test_no_leakage_independent_assessment():
    """Verify that identical visual content produces identical quality assessment regardless of document_id or context."""
    pipeline = DocumentQualityPipeline()
    img = create_clean_document_fixture()

    res_clean_meta = pipeline.assess_page(img, document_id="doc_clean", page_id="p1")
    res_spoofed_meta = pipeline.assess_page(img, document_id="doc_claim_severe_degradation", page_id="p99")

    # Feature extractions must be identical
    for k in res_clean_meta.features.keys():
        assert (
            res_clean_meta.features[k].raw_value == res_spoofed_meta.features[k].raw_value
        ), f"Feature {k} altered by metadata spoofing"
        assert (
            res_clean_meta.features[k].severity == res_spoofed_meta.features[k].severity
        ), f"Severity {k} altered by metadata spoofing"
