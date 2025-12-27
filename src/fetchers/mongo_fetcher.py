from typing import List
from pymongo import MongoClient
from src.fetchers.base import DataFetcher
from src.models import Review
import os

class MongoFetcher(DataFetcher):
    def __init__(self, uri: str, db_name: str, collection_name: str):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def fetch_data(self, limit: int = 100) -> List[Review]:
        cursor = self.collection.find().limit(limit)
        reviews = []
        for doc in cursor:
            reviews.append(Review(
                Id=str(doc.get('Id')),
                ProductId=str(doc.get('ProductId')),
                UserId=str(doc.get('UserId')),
                ProfileName=str(doc.get('ProfileName')) if doc.get('ProfileName') else None,
                HelpfulnessNumerator=int(doc.get('HelpfulnessNumerator')) if doc.get('HelpfulnessNumerator') is not None else None,
                HelpfulnessDenominator=int(doc.get('HelpfulnessDenominator')) if doc.get('HelpfulnessDenominator') is not None else None,
                Score=int(doc.get('Score')),
                Time=int(doc.get('Time')) if doc.get('Time') is not None else None,
                Summary=str(doc.get('Summary', '')),
                Text=str(doc.get('Text'))
            ))
        return reviews
