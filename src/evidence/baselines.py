"""
Baseline Registry and Adapters for Phase 7 Evidence Grounding.
Maps retrieval and grounding configurations across baselines:
- B7-0: Random Evidence Baseline
- B7-1: BM25 / Lexical Only
- B7-2: Dense Embedding Only
- B7-3: Visual Only
- B7-4: Hybrid Retrieval
- B7-5: Proposed Hierarchical Multimodal Grounding
"""

from typing import Dict, Any, List, Optional
from src.evidence.schema import EvidenceUnit


BASELINE_MAP = {
    "B7-0": {
        "name": "Random Evidence Baseline",
        "upstream_retrieval": "B6-0",
        "uses_layout": False,
        "uses_multimodal": False,
        "uses_numeric_verifier": False,
        "uses_table_verifier": False,
    },
    "B7-1": {
        "name": "BM25 / Lexical Only",
        "upstream_retrieval": "B6-1",
        "uses_layout": False,
        "uses_multimodal": False,
        "uses_numeric_verifier": True,
        "uses_table_verifier": False,
    },
    "B7-2": {
        "name": "Dense Embedding Only",
        "upstream_retrieval": "B6-2",
        "uses_layout": False,
        "uses_multimodal": False,
        "uses_numeric_verifier": True,
        "uses_table_verifier": False,
    },
    "B7-3": {
        "name": "Visual Only",
        "upstream_retrieval": "B6-3",
        "uses_layout": True,
        "uses_multimodal": True,
        "uses_numeric_verifier": False,
        "uses_table_verifier": False,
    },
    "B7-4": {
        "name": "Hybrid Retrieval",
        "upstream_retrieval": "B6-4",
        "uses_layout": False,
        "uses_multimodal": True,
        "uses_numeric_verifier": True,
        "uses_table_verifier": False,
    },
    "B7-5": {
        "name": "Proposed Hierarchical Multimodal Grounding",
        "upstream_retrieval": "B6-5",
        "uses_layout": True,
        "uses_multimodal": True,
        "uses_numeric_verifier": True,
        "uses_table_verifier": True,
    }
}


def get_baseline_config(baseline_id: str) -> Dict[str, Any]:
    """
    Retrieve configuration dictionary for a baseline ID (B7-0 to B7-5).
    """
    if baseline_id not in BASELINE_MAP:
        raise ValueError(f"Unknown Phase 7 baseline ID: {baseline_id}. Valid: {list(BASELINE_MAP.keys())}")
    return BASELINE_MAP[baseline_id]
