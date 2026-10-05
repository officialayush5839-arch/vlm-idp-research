"""
Unified Calibration Manager and Artifact Persistence for Phase 8.
Orchestrates fitting, serialization, cryptographic verification, and inference
across uncalibrated, temperature scaling, and isotonic regression calibrators.
"""

import os
import json
import hashlib
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from src.uncertainty.schema import CalibrationArtifact
from src.uncertainty.temperature import TemperatureScalingCalibrator
from src.uncertainty.isotonic import IsotonicRegressionCalibrator


def compute_sha256(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


class CalibrationManager:
    """
    Manages post-hoc calibration models, cryptographic hashing, and prediction.
    """

    def __init__(self, method: str = "uncalibrated", config: Optional[Dict[str, Any]] = None):
        self.method = method
        self.config = config or {}
        self.calibrator = None

        if method == "temperature_scaling":
            self.calibrator = TemperatureScalingCalibrator()
        elif method == "isotonic_regression":
            self.calibrator = IsotonicRegressionCalibrator()
        elif method == "uncalibrated":
            self.calibrator = None
        else:
            raise ValueError(f"Unknown calibration method: {method}")

    def fit(self, confidences: List[float], labels: List[int]) -> "CalibrationManager":
        """
        Fit calibrator on validation partition.
        """
        if self.method == "uncalibrated":
            return self
        self.calibrator.fit(confidences, labels)
        return self

    def predict(self, raw_confidence: float) -> float:
        """
        Calibrate a single confidence score.
        """
        if self.method == "uncalibrated" or self.calibrator is None:
            return float(max(0.0, min(1.0, round(raw_confidence, 6))))
        return self.calibrator.predict(raw_confidence)

    def predict_batch(self, confidences: List[float]) -> List[float]:
        """
        Calibrate a list of confidence scores.
        """
        if self.method == "uncalibrated" or self.calibrator is None:
            return [float(max(0.0, min(1.0, round(c, 6)))) for c in confidences]
        return self.calibrator.predict_batch(confidences)

    def export_artifact(self, training_partition: str = "val") -> CalibrationArtifact:
        """
        Generate serialized CalibrationArtifact with cryptographic SHA-256 fingerprint.
        """
        if training_partition.lower() == "test":
            raise ValueError("Forbidden to train/fit calibration on test partition! Must use validation partition.")
        temp_val = None
        iso_x = None
        iso_y = None

        if self.method == "temperature_scaling" and self.calibrator:
            temp_val = self.calibrator.temperature
        elif self.method == "isotonic_regression" and self.calibrator:
            iso_x = self.calibrator.x_thresholds
            iso_y = self.calibrator.y_thresholds

        now_utc = datetime.now(timezone.utc).isoformat()
        cfg_str = json.dumps(self.config, sort_keys=True)
        cfg_hash = compute_sha256(cfg_str)

        raw_payload = f"{self.method}|{training_partition}|{temp_val}|{iso_x}|{iso_y}|{cfg_hash}"
        art_hash = compute_sha256(raw_payload)

        return CalibrationArtifact(
            method=self.method,
            training_partition=training_partition,
            temperature=temp_val,
            isotonic_x=iso_x,
            isotonic_y=iso_y,
            config_hash=cfg_hash,
            artifact_hash=art_hash,
            created_at_utc=now_utc
        )

    def save_artifact(self, filepath: str, training_partition: str = "val") -> str:
        """
        Save CalibrationArtifact to disk and return its SHA-256 checksum.
        """
        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
        artifact = self.export_artifact(training_partition=training_partition)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(artifact.model_dump_json(indent=2))
        return artifact.artifact_hash

    @classmethod
    def load_artifact(cls, filepath: str) -> "CalibrationManager":
        """
        Load CalibrationArtifact from disk, re-verify hash, and initialize manager.
        """
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        art = CalibrationArtifact(**data)

        # Re-verify artifact hash
        raw_payload = f"{art.method}|{art.training_partition}|{art.temperature}|{art.isotonic_x}|{art.isotonic_y}|{art.config_hash}"
        expected_hash = compute_sha256(raw_payload)
        if art.artifact_hash != expected_hash:
            raise ValueError(f"Cryptographic hash mismatch in calibration artifact {filepath}!")

        mgr = cls(method=art.method)
        if art.method == "temperature_scaling":
            mgr.calibrator = TemperatureScalingCalibrator(temperature=art.temperature)
            mgr.calibrator.is_fitted = True
        elif art.method == "isotonic_regression":
            mgr.calibrator = IsotonicRegressionCalibrator.from_dict({
                "x_thresholds": art.isotonic_x,
                "y_thresholds": art.isotonic_y,
                "is_fitted": True
            })
        return mgr
