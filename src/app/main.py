# import streamlit as st
import os
from src.fetchers.mongo_fetcher import MongoFetcher
from src.fetchers.csv_fetcher import CSVFetcher
from src.models import Review
from src.pipeline import Pipeline
from src.transformers.text_sentiment_transformer import TextSentimentTransformer
from src.loaders.sentiment_loader import SKLearnSentimentLoader

# Configuration








file_path="src/fetchers/data.csv"
pipeline = Pipeline(CSVFetcher(file_path), TextSentimentTransformer(), SKLearnSentimentLoader("src/loaders/best_sentiment_model.pkl"))

pipeline.run()













exit()
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "amazon_reviews")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "reviews")

st.title("Amazon Fine Food Reviews Sentiment Analysis")

@st.cache_resource
def get_fetcher(type: str):
    if type == "csv":
        return CSVFetcher(file_path)
    else:
        return MongoFetcher(MONGO_URI, DB_NAME, COLLECTION_NAME)
    

fetcher = get_fetcher()

st.header("Data Preview")
try:
    reviews = fetcher.fetch_data(limit=10)
    if reviews:
        st.write(f"Fetched {len(reviews)} reviews from MongoDB.")
        for review in reviews:
            with st.expander(f"Review {review.Id} - Score: {review.Score}"):
                st.write(f"**Product:** {review.ProductId}")
                st.write(f"**User:** {review.UserId}")
                st.write(f"**Summary:** {review.Summary}")
                st.write(f"**Text:** {review.Text}")
    else:
        st.warning("No reviews found in the database. Please run the initialization script.")
except Exception as e:
    st.error(f"Error connecting to MongoDB: {e}")

st.header("Pipeline Execution")
st.info("Pipeline implementation pending model training integration.")
