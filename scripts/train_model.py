"""
Training script for the sentiment analysis model.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.config import (
    MONGO_URI,
    DB_NAME,
    COLLECTION_NAME,
    MODEL_PATH,
    VECTORIZER_PATH,
    DATA_DIR,
    DEFAULT_FETCH_LIMIT,
    TRAIN_TEST_SPLIT_RATIO,
    RANDOM_STATE,
    LOGISTIC_REGRESSION_MAX_ITER,
)
from src.fetchers.mongo_fetcher import MongoFetcher
from src.transformers.text_sentiment_transformer import TextSentimentTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib


def train():
    print("=" * 50)
    print("Starting Training Pipeline")
    print("=" * 50)
    
    print(f"\n[1/4] Connecting to MongoDB...")
    print(f"      URI: {MONGO_URI}")
    print(f"      Database: {DB_NAME}")
    print(f"      Collection: {COLLECTION_NAME}")
    
    try:
        fetcher = MongoFetcher(MONGO_URI, DB_NAME, COLLECTION_NAME)
        print("\n[2/4] Fetching data...")
        data = fetcher.fetch_data(limit=DEFAULT_FETCH_LIMIT)
    except Exception as e:
        print(f"Error fetching data: {e}")
        return False

    if not data:
        print("No data found in MongoDB.")
        print("Please run: python scripts/download_data.py")
        print("Then run: python scripts/initialize_db.py")
        return False
    
    print(f"      Fetched {len(data)} reviews")
    
    print("\n[3/4] Transforming data...")
    transformer = TextSentimentTransformer()
    
    try:
        X, y = transformer.transform(data)
        print(f"      Feature matrix shape: {X.shape}")
        print(f"      Positive samples: {sum(y == 1)}")
        print(f"      Negative samples: {sum(y == 0)}")
    except Exception as e:
        print(f"Error during transformation: {e}")
        return False
    
    DATA_DIR.mkdir(exist_ok=True)
    transformer.save_vectorizer(str(VECTORIZER_PATH))
    
    print("\n[4/4] Training model...")
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TRAIN_TEST_SPLIT_RATIO, random_state=RANDOM_STATE, stratify=y
    )
    
    model = LogisticRegression(max_iter=LOGISTIC_REGRESSION_MAX_ITER, random_state=RANDOM_STATE)
    model.fit(X_train, y_train)
    
    train_preds = model.predict(X_train)
    test_preds = model.predict(X_test)
    
    train_acc = accuracy_score(y_train, train_preds)
    test_acc = accuracy_score(y_test, test_preds)
    
    print(f"\n      Training Accuracy: {train_acc:.4f}")
    print(f"      Test Accuracy: {test_acc:.4f}")
    
    print("\n      Classification Report (Test Set):")
    print(classification_report(y_test, test_preds, target_names=["Negative", "Positive"]))
    
    joblib.dump(model, str(MODEL_PATH))
    print(f"\n[OK] Model saved to {MODEL_PATH}")
    
    print("\n" + "=" * 50)
    print("Training Complete!")
    print("=" * 50)
    return True


if __name__ == "__main__":
    success = train()
    sys.exit(0 if success else 1)
