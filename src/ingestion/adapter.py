"""
Dataset Ingestion Interface and Adapters for the 7 Benchmark Datasets.
Provides standardized accessors without requiring premature dataset downloads.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional
from pydantic import BaseModel

from src.ingestion.schema import Document


class AdapterState(str, Enum):
    """Lifecycle status of a dataset adapter."""
    PLANNED = "PLANNED"
    SCAFFOLDED = "SCAFFOLDED"
    IMPLEMENTED = "IMPLEMENTED"
    VALIDATED = "VALIDATED"
    BLOCKED = "BLOCKED"


class DatasetAdapter(ABC):
    """
    Abstract base interface for all document intelligence dataset adapters.
    """

    def __init__(self, data_root: str | Path, state: AdapterState = AdapterState.SCAFFOLDED):
        self.data_root = Path(data_root)
        self._state = state

    @property
    def state(self) -> AdapterState:
        return self._state

    @property
    @abstractmethod
    def dataset_name(self) -> str:
        """Name of the benchmark dataset."""
        pass

    @abstractmethod
    def list_documents(self, partition: Optional[str] = None) -> List[str]:
        """List all document IDs available in the dataset partition."""
        pass

    @abstractmethod
    def load_document(self, document_id: str) -> Document:
        """Load and return an ingested Document object."""
        pass

    @abstractmethod
    def load_annotations(self, document_id: str) -> List[Dict[str, Any]]:
        """Load question-answering or field-extraction annotations."""
        pass

    @abstractmethod
    def get_metadata(self) -> Dict[str, Any]:
        """Return dataset-level metadata and citation information."""
        pass


class DocVQAAdapter(DatasetAdapter):
    """Adapter for DocVQA benchmark."""
    @property
    def dataset_name(self) -> str:
        return "DocVQA"

    def list_documents(self, partition: Optional[str] = None) -> List[str]:
        return []

    def load_document(self, document_id: str) -> Document:
        raise NotImplementedError("DocVQAAdapter is in SCAFFOLDED state. Data ingestion begins in Phase 2.")

    def load_annotations(self, document_id: str) -> List[Dict[str, Any]]:
        return []

    def get_metadata(self) -> Dict[str, Any]:
        return {
            "name": "DocVQA",
            "state": self.state.value,
            "license": "Non-commercial Academic Research",
            "reference": "Mathew et al., WACV 2021"
        }


class FUNSDAdapter(DatasetAdapter):
    """Adapter for FUNSD noisy scanned forms."""
    @property
    def dataset_name(self) -> str:
        return "FUNSD"

    def list_documents(self, partition: Optional[str] = None) -> List[str]:
        return []

    def load_document(self, document_id: str) -> Document:
        raise NotImplementedError("FUNSDAdapter is in SCAFFOLDED state.")

    def load_annotations(self, document_id: str) -> List[Dict[str, Any]]:
        return []

    def get_metadata(self) -> Dict[str, Any]:
        return {
            "name": "FUNSD",
            "state": self.state.value,
            "license": "Open Access Research",
            "reference": "Jaume et al., ICDAR-W 2019"
        }


class SROIEAdapter(DatasetAdapter):
    """Adapter for SROIE receipt parsing benchmark."""
    @property
    def dataset_name(self) -> str:
        return "SROIE"

    def list_documents(self, partition: Optional[str] = None) -> List[str]:
        return []

    def load_document(self, document_id: str) -> Document:
        raise NotImplementedError("SROIEAdapter is in SCAFFOLDED state.")

    def load_annotations(self, document_id: str) -> List[Dict[str, Any]]:
        return []

    def get_metadata(self) -> Dict[str, Any]:
        return {"name": "SROIE", "state": self.state.value}


class CORDAdapter(DatasetAdapter):
    """Adapter for CORD retail receipt benchmark."""
    @property
    def dataset_name(self) -> str:
        return "CORD"

    def list_documents(self, partition: Optional[str] = None) -> List[str]:
        return []

    def load_document(self, document_id: str) -> Document:
        raise NotImplementedError("CORDAdapter is in SCAFFOLDED state.")

    def load_annotations(self, document_id: str) -> List[Dict[str, Any]]:
        return []

    def get_metadata(self) -> Dict[str, Any]:
        return {"name": "CORD", "state": self.state.value}


class MMLongBenchDocAdapter(DatasetAdapter):
    """Adapter for MMLongBench-Doc multi-page benchmark."""
    @property
    def dataset_name(self) -> str:
        return "MMLongBench-Doc"

    def list_documents(self, partition: Optional[str] = None) -> List[str]:
        return []

    def load_document(self, document_id: str) -> Document:
        raise NotImplementedError("MMLongBenchDocAdapter is in SCAFFOLDED state.")

    def load_annotations(self, document_id: str) -> List[Dict[str, Any]]:
        return []

    def get_metadata(self) -> Dict[str, Any]:
        return {
            "name": "MMLongBench-Doc",
            "state": self.state.value,
            "license": "MIT",
            "reference": "Wang et al., NeurIPS 2024"
        }


class LongDocURLAdapter(DatasetAdapter):
    """Adapter for LongDocURL multimodal long document benchmark."""
    @property
    def dataset_name(self) -> str:
        return "LongDocURL"

    def list_documents(self, partition: Optional[str] = None) -> List[str]:
        return []

    def load_document(self, document_id: str) -> Document:
        raise NotImplementedError("LongDocURLAdapter is in SCAFFOLDED state.")

    def load_annotations(self, document_id: str) -> List[Dict[str, Any]]:
        return []

    def get_metadata(self) -> Dict[str, Any]:
        return {
            "name": "LongDocURL",
            "state": self.state.value,
            "license": "Research Use Only",
            "reference": "Deng et al., ACL 2025"
        }


class XLDocBenchAdapter(DatasetAdapter):
    """Adapter for XL-DocBench extra-long document benchmark."""
    @property
    def dataset_name(self) -> str:
        return "XL-DocBench"

    def list_documents(self, partition: Optional[str] = None) -> List[str]:
        return []

    def load_document(self, document_id: str) -> Document:
        raise NotImplementedError("XLDocBenchAdapter is in SCAFFOLDED state.")

    def load_annotations(self, document_id: str) -> List[Dict[str, Any]]:
        return []

    def get_metadata(self) -> Dict[str, Any]:
        return {
            "name": "XL-DocBench",
            "state": self.state.value,
            "license": "Research Use Only",
            "reference": "arXiv:2608.00036"
        }
