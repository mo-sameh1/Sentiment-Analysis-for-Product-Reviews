from abc import ABC
from typing import Any, List
import pandas as pd
import joblib
from src.models import Sentiment
from src.loaders.base import ModelLoader
from sklearn.base import BaseEstimator


class SKLearnSentimentLoader(ModelLoader):
    """
    Loader for a pre-trained scikit-learn sentiment model.
    Returns predictions as List[Sentiment] on a random 100 samples.
    """

    def __init__(self, model_path: str):
        self.model_path = model_path
        self.model: BaseEstimator = None

    def load(self):
        """Load the pre-trained model."""
        self.model = joblib.load(self.model_path)
        print(f"✅ Model loaded from '{self.model_path}'")

    def predict(self, data: Any) -> List[Sentiment]:
        """
        Predict sentiment for a random 100 rows and return List[Sentiment].
        Uses 0.5 threshold to classify positive/negative.

        Parameters:
            data: Transformed data (TF-IDF matrix or DataFrame)

        Returns:
            List[Sentiment]: Predictions with label and confidence
        """
        self.load()
        if self.model is None:
            raise ValueError("Model not loaded. Call `load()` first.")

        # Convert sparse matrix to DataFrame for sampling
        if not isinstance(data, pd.DataFrame):
            df = pd.DataFrame(data.toarray())
        else:
            df = data

        # Randomly sample 100 rows
        sample_df = df.sample(n=100, random_state=42)

        # Predict probabilities or raw outputs
        if hasattr(self.model, "predict_proba"):
            probs = self.model.predict_proba(sample_df)[:, 1]  # Probability of positive class
        else:
            # If the model predicts a float between 0 and 1
            probs = self.model.predict(sample_df)

        results: List[Sentiment] = []
        for p in probs:
            if p >= 0.5:
                label = "positive"
                confidence = float(p)
            else:
                label = "negative"
                confidence = float(1 - p)

            results.append(Sentiment(label=label, confidence=confidence))

        return results
