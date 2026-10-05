"""
Phase 8 Smoke Test Script.
Performs an end-to-end dry run of baselines A0 through A5 on sample queries.
"""

import os
import sys
import json
import yaml

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.uncertainty.pipeline import UncertaintyPipeline
from src.uncertainty.baselines import (
    BaselineRegistry,
    A0NoAbstentionBaseline,
    A1RandomAbstentionBaseline,
    A2UncalibratedBaseline,
    A3TemperatureScalingBaseline,
    A4IsotonicBaseline,
    A5EvidenceAwareBaseline
)
from src.uncertainty.schema import UncertaintyPackage


def run_smoke():
    print("=== Starting Phase 8 Smoke Test ===")

    manifest_path = "experiments/phase6/indexes/corpus_manifest.json"
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    # Pick 1 val query and 1 test query
    val_q = [q for q in manifest["queries"] if any(d["document_id"] == q["document_id"] and d["split"] == "val" for d in manifest["documents"])][0]
    test_q = [q for q in manifest["queries"] if any(d["document_id"] == q["document_id"] and d["split"] == "test" for d in manifest["documents"])][0]

    pipeline = UncertaintyPipeline(method="uncalibrated")

    for label, q in [("Validation", val_q), ("Test", test_q)]:
        pkg = pipeline.process(
            document_id=q["document_id"],
            query_id=q["query_id"],
            model_output={"confidence": 0.82},
            retrieval_metadata={"retrieval_margin": 0.45, "retrieval_entropy": 0.3},
            grounding_result={
                "semantic_support_score": 0.88,
                "entity_coverage": 0.90,
                "is_valid_box": True,
                "sufficiency_status": "SUFFICIENT",
                "grounding_status": "GROUNDED",
                "citation_count": 2
            },
            quality_metadata={"overall_quality": 0.85, "blur": 0.1, "noise": 0.1, "skew": 0.0, "contrast": 0.9, "resolution": 0.9}
        )
        assert isinstance(pkg, UncertaintyPackage)
        assert len(pkg.package_hash) == 64
        print(f"[{label}] Query {q['query_id']}: Decision={pkg.decision.decision}, Status={pkg.decision.uncertainty_status if hasattr(pkg.decision, 'uncertainty_status') else 'OK'}, CalConf={pkg.calibrated_confidence}")

    # Verify all baselines
    print("Testing baselines A0-A5...")
    for b_name in BaselineRegistry.list_baselines():
        b_cls = BaselineRegistry.get(b_name)
        b_inst = b_cls()
        res = b_inst.evaluate_single(confidence=0.75, features=pkg.features, target_coverage=0.8)
        assert res.decision.decision in ["ANSWER", "ABSTAIN"]
        print(f"  {b_name}: {res.decision.decision} (threshold={res.decision.threshold})")

    print("=== Phase 8 Smoke Test PASSED ===")


if __name__ == "__main__":
    run_smoke()
