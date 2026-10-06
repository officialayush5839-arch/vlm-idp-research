"""src/robustness/domain_registry.py
Immutable domain registry defining evaluation domains D0 through D4.
"""

from typing import Dict, Any, List, Optional
from pathlib import Path
import yaml
from src.robustness.schema import DomainID


class DomainRegistry:
    """Provides validated domain specifications and document mappings."""

    def __init__(self, config_path: Optional[Path] = None):
        cfg_path = config_path or (
            Path(__file__).resolve().parent.parent.parent / "configs" / "phase10" / "domain_config.yaml"
        )
        with open(cfg_path, "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f)

        self.domains: Dict[DomainID, Dict[str, Any]] = {}
        self.doc_to_domain: Dict[str, DomainID] = {}

        for d in cfg.get("domains", []):
            d_id = DomainID(d["domain_id"])
            self.domains[d_id] = d
            for doc_id in d.get("document_ids", []):
                self.doc_to_domain[doc_id] = d_id

    def get_domain(self, domain_id: DomainID) -> Dict[str, Any]:
        return self.domains[domain_id]

    def get_domain_for_doc(self, doc_id: str) -> Optional[DomainID]:
        return self.doc_to_domain.get(doc_id)

    def list_domains(self) -> List[DomainID]:
        return list(self.domains.keys())
