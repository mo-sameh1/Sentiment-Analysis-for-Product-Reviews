"""
Inference module for sentiment prediction on new text inputs.
"""

import os
from typing import Optional
from src.transformers.text_sentiment_transformer import TextSentimentTransformer
from src.loaders.sentiment_loader import SKLearnSentimentLoader
from src.models import Sentiment


class SentimentPredictor:
    """Handles sentiment prediction for individual text inputs."""
    
    def __init__(
        self, 
        model_path: str = "data/model.pkl", 
        vectorizer_path: str = "data/vectorizer.pkl"
    ):
        self.model_path = model_path
        self.vectorizer_path = vectorizer_path
        self._transformer: Optional[TextSentimentTransformer] = None
        self._loader: Optional[SKLearnSentimentLoader] = None
        
    @property
    def transformer(self) -> TextSentimentTransformer:
        if self._transformer is None:
            self._transformer = TextSentimentTransformer()
            if os.path.exists(self.vectorizer_path):
                self._transformer.load_vectorizer(self.vectorizer_path)
        return self._transformer
    
    @property
    def loader(self) -> SKLearnSentimentLoader:
        if self._loader is None:
            self._loader = SKLearnSentimentLoader(self.model_path)
        return self._loader

    def predict_single(self, text: str) -> Sentiment:
        """Predict sentiment for a single text input."""
        if not os.path.exists(self.vectorizer_path):
            raise FileNotFoundError(
                f"Vectorizer not found at {self.vectorizer_path}. "
                "Please train the model first."
            )
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(
                f"Model not found at {self.model_path}. "
                "Please train the model first."
            )
             
        features = self.transformer.transform_inference(text)
        return self.loader.predict_single(features)
