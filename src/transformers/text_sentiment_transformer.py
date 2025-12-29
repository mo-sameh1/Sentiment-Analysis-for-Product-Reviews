from abc import ABC, abstractmethod
from typing import Any, List, Tuple, Union
import pandas as pd
import re
import nltk

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from src.models import Review
from src.transformers.base import DataTransformer

# Download required NLTK resources
nltk.download("stopwords")
nltk.download("wordnet")
nltk.download("omw-1.4")



class TextSentimentTransformer(DataTransformer):
    """
    Transformer for binary sentiment analysis on Amazon reviews.
    Can accept a List[Review] or a pandas DataFrame.
    Converts raw reviews into TF-IDF features and sentiment labels.
    """

    def __init__(self, max_features: int = 10000):
        self.stop_words = set(stopwords.words("english"))
        self.lemmatizer = WordNetLemmatizer()
        self.vectorizer = TfidfVectorizer(
            max_features=max_features,
            ngram_range=(1, 2)
        )

    def _clean_text(self, text: str) -> str:
        """Cleans and normalizes review text."""
        if not isinstance(text, str):
            return ""  # Treat NaN or non-strings as empty

        text = re.sub(r"<.*?>", "", text)
        text = re.sub(r"[^a-zA-Z]", " ", text)
        text = text.lower()
        words = text.split()
        words = [
            self.lemmatizer.lemmatize(w, pos="v")
            for w in words
            if w not in self.stop_words
        ]
        return " ".join(words)

    def transform(
        self, data: List[Review]
    ) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Parameters:
            data (List[Review] or pd.DataFrame): Raw reviews

        Returns:
            X: TF-IDF feature matrix
            y: Binary sentiment labels
        """

        # Convert List[Review] to DataFrame if necessary
        if isinstance(data, list):
            data = pd.DataFrame([r.__dict__ for r in data])

        # Drop neutral reviews
        data = data[data["Score"] != 3].copy()

        # Create binary sentiment label
        data["Sentiment"] = data["Score"].apply(lambda x: 1 if x >= 4 else 0)

        # Balance classes
        min_size = data["Sentiment"].value_counts().min()
        pos = data[data["Sentiment"] == 1].sample(min_size, random_state=42)
        neg = data[data["Sentiment"] == 0].sample(min_size, random_state=42)
        data = pd.concat([pos, neg]).sample(frac=1, random_state=42)

        # Combine text fields
        data["Combined_Content"] = data["Summary"] + " " + data["Text"]

        # Clean text
        data["Cleaned_Content"] = data["Combined_Content"].apply(self._clean_text)

        # Vectorize text
        X = self.vectorizer.fit_transform(data["Cleaned_Content"])
        y = data["Sentiment"]

        return X, y
