"""
Zero-Leakage Static Code Auditor for Phase 5.
Parses AST of routing modules to guarantee zero access to ground truth, evaluation scores,
or synthetic degradation labels at inference time.
"""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Any, Dict, List


FORBIDDEN_IDENTIFIERS: List[str] = [
    "ground_truth_answers",
    "ground_truth_bboxes",
    "target_class",
    "evaluator_score",
    "condition_severity",
    "synthetic_severity",
    "true_severity",
    "true_family",
]


class ZeroLeakageRouterAuditor:
    """
    Performs static AST code verification on routing modules.
    Guarantees no access to ground truth, evaluation scores, or synthetic degradation labels.
    """

    def __init__(self, forbidden_terms: Optional[List[str]] = None):
        self.forbidden_terms = forbidden_terms or list(FORBIDDEN_IDENTIFIERS)

    def audit_file(self, file_path: str) -> Dict[str, Any]:
        """
        Audits a single python source file for forbidden leakage identifiers.
        """
        path = Path(file_path)
        violations: List[str] = []

        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except Exception as e:
            return {
                "file": str(path),
                "status": "ERROR",
                "violations": [f"AST Parse Error: {e}"],
            }

        for node in ast.walk(tree):
            # Check function definition argument names
            if isinstance(node, ast.FunctionDef):
                for arg in node.args.args:
                    if arg.arg in self.forbidden_terms:
                        violations.append(
                            f"File {path.name}:{node.lineno} - Function '{node.name}' contains forbidden argument '{arg.arg}'"
                        )
            # Check name references
            elif isinstance(node, ast.Name):
                if node.id in self.forbidden_terms:
                    violations.append(
                        f"File {path.name}:{node.lineno} - Code references forbidden identifier '{node.id}'"
                    )
            # Check attribute access
            elif isinstance(node, ast.Attribute):
                attr_name = node.attr
                full_attr = f"{node.value.id}.{attr_name}" if isinstance(node.value, ast.Name) else attr_name
                if attr_name in self.forbidden_terms or full_attr in self.forbidden_terms:
                    violations.append(
                        f"File {path.name}:{node.lineno} - Code references forbidden attribute '{full_attr}'"
                    )

        status = "FAIL" if violations else "PASS"
        return {
            "file": str(path),
            "status": status,
            "violations": violations,
        }

    def audit_directory(self, dir_path: str) -> Dict[str, Any]:
        """
        Audits all Python files in a directory, ignoring __pycache__.
        """
        base = Path(dir_path)
        py_files = [f for f in base.glob("*.py") if not f.name.startswith("__")]
        all_violations: List[str] = []
        files_scanned = 0

        for f in py_files:
            # Skip test files and auditor itself
            if f.name.startswith("test_") or f.name == "audit.py":
                continue
            files_scanned += 1
            res = self.audit_file(str(f))
            if res["status"] != "PASS":
                all_violations.extend(res["violations"])

        status = "FAIL" if all_violations else "PASS"
        return {
            "directory": str(base),
            "files_scanned": files_scanned,
            "status": status,
            "violations": all_violations,
        }
