import os
import pandas as pd
from pymongo import MongoClient
from typing import List
import sys

# Configuration
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "amazon_reviews")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "reviews")
DATA_FILE = os.path.join("data", "Reviews.csv")
SAMPLE_SIZE = 10000  # Limit initial load to 10k rows for speed

def initialize_db():
    print(f"Connecting to MongoDB at {MONGO_URI}...")
    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]

        # Check if data exists
        if collection.count_documents({}) > 0:
            print("Database already contains data. Skipping initialization.")
            return

        if not os.path.exists(DATA_FILE):
            print(f"Data file not found at {DATA_FILE}.")
            print("Attempting to download dataset...")
            try:
                # Try importing from scripts module
                from scripts.download_data import download_dataset
                download_dataset()
            except ImportError:
                # Handle case where script is run from root
                sys.path.append(os.getcwd())
                try:
                    from scripts.download_data import download_dataset
                    download_dataset()
                except ImportError:
                     print("Could not import download_data script.")

        if not os.path.exists(DATA_FILE):
             print("Data file still not found. Exiting.")
             return

        print(f"Reading data from {DATA_FILE}...")
        # Read CSV
        df = pd.read_csv(DATA_FILE)
        
        # Take a sample if dataset is huge
        # if len(df) > SAMPLE_SIZE:
        #     print(f"Dataset is large ({len(df)} rows). Sampling {SAMPLE_SIZE} rows for initial load.")
        #     df = df.head(SAMPLE_SIZE)
        
        # Convert to dictionary records
        records = df.to_dict("records")
        
        # Insert into Mongo
        print(f"Inserting {len(records)} records into MongoDB...")
        collection.insert_many(records)
        print("Successfully inserted data.")

    except Exception as e:
        print(f"Error initializing database: {e}")

if __name__ == "__main__":
    initialize_db()
