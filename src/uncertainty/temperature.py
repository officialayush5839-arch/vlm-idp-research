"""
Temperature Scaling Post-Hoc Calibrator for Phase 8.
Optimizes a single temperature parameter T > 0 on validation logits
via Negative Log-Likelihood (NLL) minimization.
"""

import math
import numpy as np
from scipy.optimize import minimize_scalar
from typing import Dict, Any, List, Optional


def logit(p: float, eps: float = 1e-6) -> float:
    """
    Inverse sigmoid (logit function) with numerical clamping.
    """
    clamped_p = max(eps, min(1.0 - eps, float(p)))
    return math.log(clamped_p / (1.0 - clamped_p))


def sigmoid(z: float) -> float:
    """
    Numerically stable logistic sigmoid function.
    """
    if z >= 0:
        ez = math.exp(-z)
        return 1.0 / (1.0 + ez)
    else:
        ez = math.exp(z)
        return ez / (1.0 + ez)


class TemperatureScalingCalibrator:
    """
    Fits and applies Temperature Scaling to confidence scores.
    """

    def __init__(self, temperature: float = 1.0, bounds: tuple = (0.01, 10.0)):
        self.temperature = float(temperature)
        self.bounds = bounds
        self.is_fitted = False

    def fit(self, confidences: List[float], labels: List[int]) -> "TemperatureScalingCalibrator":
        """
        Fit temperature T by minimizing binary cross-entropy on validation data.
        """
        if len(confidences) == 0 or len(labels) == 0:
            raise ValueError("Cannot fit temperature scaling on empty data")
        if len(confidences) != len(labels):
            raise ValueError("Confidences and labels must have identical length")

        confs = np.asarray(confidences, dtype=float)
        y = np.asarray(labels, dtype=float)

        logits = np.array([logit(c) for c in confs], dtype=float)

        def nll_objective(t: float) -> float:
            scaled_logits = logits / t
            # Stable BCE
            losses = np.maximum(scaled_logits, 0) - scaled_logits * y + np.log1p(np.exp(-np.abs(scaled_logits)))
            return float(np.mean(losses))

        res = minimize_scalar(nll_objective, bounds=self.bounds, method="bounded")
        self.temperature = float(res.x)
        self.is_fitted = True
        return self

    def predict(self, confidence: float) -> float:
        """
        Calibrate a single confidence score.
        """
        z = logit(confidence)
        scaled_z = z / self.temperature
        return float(max(0.0, min(1.0, round(sigmoid(scaled_z), 6))))

    def predict_batch(self, confidences: List[float]) -> List[float]:
        """
        Calibrate a batch of confidence scores.
        """
        return [self.predict(c) for c in confidences]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "method": "temperature_scaling",
            "temperature": self.temperature,
            "bounds": list(self.bounds),
            "is_fitted": self.is_fitted
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TemperatureScalingCalibrator":
        cal = cls(
            temperature=data.get("temperature", 1.0),
            bounds=tuple(data.get("bounds", [0.01, 10.0]))
        )
        cal.is_fitted = data.get("is_fitted", True)
        return cal
