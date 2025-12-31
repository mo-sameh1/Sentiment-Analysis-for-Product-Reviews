"""
Prediction service for sentiment analysis inference.
Uses the pipeline's transformer for text preprocessing.
"""

from typing import Optional, List
from dataclasses import dataclass
from src.config import (
    MODEL_PATH,
    VECTORIZER_PATH,
    SENTIMENT_POSITIVE,
    SENTIMENT_NEGATIVE,
    SENTIMENT_ERROR,
)
from src.transformers.text_sentiment_transformer import TextSentimentTransformer
from src.loaders.sentiment_loader import SKLearnSentimentLoader


@dataclass
class PredictionResult:
    text: str
    label: str
    confidence: float
    
    @property
    def is_positive(self) -> bool:
        return self.label == SENTIMENT_POSITIVE
    
    @property
    def confidence_percent(self) -> str:
        return f"{self.confidence:.1%}"


class PredictionService:
    _instance: Optional["PredictionService"] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self._transformer: Optional[TextSentimentTransformer] = None
        self._loader: Optional[SKLearnSentimentLoader] = None
    
    @property
    def transformer(self) -> TextSentimentTransformer:
        if self._transformer is None:
            self._transformer = TextSentimentTransformer()
            if VECTORIZER_PATH.exists():
                self._transformer.load_vectorizer(str(VECTORIZER_PATH))
        return self._transformer
    
    @property
    def loader(self) -> SKLearnSentimentLoader:
        if self._loader is None:
            self._loader = SKLearnSentimentLoader(str(MODEL_PATH))
        return self._loader
    
    def clean_text(self, text: str) -> str:
        return self.transformer._clean_text(text)
    
    def is_model_available(self) -> bool:
        return MODEL_PATH.exists() and VECTORIZER_PATH.exists()
    
    def get_model_info(self) -> dict:
        info = {
            "model_exists": MODEL_PATH.exists(),
            "vectorizer_exists": VECTORIZER_PATH.exists(),
            "model_path": str(MODEL_PATH),
            "vectorizer_path": str(VECTORIZER_PATH)
        }
        
        if info["model_exists"]:
            info["model_size"] = f"{MODEL_PATH.stat().st_size / 1024:.1f} KB"
        if info["vectorizer_exists"]:
            info["vectorizer_size"] = f"{VECTORIZER_PATH.stat().st_size / 1024:.1f} KB"
            
        return info
    
    def predict_single(self, text: str) -> PredictionResult:
        if not self.is_model_available():
            raise FileNotFoundError("Model not trained. Please run the training pipeline first.")
        
        features = self.transformer.transform_inference(text)
        result = self.loader.predict_single(features)
        
        return PredictionResult(
            text=text,
            label=result.label,
            confidence=result.confidence
        )
    
    def predict_batch(self, texts: List[str]) -> List[PredictionResult]:
        results = []
        for text in texts:
            try:
                result = self.predict_single(text)
                results.append(result)
            except Exception:
                results.append(PredictionResult(
                    text=text,
                    label=SENTIMENT_ERROR,
                    confidence=0.0
                ))
        return results
    
    def get_batch_summary(self, results: List[PredictionResult]) -> dict:
        valid_results = [r for r in results if r.label != SENTIMENT_ERROR]
        if not valid_results:
            return {"total": len(results), "positive": 0, "negative": 0, "avg_confidence": 0}
        
        positive = sum(1 for r in valid_results if r.is_positive)
        negative = len(valid_results) - positive
        avg_conf = sum(r.confidence for r in valid_results) / len(valid_results)
        
        return {
            "total": len(results),
            "valid": len(valid_results),
            "positive": positive,
            "negative": negative,
            "positive_ratio": positive / len(valid_results) if valid_results else 0,
            "avg_confidence": avg_conf
        }
