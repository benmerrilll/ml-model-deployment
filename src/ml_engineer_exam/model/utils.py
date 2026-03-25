from pathlib import Path
from typing import Literal

import joblib
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

BASE_MODELS = {
    "linear": LinearRegression(),
    "ridge": Ridge(alpha=1.0),
    "random_forest": RandomForestRegressor(n_estimators=100, random_state=42),
}


class HousingModel:
    def __init__(self, model_type: Literal["linear", "ridge", "random_forest"] = "linear"):
        self.model_type = model_type
        self.model = BASE_MODELS[model_type]

    def train(self, X_train, y_train):
        """Train the model."""
        self.model.fit(X_train, y_train)
        return self

    def predict(self, X):
        """Make predictions."""
        return self.model.predict(X)

    def evaluate(self, X_test, y_test):
        """Evaluate model performance."""
        y_pred = self.predict(X_test)
        metrics = {
            "mse": mean_squared_error(y_test, y_pred),
            "rmse": np.sqrt(mean_squared_error(y_test, y_pred)),
            "mae": mean_absolute_error(y_test, y_pred),
            "r2": r2_score(y_test, y_pred),
        }
        return metrics

    def save(self, path: Path):
        """Save model to disk."""
        path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self.model, path)

    @classmethod
    def load(cls, path: Path):
        """Load model from disk."""
        instance = cls()
        instance.model = joblib.load(path)
        return instance
