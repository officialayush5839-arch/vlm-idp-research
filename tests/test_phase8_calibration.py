import os
import tempfile
import pytest
from src.uncertainty.calibration import CalibrationManager


def test_calibration_manager_uncalibrated():
    mgr = CalibrationManager(method="uncalibrated")
    mgr.fit([0.2, 0.8], [0, 1])
    assert mgr.predict(0.75) == 0.75
    assert mgr.predict_batch([0.1, 0.9]) == [0.1, 0.9]


def test_calibration_manager_temperature_scaling():
    mgr = CalibrationManager(method="temperature_scaling")
    confidences = [0.1, 0.2, 0.4, 0.6, 0.8, 0.9]
    labels = [0, 0, 0, 1, 1, 1]
    mgr.fit(confidences, labels)

    with tempfile.TemporaryDirectory() as tmpdir:
        art_path = os.path.join(tmpdir, "temp_art.json")
        art_hash = mgr.save_artifact(art_path, training_partition="val")
        assert len(art_hash) == 64

        loaded_mgr = CalibrationManager.load_artifact(art_path)
        assert loaded_mgr.method == "temperature_scaling"
        assert abs(loaded_mgr.predict(0.6) - mgr.predict(0.6)) < 1e-5

        # Tamper test
        with open(art_path, "r", encoding="utf-8") as f:
            content = f.read()
        tampered_content = content.replace('"temperature":', '"temperature": 9.99, "_orig_temp":')
        with open(art_path, "w", encoding="utf-8") as f:
            f.write(tampered_content)

        with pytest.raises(ValueError, match="hash mismatch"):
            CalibrationManager.load_artifact(art_path)


def test_calibration_manager_isotonic_regression():
    mgr = CalibrationManager(method="isotonic_regression")
    confidences = [0.1, 0.2, 0.4, 0.6, 0.8, 0.9]
    labels = [0, 0, 0, 1, 1, 1]
    mgr.fit(confidences, labels)

    with tempfile.TemporaryDirectory() as tmpdir:
        art_path = os.path.join(tmpdir, "iso_art.json")
        art_hash = mgr.save_artifact(art_path, training_partition="val")
        assert len(art_hash) == 64

        loaded_mgr = CalibrationManager.load_artifact(art_path)
        assert loaded_mgr.method == "isotonic_regression"
        assert abs(loaded_mgr.predict(0.6) - mgr.predict(0.6)) < 1e-5
