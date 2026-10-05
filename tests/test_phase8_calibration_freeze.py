import os
import tempfile
import pytest
from src.uncertainty.calibration import CalibrationManager


def test_calibration_freeze_and_reverification():
    mgr = CalibrationManager(method="temperature_scaling")
    mgr.fit([0.2, 0.4, 0.6, 0.8], [0, 0, 1, 1])

    with tempfile.TemporaryDirectory() as tmpdir:
        art_path = os.path.join(tmpdir, "frozen_model.json")
        orig_hash = mgr.save_artifact(art_path, training_partition="val")

        # Load and verify intact hash
        loaded_mgr = CalibrationManager.load_artifact(art_path)
        re_exported = loaded_mgr.export_artifact(training_partition="val")
        assert re_exported.artifact_hash == orig_hash

        # Run mock inference
        for c in [0.1, 0.5, 0.9]:
            loaded_mgr.predict(c)

        # Confirm artifact file has not been altered
        reloaded = CalibrationManager.load_artifact(art_path)
        assert reloaded.export_artifact(training_partition="val").artifact_hash == orig_hash
