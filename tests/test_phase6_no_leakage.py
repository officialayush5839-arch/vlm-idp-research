"""
Zero-Leakage Audit for Phase 6 Retrieval Codebase.
Performs AST and string audits verifying that retrieval models and pipeline modules
do NOT access test-set ground-truth labels or answers during indexing, scoring, or selection.
"""

import ast
import os
import glob


def test_retrieval_modules_no_ground_truth_leakage():
    """
    Ensure src/retrieval/*.py modules do not use ground_truth_pages
    or ground_truth_regions inside their internal ranking/indexing algorithms.
    """
    retrieval_files = glob.glob("src/retrieval/*.py")
    assert len(retrieval_files) >= 5, "Retrieval modules should exist"

    # Only schema and metrics are allowed to declare or reference ground truth for evaluation
    allowed_files = {"schema.py", "metrics.py"}

    forbidden_attributes = {"ground_truth_pages", "ground_truth_regions", "ground_truth_answer"}

    for fpath in retrieval_files:
        fname = os.path.basename(fpath)
        if fname in allowed_files:
            continue

        with open(fpath, "r", encoding="utf-8") as f:
            code = f.read()

        parsed = ast.parse(code, filename=fpath)

        for node in ast.walk(parsed):
            if isinstance(node, ast.Attribute):
                if node.attr in forbidden_attributes:
                    raise AssertionError(
                        f"Leakage detected in {fname}: access to forbidden ground-truth attribute '{node.attr}'"
                    )
            elif isinstance(node, ast.Name):
                if node.id in forbidden_attributes:
                    raise AssertionError(
                        f"Leakage detected in {fname}: reference to forbidden ground-truth variable '{node.id}'"
                    )
