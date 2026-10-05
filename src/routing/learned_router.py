"""
Lightweight Learned Router for Phase 5.
Trains a classifier (Logistic Regression or Random Forest) to map quality features
to model selection based strictly on training partition model outcomes.
Enforces zero test leakage.
"""

from __future__ import annotations

from typing import Any, List, Optional, Tuple, Union
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier


class LearnedQualityRouter:
    """
    Lightweight ML-based model router trained on train/val performance outcomes.
    """

    def __init__(self, classifier_type: str = "logistic", random_state: int = 42):
        self.classifier_type = classifier_type.lower()
        self.random_state = random_state
        self.is_fitted = False
        if self.classifier_type == "logistic":
            self.model = LogisticRegression(C=1.0, max_iter=1000, random_state=random_state)
        elif self.classifier_type in ["rf", "random_forest"]:
            self.model = RandomForestClassifier(n_estimators=50, max_depth=5, random_state=random_state)
        else:
            raise ValueError(f"Unsupported classifier type: {classifier_type}")

    def fit(
        self,
        X: Union[np.ndarray, List[List[float]]],
        y: Union[np.ndarray, List[str]],
        partition: str = "train",
    ) -> LearnedQualityRouter:
        """
        Fit the router on training or validation samples.
        Strictly forbids fitting on 'test'.
        """
        if partition.lower() == "test":
            raise ValueError("Fitting learned router on the test partition is strictly forbidden.")

        X_arr = np.asarray(X, dtype=float)
        y_arr = np.asarray(y, dtype=str)

        self.model.fit(X_arr, y_arr)
        self.is_fitted = True
        return self

    def predict(self, feature_vector: Union[List[float], np.ndarray]) -> Tuple[str, str, float]:
        """
        Predict preferred model for an unseen sample.
        Returns: (selected_model, decision_reason, confidence)
        """
        if not self.is_fitted:
            return "B2", "Learned router uninitialized; defaulting to robust fixed baseline B2.", 0.50

        feat_arr = np.asarray(feature_vector, dtype=float).reshape(1, -1)
        pred_model = str(self.model.predict(feat_arr)[0])

        if hasattr(self.model, "predict_proba"):
            probs = self.model.predict_proba(feat_arr)[0]
            conf = float(np.max(probs))
        else:
            conf = 0.80

        reason = f"Learned classifier ({self.classifier_type}) predicted {pred_model} with probability {conf:.2f}."
        return pred_model, reason, conf
