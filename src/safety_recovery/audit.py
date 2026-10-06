"""src/safety_recovery/audit.py
Static AST Zero-Leakage Checker for src/safety_recovery/.
"""

import ast
import os
from typing import List, Tuple

FORBIDDEN_KEYWORDS = {
    "ground_truth",
    "gold_label",
    "gold_answer",
    "target_label",
    "true_label",
    "oracle",
    "label_leakage",
}


class ZeroLeakageAuditor:
    """Scans python files in src/safety_recovery/ for forbidden keywords."""

    @staticmethod
    def audit_directory(dir_path: str = "src/safety_recovery") -> List[Tuple[str, int, str]]:
        violations = []
        for root, _, files in os.walk(dir_path):
            for file in files:
                if file.endswith(".py") and file != "audit.py":
                    p = os.path.join(root, file)
                    with open(p, "r", encoding="utf-8") as f:
                        tree = ast.parse(f.read(), filename=p)
                    for node in ast.walk(tree):
                        if isinstance(node, ast.Name) and node.id in FORBIDDEN_KEYWORDS:
                            violations.append((p, node.lineno, f"Forbidden name: {node.id}"))
                        elif isinstance(node, ast.Attribute) and node.attr in FORBIDDEN_KEYWORDS:
                            violations.append((p, node.lineno, f"Forbidden attr: {node.attr}"))
        return violations
