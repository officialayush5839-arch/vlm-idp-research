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


import datetime
from pathlib import Path
import joblib

FEATURE_NAMES: List[str] = [
    "blur", "noise", "skew", "glare", "contrast",
    "resolution", "compression", "illumination", "occlusion", "perspective"
]


class LearnedQualityRouter:
    """
    Lightweight ML-based model router trained on train/val performance outcomes.
    Enforces deterministic joblib serialization and zero-leakage training.
    """

    def __init__(self, classifier_type: str = "logistic", random_state: int = 42):
        self.classifier_type = classifier_type.lower()
        self.random_state = random_state
        self.is_fitted = False
        self.feature_names = list(FEATURE_NAMES)
        self.metadata: Dict[str, Any] = {}
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
        metadata: Optional[Dict[str, Any]] = None,
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
        self.metadata = metadata or {
            "partition": partition,
            "fitted_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "n_samples": int(len(X_arr)),
            "n_classes": int(len(np.unique(y_arr))),
            "classes": [str(c) for c in np.unique(y_arr)],
        }
        return self

    def save(self, path: Union[str, Path]) -> str:
        """
        Serializes fitted model, feature ordering, and provenance metadata to disk using joblib.
        """
        if not self.is_fitted:
            raise ValueError("Cannot serialize an unfitted LearnedQualityRouter.")

        out_path = Path(path)
        out_path.parent.mkdir(parents=True, exist_ok=True)

        payload = {
            "model": self.model,
            "classifier_type": self.classifier_type,
            "random_state": self.random_state,
            "is_fitted": self.is_fitted,
            "feature_names": self.feature_names,
            "metadata": self.metadata,
        }
        joblib.dump(payload, str(out_path))
        return str(out_path)

    def load(self, path: Union[str, Path]) -> LearnedQualityRouter:
        """
        Loads serialized model, feature ordering, and metadata from disk.
        """
        in_path = Path(path)
        if not in_path.exists():
            raise FileNotFoundError(f"Serialized learned router file not found at: {in_path}")

        payload = joblib.load(str(in_path))
        self.model = payload["model"]
        self.classifier_type = payload["classifier_type"]
        self.random_state = payload["random_state"]
        self.is_fitted = payload["is_fitted"]
        self.feature_names = payload.get("feature_names", list(FEATURE_NAMES))
        self.metadata = payload.get("metadata", {})
        return self

    @classmethod
    def from_file(cls, path: Union[str, Path]) -> LearnedQualityRouter:
        """
        Factory to instantiate and load a LearnedQualityRouter from disk.
        """
        router = cls()
        router.load(path)
        return router

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
