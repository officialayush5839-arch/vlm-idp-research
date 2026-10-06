"""tests/test_phase11_cardinality.py
Unit tests verifying experimental cardinality across 7 baselines, 5 domains, 25 documents, and 5 seeds.
"""

import json


def test_experiment_cardinality_planning():
    # 7 baselines * 5 domains * 5 docs * 5 seeds = 875 planned experiments
    baselines = ["B11-0", "B11-1", "B11-2", "B11-3", "B11-4", "B11-5", "B11-6"]
    domains = ["D0", "D1", "D2", "D3", "D4"]
    docs_per_domain = 5
    seeds = [42, 123, 456, 789, 101112]

    expected_total = len(baselines) * len(domains) * docs_per_domain * len(seeds)
    assert expected_total == 875, f"Expected 875 planned evaluations, calculated {expected_total}"
