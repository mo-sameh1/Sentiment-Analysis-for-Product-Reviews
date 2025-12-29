from abc import ABC, abstractmethod
from typing import Any, List
from src.models import Sentiment

class ModelLoader(ABC):
    @abstractmethod
    def load(self):
        """Loads the model from disk or memory."""
        pass

    @abstractmethod
    def predict(self, data: Any) -> List[Sentiment]:
        """Makes predictions on the transformed data."""
        pass
