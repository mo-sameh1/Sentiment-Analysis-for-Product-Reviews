"""
Database initialization script - loads CSV data into MongoDB.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd
from pymongo import MongoClient
from src.config import (
    MONGO_URI,
    DB_NAME,
    COLLECTION_NAME,
    REVIEWS_CSV_PATH,
)


def initialize_db():
    print(f"Connecting to MongoDB at {MONGO_URI}...")
    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]

        if collection.count_documents({}) > 0:
            print("Database already contains data. Skipping initialization.")
            return

        if not REVIEWS_CSV_PATH.exists():
            print(f"Data file not found at {REVIEWS_CSV_PATH}.")
            print("Attempting to download dataset...")
            try:
                from scripts.download_data import download_dataset
                download_dataset()
            except ImportError:
                print("Could not import download_data script.")

        if not REVIEWS_CSV_PATH.exists():
            print("Data file still not found. Exiting.")
            return

        print(f"Reading data from {REVIEWS_CSV_PATH}...")
        df = pd.read_csv(REVIEWS_CSV_PATH)
        
        records = df.to_dict("records")
        
        print(f"Inserting {len(records)} records into MongoDB...")
        collection.insert_many(records)
        print("Successfully inserted data.")

    except Exception as e:
        print(f"Error initializing database: {e}")


if __name__ == "__main__":
    initialize_db()
