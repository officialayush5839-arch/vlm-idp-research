"""
Page Index Container and Serializer for Long Documents.
Stores document page records, indexes, and allows serialization to disk.
"""

import json
import os
from typing import List, Dict, Optional
from src.retrieval.schema import DocumentPageRecord


class PageIndex:
    """
    In-memory and file-backed container for document page records.
    """
    def __init__(self, document_id: str):
        self.document_id = document_id
        self.pages: Dict[int, DocumentPageRecord] = {}

    def add_page(self, page: DocumentPageRecord) -> None:
        """
        Add or replace a page record.
        """
        self.pages[page.page_number] = page

    def get_pages(self) -> List[DocumentPageRecord]:
        """
        Return list of pages sorted by page number.
        """
        return [self.pages[p] for p in sorted(self.pages.keys())]

    def total_pages(self) -> int:
        """
        Total number of indexed pages.
        """
        return len(self.pages)

    def save(self, filepath: str) -> None:
        """
        Save all page records to a JSON file.
        """
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        data = {
            "document_id": self.document_id,
            "pages": [p.model_dump() for p in self.get_pages()]
        }
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    @classmethod
    def load(cls, filepath: str) -> "PageIndex":
        """
        Load page index from JSON file.
        """
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        idx = cls(document_id=data["document_id"])
        for p_dict in data["pages"]:
            idx.add_page(DocumentPageRecord(**p_dict))
        return idx
