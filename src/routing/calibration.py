"""
Post-Hoc Calibration Engine for Multi-Signal Uncertainty.
Fitted strictly on validation partitions to produce calibrated confidence estimates.
Strictly prohibits test partition calibration.
"""

from __future__ import annotations

from typing import Any, List, Optional, Union
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.isotonic import IsotonicRegression


class PostHocCalibrator:
    """
    Fits calibration models (Platt Logistic or Isotonic) mapping multi-signal
    uncertainty vectors to true empirical confidence.
    """

    def __init__(self, method: str = "logistic"):
        self.method = method.lower()
        self.is_fitted = False
        if self.method == "logistic":
            self.model = LogisticRegression(C=1.0, max_iter=1000)
        elif self.method == "isotonic":
            self.model = IsotonicRegression(out_of_bounds="clip", increasing=True)
        else:
            raise ValueError(f"Unsupported calibration method: {method}")

    def fit(
        self,
        X: Union[np.ndarray, List[List[float]]],
        y: Union[np.ndarray, List[int]],
        partition: str = "val",
    ) -> PostHocCalibrator:
        """
        Fit the calibrator on validation or training data.
        Raises ValueError if partition is 'test' to guarantee zero test leakage.
        """
        if partition.lower() == "test":
            raise ValueError(
                "Post-hoc calibration on the test partition is strictly forbidden by the research protocol."
            )

        X_arr = np.asarray(X, dtype=float)
        y_arr = np.asarray(y, dtype=int)

        if self.method == "logistic":
            # Multi-dimensional feature vector
            if X_arr.ndim == 1:
                X_arr = X_arr.reshape(-1, 1)
            self.model.fit(X_arr, y_arr)
        elif self.method == "isotonic":
            # 1D summary projection
            if X_arr.ndim == 2:
                X_scalar = X_arr.mean(axis=1)
            else:
                X_scalar = X_arr
            self.model.fit(X_scalar, y_arr)

        self.is_fitted = True
        return self

    def calibrate(self, vector: Union[List[float], np.ndarray]) -> float:
        """
        Maps a 6-signal uncertainty vector to a single calibrated confidence in [0, 1].
        """
        if not self.is_fitted:
            # Uncalibrated linear average fallback
            return float(np.mean(vector))

        vec_arr = np.asarray(vector, dtype=float)
        if self.method == "logistic":
            if vec_arr.ndim == 1:
                vec_arr = vec_arr.reshape(1, -1)
            # Predict class 1 probability
            prob = self.model.predict_proba(vec_arr)[0, 1]
            return float(max(0.0, min(1.0, prob)))
        elif self.method == "isotonic":
            scalar = float(np.mean(vec_arr))
            prob = self.model.predict([scalar])[0]
            return float(max(0.0, min(1.0, prob)))
        return float(np.mean(vec_arr))

    @staticmethod
    def get_status(confidence: float, tau_accept: float = 0.75, tau_review: float = 0.40) -> str:
        """
        Maps confidence to tripartite decision status per uncertainty protocol.
        """
        if confidence >= tau_accept:
            return "VERIFIED"
        elif confidence >= tau_review:
            return "UNCERTAIN"
        else:
            return "REVIEW_REQUIRED"

    @staticmethod
    def compute_ece(probs: np.ndarray, y_true: np.ndarray, num_bins: int = 10) -> float:
        """
        Expected Calibration Error (ECE) across equal-width confidence bins.
        """
        probs = np.asarray(probs)
        y_true = np.asarray(y_true)
        bin_limits = np.linspace(0.0, 1.0, num_bins + 1)
        ece = 0.0
        n_samples = len(probs)
        if n_samples == 0:
            return 0.0

        for i in range(num_bins):
            bin_lower = bin_limits[i]
            bin_upper = bin_limits[i + 1]
            if i == num_bins - 1:
                in_bin = (probs >= bin_lower) & (probs <= bin_upper)
            else:
                in_bin = (probs >= bin_lower) & (probs < bin_upper)

            prop_in_bin = np.mean(in_bin)
            if prop_in_bin > 0:
                acc_in_bin = np.mean(y_true[in_bin])
                avg_conf_in_bin = np.mean(probs[in_bin])
                ece += np.abs(avg_conf_in_bin - acc_in_bin) * prop_in_bin

        return float(ece)

    @staticmethod
    def compute_brier_score(probs: np.ndarray, y_true: np.ndarray) -> float:
        """
        Mean squared difference between predicted probabilities and binary outcomes.
        """
        probs = np.asarray(probs)
        y_true = np.asarray(y_true)
        if len(probs) == 0:
            return 0.0
        return float(np.mean((probs - y_true) ** 2))
