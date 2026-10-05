"""
Isotonic Regression Post-Hoc Calibrator for Phase 8.
Fits a non-parametric, monotonically non-decreasing piecewise constant
mapping from raw confidence to calibrated probability.
"""

from typing import Dict, Any, List, Optional
import numpy as np
from sklearn.isotonic import IsotonicRegression


class IsotonicRegressionCalibrator:
    """
    Fits and applies Isotonic Regression to confidence scores.
    """

    def __init__(self, y_min: float = 0.0, y_max: float = 1.0):
        self.y_min = y_min
        self.y_max = y_max
        self.regressor = IsotonicRegression(
            out_of_bounds="clip",
            y_min=y_min,
            y_max=y_max,
            increasing=True
        )
        self.is_fitted = False
        self.x_thresholds: List[float] = []
        self.y_thresholds: List[float] = []

    def fit(self, confidences: List[float], labels: List[int]) -> "IsotonicRegressionCalibrator":
        """
        Fit isotonic regression on validation data.
        """
        if len(confidences) == 0 or len(labels) == 0:
            raise ValueError("Cannot fit isotonic regression on empty data")
        if len(confidences) != len(labels):
            raise ValueError("Confidences and labels must have identical length")

        confs = np.asarray(confidences, dtype=float)
        y = np.asarray(labels, dtype=float)

        self.regressor.fit(confs, y)
        self.is_fitted = True
        self.x_thresholds = [float(x) for x in self.regressor.X_thresholds_]
        self.y_thresholds = [float(val) for val in self.regressor.y_thresholds_]
        return self

    def predict(self, confidence: float) -> float:
        """
        Calibrate a single confidence score.
        """
        if not self.is_fitted:
            return float(confidence)
        val = float(self.regressor.predict([float(confidence)])[0])
        return float(max(self.y_min, min(self.y_max, round(val, 6))))

    def predict_batch(self, confidences: List[float]) -> List[float]:
        """
        Calibrate a batch of confidence scores.
        """
        if not self.is_fitted:
            return [float(c) for c in confidences]
        arr = self.regressor.predict(np.asarray(confidences, dtype=float))
        return [float(max(self.y_min, min(self.y_max, round(v, 6)))) for v in arr]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "method": "isotonic_regression",
            "y_min": self.y_min,
            "y_max": self.y_max,
            "is_fitted": self.is_fitted,
            "x_thresholds": self.x_thresholds,
            "y_thresholds": self.y_thresholds
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "IsotonicRegressionCalibrator":
        cal = cls(
            y_min=data.get("y_min", 0.0),
            y_max=data.get("y_max", 1.0)
        )
        cal.is_fitted = data.get("is_fitted", True)
        cal.x_thresholds = data.get("x_thresholds", [])
        cal.y_thresholds = data.get("y_thresholds", [])
        if cal.is_fitted and len(cal.x_thresholds) > 0 and len(cal.y_thresholds) > 0:
            cal.regressor.fit(cal.x_thresholds, cal.y_thresholds)
        return cal
