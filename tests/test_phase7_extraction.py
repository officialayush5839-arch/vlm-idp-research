"""
Unit tests for Phase 7 Evidence Extraction from upstream packages.
"""

from src.evidence.extractor import EvidenceExtractor
from src.evidence.schema import EvidenceUnit


def test_evidence_extractor_from_phase6_regions():
    extractor = EvidenceExtractor()
    selected_regions = [
        {
            "region_id": "reg_header",
            "page_number": 2,
            "bbox": (50, 50, 950, 150),
            "text_content": "Invoice Summary and Total Balance",
            "score": 0.88,
            "source_type": "text"
        },
        {
            "region_id": "reg_table_total",
            "page_number": 2,
            "bbox": (500, 700, 900, 850),
            "text_content": "Total: $1,450.00",
            "score": 0.95,
            "source_type": "table"
        }
    ]
    selected_pages = [
        {"page_number": 2, "score": 0.92, "clean_text": "Full page text"}
    ]

    units = extractor.extract_from_phase6_package(
        package_id="pkg_test_001",
        document_id="doc_financial_42",
        selected_pages=selected_pages,
        selected_regions=selected_regions,
        page_dimensions={2: (1000, 1000)}
    )

    assert len(units) == 2
    assert isinstance(units[0], EvidenceUnit)
    assert units[0].page_id == 2
    assert units[0].region_id == "reg_header"
    assert units[0].bbox_1000 == (50, 50, 950, 150)
    assert units[0].bbox_pixel == (50, 50, 950, 150)
    assert units[0].provenance_hash != ""
    assert units[1].region_id == "reg_table_total"
    assert units[1].source_type == "table"


def test_evidence_extractor_coarse_page_fallback():
    extractor = EvidenceExtractor()
    selected_pages = [
        {"page_number": 1, "score": 0.75, "raw_text": "Front page of report"},
        {"page_number": 5, "score": 0.82, "raw_text": "Appendix results table"}
    ]

    units = extractor.extract_from_phase6_package(
        package_id="pkg_test_002",
        document_id="doc_report_10",
        selected_pages=selected_pages,
        selected_regions=[]
    )

    assert len(units) == 2
    assert units[0].page_id == 1
    assert units[0].region_id == "page_full_1"
    assert units[0].bbox_1000 == (0, 0, 1000, 1000)
    assert units[1].page_id == 5
