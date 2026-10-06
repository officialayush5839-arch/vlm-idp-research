"""src/robustness/audit.py
Static analysis zero-leakage auditor for Phase 10 source code.
Uses Python AST inspection to guarantee that forbidden ground-truth identifiers
and test-domain cheat flags are never accessed in runtime decision paths.
"""

import ast
from pathlib import Path
from typing import List, Dict, Any, Set

FORBIDDEN_NAMES: Set[str] = {
    "ground_truth",
    "gold_answer",
    "gold_label",
    "gold_bbox",
    "gold_region",
    "test_label",
    "oracle_model",
    "test_score",
    "test_metric",
    "degradation_severity_label",
    "degradation_family_label",
}


class RobustnessZeroLeakageAuditor:
    """Inspects src/robustness/ Python modules for forbidden ground truth references."""

    @staticmethod
    def audit_module(file_path: Path) -> List[Dict[str, Any]]:
        violations = []
        with open(file_path, "r", encoding="utf-8") as f:
            source = f.read()

        try:
            tree = ast.parse(source, filename=str(file_path))
        except SyntaxError as e:
            return [{"line": e.lineno, "message": f"SyntaxError during AST parsing: {e}"}]

        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and node.id in FORBIDDEN_NAMES:
                if file_path.name not in ("evaluation.py", "robustness_metrics.py"):
                    violations.append({
                        "file": str(file_path.name),
                        "line": getattr(node, "lineno", 0),
                        "name": node.id,
                        "message": f"Illegal access to ground-truth symbol: {node.id}",
                    })
            elif isinstance(node, ast.Attribute) and node.attr in FORBIDDEN_NAMES:
                if file_path.name not in ("evaluation.py", "robustness_metrics.py"):
                    violations.append({
                        "file": str(file_path.name),
                        "line": getattr(node, "lineno", 0),
                        "name": node.attr,
                        "message": f"Illegal access to ground-truth attribute: {node.attr}",
                    })

        return violations

    @classmethod
    def audit_robustness_package(cls, package_dir: Path) -> List[Dict[str, Any]]:
        all_violations = []
        for py_file in package_dir.glob("*.py"):
            violations = cls.audit_module(py_file)
            all_violations.extend(violations)
        return all_violations
