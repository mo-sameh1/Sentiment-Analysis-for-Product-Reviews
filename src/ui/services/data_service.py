"""
Data service for fetching and caching data from MongoDB.
"""

from typing import List, Optional
import pandas as pd
from src.config import (
    MONGO_URI,
    DB_NAME,
    COLLECTION_NAME,
    MONGO_CONNECTION_TIMEOUT_MS,
)


class DataService:
    _instance: Optional["DataService"] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.mongo_uri = MONGO_URI
        self.db_name = DB_NAME
        self.collection_name = COLLECTION_NAME
        self._cached_data: Optional[pd.DataFrame] = None
        self._cache_limit: int = 0
    
    def get_connection_info(self) -> dict:
        return {
            "uri": self.mongo_uri,
            "database": self.db_name,
            "collection": self.collection_name
        }
    
    def fetch_reviews(self, limit: int = 1000, force_refresh: bool = False) -> pd.DataFrame:
        if self._cached_data is not None and self._cache_limit >= limit and not force_refresh:
            return self._cached_data.head(limit)
        
        try:
            from src.fetchers.mongo_fetcher import MongoFetcher
            fetcher = MongoFetcher(self.mongo_uri, self.db_name, self.collection_name)
            reviews = fetcher.fetch_data(limit=limit)
            
            if not reviews:
                return pd.DataFrame()
            
            data = [r.model_dump() for r in reviews]
            self._cached_data = pd.DataFrame(data)
            self._cache_limit = limit
            return self._cached_data
            
        except Exception as e:
            raise ConnectionError(f"Failed to connect to MongoDB: {e}")
    
    def check_connection(self) -> bool:
        try:
            from pymongo import MongoClient
            client = MongoClient(self.mongo_uri, serverSelectionTimeoutMS=MONGO_CONNECTION_TIMEOUT_MS)
            client.server_info()
            return True
        except Exception:
            return False
    
    def get_collection_stats(self) -> dict:
        try:
            from pymongo import MongoClient
            client = MongoClient(self.mongo_uri)
            db = client[self.db_name]
            collection = db[self.collection_name]
            count = collection.count_documents({})
            return {"total_documents": count, "status": "connected"}
        except Exception as e:
            return {"total_documents": 0, "status": f"error: {e}"}
