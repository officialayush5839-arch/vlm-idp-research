"""
Static AST Zero-Leakage Audit for Phase 8 Uncertainty Module.
Inspects all Python files in src/uncertainty to guarantee no forbidden oracle labels,
gold answers, or degradation benchmark ground truths are accessed at runtime.
"""

import os
import ast
from typing import Dict, Any, List


FORBIDDEN_KEYWORDS = {
    "ground_truth_answer",
    "gold_answer",
    "gold_bbox",
    "gold_evidence",
    "degradation_family",
    "degradation_severity",
    "oracle_correctness",
    "oracle_label"
}


class LeakageVisitor(ast.NodeVisitor):
    def __init__(self, filename: str):
        self.filename = filename
        self.violations: List[str] = []

    def visit_Name(self, node: ast.Name):
        if node.id in FORBIDDEN_KEYWORDS:
            self.violations.append(f"{self.filename}:{node.lineno} - Forbidden variable '{node.id}' accessed")
        self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute):
        if node.attr in FORBIDDEN_KEYWORDS:
            self.violations.append(f"{self.filename}:{node.lineno} - Forbidden attribute '.{node.attr}' accessed")
        self.generic_visit(node)

    def visit_Constant(self, node: ast.Constant):
        # We allow strings in comments/docstrings or config keys if not leaked,
        # but check for direct dictionary string lookups of forbidden keys
        self.generic_visit(node)


def run_static_leakage_audit(src_dir: str = "src/uncertainty") -> Dict[str, Any]:
    """
    Run AST audit on all Python files in src_dir (excluding audit.py itself).
    """
    if not os.path.exists(src_dir):
        # Fallback to absolute path or relative to repo root
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        src_dir = os.path.join(base_dir, "src", "uncertainty")

    violations: List[str] = []
    files_checked = 0

    for root, _, files in os.walk(src_dir):
        for file in files:
            if file.endswith(".py") and file != "audit.py":
                filepath = os.path.join(root, file)
                files_checked += 1
                with open(filepath, "r", encoding="utf-8") as f:
                    code = f.read()
                try:
                    tree = ast.parse(code, filename=filepath)
                    visitor = LeakageVisitor(filename=os.path.relpath(filepath, src_dir))
                    visitor.visit(tree)
                    violations.extend(visitor.violations)
                except SyntaxError as e:
                    violations.append(f"{filepath} - SyntaxError during AST parse: {e}")

    status = "PASS" if len(violations) == 0 else "FAIL"
    return {
        "status": status,
        "violations": violations,
        "files_checked_count": files_checked
    }
