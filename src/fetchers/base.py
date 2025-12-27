from abc import ABC, abstractmethod
from typing import List
from src.models import Review

class DataFetcher(ABC):
    @abstractmethod
    def fetch_data(self) -> List[Review]:
        """Fetches data from the source and returns a list of Review objects."""
        pass
