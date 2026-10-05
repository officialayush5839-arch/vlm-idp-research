"""
Unit tests for PageIndex persistence and retrieval.
"""

from src.retrieval.page_index import PageIndex
from src.retrieval.schema import DocumentPageRecord, DocumentRegionRecord


def test_page_index_save_and_load(tmp_path):
    doc_id = "doc_persist_123"
    idx = PageIndex(document_id=doc_id)

    p1 = DocumentPageRecord(
        document_id=doc_id,
        page_number=1,
        split="test",
        raw_text="Title page and table of contents",
        regions=[]
    )
    p2 = DocumentPageRecord(
        document_id=doc_id,
        page_number=2,
        split="test",
        raw_text="Operating income and expense reports",
        regions=[
            DocumentRegionRecord(
                region_id="r_inc",
                page_number=2,
                bbox=(100, 200, 800, 600),
                region_type="table",
                text_content="Income statement table"
            )
        ]
    )

    idx.add_page(p1)
    idx.add_page(p2)
    assert idx.total_pages() == 2

    save_file = str(tmp_path / "page_index.json")
    idx.save(save_file)

    loaded = PageIndex.load(save_file)
    assert loaded.document_id == doc_id
    assert loaded.total_pages() == 2

    pages = loaded.get_pages()
    assert pages[0].page_number == 1
    assert pages[1].page_number == 2
    assert len(pages[1].regions) == 1
    assert pages[1].regions[0].region_id == "r_inc"
