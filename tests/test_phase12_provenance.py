"""Tests for Phase 12 Provenance Descriptors."""

import json
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).parent.parent
PROV_DIR = REPO_ROOT / "data" / "phase12_authentic" / "provenance"


def test_provenance_files_count_and_keys():
    assert PROV_DIR.exists()
    prov_files = list(PROV_DIR.glob("*_provenance.json"))
    assert len(prov_files) == 260
    sample = prov_files[0]
    with open(sample, "r", encoding="utf-8") as fp:
        p = json.load(fp)
    required_keys = [
        "document_id", "family_id", "source_type", "domain",
        "acquisition_modality", "degradation_type", "page_count",
        "license_status", "source_reference", "collection_timestamp",
        "annotation_status", "checksum_sha256"
    ]
    for k in required_keys:
        assert k in p
