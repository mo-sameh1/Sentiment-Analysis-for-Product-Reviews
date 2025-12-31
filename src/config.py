"""
Application-wide constants and configuration.

This module centralizes all configuration values, paths, and string constants
used throughout the application to avoid hardcoding values in multiple places.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


# =============================================================================
# Path Constants
# =============================================================================

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
SRC_DIR = PROJECT_ROOT / "src"

# Model and Vectorizer Paths
MODEL_PATH = DATA_DIR / "model.pkl"
VECTORIZER_PATH = DATA_DIR / "vectorizer.pkl"
REVIEWS_CSV_PATH = DATA_DIR / "Reviews.csv"


# =============================================================================
# MongoDB Configuration
# =============================================================================

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "sentiment_db")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "reviews")

MONGO_CONNECTION_TIMEOUT_MS = 3000


# =============================================================================
# Kaggle Configuration
# =============================================================================

KAGGLE_DATASET_NAME = "snap/amazon-fine-food-reviews"
KAGGLE_FILE_NAME = "Reviews.csv"


# =============================================================================
# Model Training Configuration
# =============================================================================

DEFAULT_FETCH_LIMIT = 5000
TFIDF_MAX_FEATURES = 10000
TFIDF_NGRAM_RANGE = (1, 2)
TRAIN_TEST_SPLIT_RATIO = 0.2
RANDOM_STATE = 42
LOGISTIC_REGRESSION_MAX_ITER = 1000


# =============================================================================
# UI Configuration
# =============================================================================

APP_TITLE = "Sentiment Analysis Dashboard"
APP_ICON = "📊"
APP_VERSION = "1.0.0"

PAGE_HOME = "Home"
PAGE_DATA_EXPLORER = "Data Explorer"
PAGE_SINGLE_PREDICTION = "Single Prediction"
PAGE_BATCH_ANALYSIS = "Batch Analysis"
PAGE_PIPELINE_STATUS = "Pipeline Status"

PAGES = [
    ("🏠", PAGE_HOME),
    ("📊", PAGE_DATA_EXPLORER),
    ("🔮", PAGE_SINGLE_PREDICTION),
    ("📋", PAGE_BATCH_ANALYSIS),
    ("⚙️", PAGE_PIPELINE_STATUS),
]


# =============================================================================
# Sentiment Labels
# =============================================================================

SENTIMENT_POSITIVE = "positive"
SENTIMENT_NEGATIVE = "negative"
SENTIMENT_NEUTRAL = "neutral"
SENTIMENT_ERROR = "error"

CONFIDENCE_HIGH_THRESHOLD = 0.8
CONFIDENCE_MEDIUM_THRESHOLD = 0.6


# =============================================================================
# Sample Reviews for Demo
# =============================================================================

SAMPLE_REVIEWS = {
    "Positive Example": (
        "This product is absolutely amazing! I've been using it for a month now "
        "and it exceeded all my expectations. The quality is outstanding and the "
        "price is very reasonable. Highly recommend to everyone!"
    ),
    "Negative Example": (
        "Terrible product. Broke after two days of use. The quality is extremely "
        "poor and it doesn't work as advertised. Complete waste of money. "
        "Would not recommend to anyone."
    ),
    "Neutral Example": (
        "The product is okay. Nothing special but it does what it's supposed to do. "
        "Average quality for the price. Not great, not terrible."
    ),
    "Mixed Example": (
        "The product quality is good but the shipping was terrible. It arrived late "
        "and the packaging was damaged. Customer service was helpful though."
    ),
}


# =============================================================================
# Status Messages
# =============================================================================

MSG_DB_CONNECTED = "✅ Connected"
MSG_DB_DISCONNECTED = "❌ Disconnected"
MSG_MODEL_READY = "✅ Model Ready"
MSG_MODEL_NOT_TRAINED = "⚠️ Model Not Trained"

MSG_NO_DATA_FOUND = "No data found in the database. Please run the data initialization script."
MSG_MODEL_NOT_AVAILABLE = "Model not available. Please train the model first."
