"""
Unit tests for Phase 7 Grounding Classifier and Decision State Machine.
"""

from src.evidence.schema import EvidenceUnit
from src.evidence.grounding_classifier import GroundingClassifier


def test_grounding_classifier_supported():
    classifier = GroundingClassifier()
    units = [
        EvidenceUnit(
            evidence_id="ev_01",
            document_id="doc_inv",
            page_id=1,
            region_id="reg_total",
            bbox_1000=(100, 100, 300, 300),
            text="Invoice Total Amount: $1,450.00",
            provenance_hash="h1"
        )
    ]
    gt_bboxes = [(100, 100, 300, 300)]

    g_res, s_res = classifier.classify_grounding(
        query_text="What is the invoice total amount?",
        answer_text="$1,450.00",
        evidence_units=units,
        ground_truth_bboxes=gt_bboxes
    )

    assert g_res.grounding_status == "GROUNDED"
    assert g_res.answer_support_status == "SUPPORTED"
    assert g_res.spatial_grounding_status == "PASS"
    assert s_res.support_status == "SUPPORTED"
    assert s_res.spatial_score == 1.0


def test_grounding_classifier_insufficient_evidence():
    classifier = GroundingClassifier()
    g_res, s_res = classifier.classify_grounding(
        query_text="What is the total amount?",
        answer_text="$1,450.00",
        evidence_units=[]
    )
    assert g_res.grounding_status == "UNSUPPORTED"
    assert g_res.answer_support_status == "INSUFFICIENT_EVIDENCE"
    assert s_res.support_status == "INSUFFICIENT_EVIDENCE"


def test_grounding_classifier_spatial_failure():
    classifier = GroundingClassifier()
    units = [
        EvidenceUnit(
            evidence_id="ev_01",
            document_id="doc_inv",
            page_id=1,
            region_id="reg_total",
            bbox_1000=(100, 100, 200, 200),
            text="Invoice Total Amount: $1,450.00",
            provenance_hash="h1"
        )
    ]
    # Ground truth box is located far away on page
    gt_bboxes = [(700, 700, 900, 900)]

    g_res, s_res = classifier.classify_grounding(
        query_text="What is the invoice total amount?",
        answer_text="$1,450.00",
        evidence_units=units,
        ground_truth_bboxes=gt_bboxes
    )

    assert g_res.grounding_status == "UNSUPPORTED"
    assert g_res.answer_support_status == "NOT_SUPPORTED"
    assert g_res.spatial_grounding_status == "FAIL"


def test_grounding_classifier_numeric_failure():
    classifier = GroundingClassifier()
    units = [
        EvidenceUnit(
            evidence_id="ev_01",
            document_id="doc_inv",
            page_id=1,
            region_id="reg_total",
            bbox_1000=(100, 100, 300, 300),
            text="Invoice Total Amount: $145.00",
            provenance_hash="h1"
        )
    ]

    g_res, s_res = classifier.classify_grounding(
        query_text="What is the invoice total amount?",
        answer_text="$1,450.00",  # Claiming $1450 when text says $145
        evidence_units=units
    )

    assert g_res.grounding_status == "UNSUPPORTED"
    assert g_res.answer_support_status == "NOT_SUPPORTED"
