"""tests/test_phase10_5_partition_integrity.py
Unit tests verifying test partition integrity and document preservation across domains.
"""

import json


def test_test_partition_docs():
    with open("experiments/phase6/indexes/corpus_manifest.json", "r", encoding="utf-8") as f:
        corpus = json.load(f)

    test_docs = [d for d in corpus["documents"] if d["split"] == "test"]
    assert len(test_docs) == 25, f"Expected exactly 25 test documents, found {len(test_docs)}"

    # Check that experiment manifest maps exactly 5 unique documents to each of D0-D4
    with open("experiments/phase10/manifests/experiment_manifest.json", "r", encoding="utf-8") as f:
        man = json.load(f)

    docs_by_dom = {}
    for e in man["experiments"]:
        dom = e["domain_id"]
        doc = e["document_id"]
        if dom not in docs_by_dom:
            docs_by_dom[dom] = set()
        docs_by_dom[dom].add(doc)

    for i in range(5):
        dom_key = [k for k in docs_by_dom.keys() if f"D{i}_" in k][0]
        assert len(docs_by_dom[dom_key]) == 5, f"Expected 5 docs for {dom_key}, got {len(docs_by_dom[dom_key])}"
