from abc import ABC, abstractmethod
from typing import List, Any
from src.models import Review

class DataTransformer(ABC):
    @abstractmethod
    def transform(self, data: List[Review]) -> Any:
        """Transforms the list of reviews into a format suitable for the model."""
        pass
