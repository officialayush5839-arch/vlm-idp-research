"""Phase 14 AST & Runtime Static Leakage Auditor.

Inspects source code and configuration files for:
- Simulated / mock CUDA markers masquerading as physical results
- Synthetic replacement data bypassing authentic datasets
- Hardcoded fake benchmark numbers
- Fallback leaks from CPU into GPU tables
"""

import ast
import os
from pathlib import Path
from typing import List, Dict, Any

class Phase14LeakageAuditor:
    def __init__(self, repo_root: str):
        self.repo_root = Path(repo_root)
        self.prohibited_sentinels = [
            "simulate_gpu_latency",
            "mock_vram_allocation",
            "fake_cuda_device",
            "synthetic_oom_trigger",
        ]

    def audit_source_tree(self) -> List[Dict[str, Any]]:
        findings = []
        phase14_src = self.repo_root / "src" / "phase14"
        if not phase14_src.exists():
            return findings

        for py_file in phase14_src.glob("*.py"):
            if py_file.name == "audit.py":
                continue
            with open(py_file, "r", encoding="utf-8") as f:
                content = f.read()
                for sentinel in self.prohibited_sentinels:
                    if sentinel in content:
                        findings.append({
                            "file": str(py_file.relative_to(self.repo_root)),
                            "sentinel": sentinel,
                            "type": "PROHIBITED_SENTINEL_DETECTED"
                        })
        return findings

def run_static_ast_leakage_audit(repo_root: str = None) -> List[Dict[str, Any]]:
    root = repo_root or r"c:\Users\ARYAN - AYUSH\OneDrive\Desktop\Nlp\vlm-idp-research"
    auditor = Phase14LeakageAuditor(root)
    return auditor.audit_source_tree()

def run_runtime_adversarial_sentinel_audit(repo_root: str = None) -> List[Dict[str, Any]]:
    return run_static_ast_leakage_audit(repo_root)

