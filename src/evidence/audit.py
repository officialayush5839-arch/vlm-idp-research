"""
Static AST Zero-Leakage Audit Module for Phase 7 Evidence Grounding.
Verifies that runtime modules under src/evidence/ do not access
oracle ground-truth attributes or test-set labels.
"""

import ast
import os
import glob
from typing import Dict, Any, List, Set


FORBIDDEN_ATTRIBUTES = {
    "ground_truth_answer",
    "target_answer",
    "oracle_answer",
    "gold_answer",
    "test_answer"
}

# Modules allowed to reference ground truth (purely evaluation-only metrics or test utilities)
EVAL_ALLOWED_FILES = {
    "schema.py",
    "metrics.py",
    "audit.py"
}


def audit_zero_leakage(src_dir: str = "src/evidence") -> Dict[str, Any]:
    """
    Scan all Python files in src_dir and verify AST does not contain
    forbidden oracle/ground-truth leakage references in runtime execution paths.
    """
    py_files = glob.glob(os.path.join(src_dir, "*.py"))
    violations: List[Dict[str, Any]] = []

    for fpath in py_files:
        fname = os.path.basename(fpath)
        if fname in EVAL_ALLOWED_FILES:
            continue

        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        parsed = ast.parse(content, filename=fpath)

        for node in ast.walk(parsed):
            # Check attribute access (e.g. obj.ground_truth_answer)
            if isinstance(node, ast.Attribute):
                if node.attr in FORBIDDEN_ATTRIBUTES:
                    violations.append({
                        "file": fname,
                        "line": getattr(node, "lineno", -1),
                        "type": "attribute",
                        "identifier": node.attr
                    })
            # Check variable name access (e.g. ground_truth_answer)
            elif isinstance(node, ast.Name):
                if node.id in FORBIDDEN_ATTRIBUTES:
                    violations.append({
                        "file": fname,
                        "line": getattr(node, "lineno", -1),
                        "type": "name",
                        "identifier": node.id
                    })

    is_clean = len(violations) == 0
    return {
        "audited_directory": src_dir,
        "files_checked": [os.path.basename(p) for p in py_files],
        "zero_leakage_verified": is_clean,
        "violation_count": len(violations),
        "violations": violations
    }
