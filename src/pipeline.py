from typing import List
from src.fetchers.base import DataFetcher
from src.transformers.base import DataTransformer
from src.loaders.base import ModelLoader
from src.models import Review, Sentiment

class Pipeline:
    def __init__(self, fetcher: DataFetcher, transformer: DataTransformer, loader: ModelLoader):
        self.fetcher = fetcher
        self.transformer = transformer
        self.loader = loader

    def run(self) -> List[Sentiment]:
        data = self.fetcher.fetch_data()
        transformed_data,_ = self.transformer.transform(data)
        predictions = self.loader.predict(transformed_data)
        print("predictions : ",predictions)
        print("pipeline completed")
        return predictions
