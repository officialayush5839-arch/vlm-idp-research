import pytest


def test_prior_phases_regression_import():
    # Phase 1, 2, 2.5
    import src.ocr
    import src.vlm

    # Phase 3
    import src.quality

    # Phase 5 & 5.1
    import src.routing

    # Phase 6
    import src.retrieval

    # Phase 7
    import src.grounding

    assert True
