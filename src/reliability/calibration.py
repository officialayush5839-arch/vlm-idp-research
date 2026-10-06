"""src/reliability/calibration.py
Calibration wrapper for Phase 9, strictly operating on validation data.
"""

from typing import List, Dict, Any, Optional
import numpy as np


class ReliabilityCalibrator:
    """Wrapper for temperature scaling and isotonic regression calibrators."""

    def __init__(self, method: str = "temperature_scaling", temperature: float = 1.0):
        self.method = method
        self.temperature = max(1e-4, float(temperature))
        self.is_fitted = False
        self.isotonic_model = None

    def fit_validation(self, scores: List[float], labels: List[int]) -> "ReliabilityCalibrator":
        """Fits calibration parameters strictly on validation partition."""
        scores_arr = np.array(scores, dtype=float)
        labels_arr = np.array(labels, dtype=int)

        if self.method == "temperature_scaling":
            # Simple grid search or mean matching for temperature
            best_temp = 1.0
            best_nll = float("inf")
            for t in np.linspace(0.5, 3.0, 51):
                eps = 1e-6
                clamped = np.clip(scores_arr, eps, 1.0 - eps)
                logits = np.log(clamped / (1.0 - clamped))
                scaled = 1.0 / (1.0 + np.exp(-logits / t))
                scaled = np.clip(scaled, eps, 1.0 - eps)
                nll = -np.mean(labels_arr * np.log(scaled) + (1 - labels_arr) * np.log(1 - scaled))
                if nll < best_nll:
                    best_nll = nll
                    best_temp = t
            self.temperature = float(best_temp)

        elif self.method == "isotonic":
            from sklearn.isotonic import IsotonicRegression
            self.isotonic_model = IsotonicRegression(out_of_bounds="clip", y_min=0.0, y_max=1.0)
            self.isotonic_model.fit(scores_arr, labels_arr)

        self.is_fitted = True
        return self

    def calibrate(self, score: float) -> float:
        if not self.is_fitted and self.isotonic_model is None:
            # Return scaled with current temp
            eps = 1e-6
            clamped = max(eps, min(1.0 - eps, score))
            import math
            logit = math.log(clamped / (1.0 - clamped))
            return 1.0 / (1.0 + math.exp(-logit / self.temperature))

        if self.isotonic_model is not None:
            return float(self.isotonic_model.predict([score])[0])

        import math
        eps = 1e-6
        clamped = max(eps, min(1.0 - eps, score))
        logit = math.log(clamped / (1.0 - clamped))
        return 1.0 / (1.0 + math.exp(-logit / self.temperature))
