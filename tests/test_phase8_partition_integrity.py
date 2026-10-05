import pytest
from src.uncertainty.calibration import CalibrationManager


def test_partition_integrity_enforcement():
    mgr = CalibrationManager(method="temperature_scaling")
    mgr.fit([0.2, 0.8], [0, 1])

    # Valid export on val partition
    art_val = mgr.export_artifact(training_partition="val")
    assert art_val.training_partition == "val"

    # Exporting on test partition is explicitly forbidden and must raise ValueError
    with pytest.raises(ValueError, match="Forbidden to train/fit calibration on test partition"):
        # We enforce this in export_artifact
        mgr.export_artifact(training_partition="test")
