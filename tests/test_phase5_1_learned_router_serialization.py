"""
Tests for Phase 5.1 Learned Router Serialization (Audit Defect P1-03).
Verifies joblib model serialization, loading, and prediction parity.
"""

import pytest
import tempfile
import shutil
from pathlib import Path
import numpy as np

from src.routing.learned_router import LearnedQualityRouter


def test_learned_router_serialization_and_reloading():
    """Verify that a fitted router serializes and reloads with exact prediction parity."""
    temp_dir = tempfile.mkdtemp()
    try:
        model_path = Path(temp_dir) / "test_learned_router.joblib"

        router = LearnedQualityRouter(classifier_type="logistic", random_state=42)
        assert router.is_fitted is False

        # Attempting to save unfitted router must raise ValueError
        with pytest.raises(ValueError):
            router.save(model_path)

        # Fit on synthetic training data
        np.random.seed(42)
        X = np.random.uniform(0.0, 1.0, size=(50, 10))
        y = ["B0" if x[0] < 0.3 else ("B1" if x[1] < 0.5 else "B2") for x in X]
        router.fit(X, y, partition="train")
        assert router.is_fitted is True

        # Save to disk
        router.save(model_path)
        assert model_path.exists()

        # Reload from disk
        reloaded = LearnedQualityRouter.from_file(model_path)
        assert reloaded.is_fitted is True
        assert reloaded.classifier_type == "logistic"
        assert len(reloaded.feature_names) == 10

        # Test prediction parity on unseen test vectors
        X_test = np.random.uniform(0.0, 1.0, size=(10, 10))
        for vec in X_test:
            pred1, reason1, conf1 = router.predict(vec)
            pred2, reason2, conf2 = reloaded.predict(vec)
            assert pred1 == pred2
            assert reason1 == reason2
            assert abs(conf1 - conf2) < 1e-6

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)
