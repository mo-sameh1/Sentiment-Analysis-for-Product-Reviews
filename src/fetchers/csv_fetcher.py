from typing import List
import pandas as pd
from src.fetchers.base import DataFetcher
from src.models import Review

class CSVFetcher(DataFetcher):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def fetch_data(self) -> List[Review]:
        df = pd.read_csv(self.file_path)
        # Ensure columns match, simple mapping
        reviews = []
        for _, row in df.iterrows():
            reviews.append(Review(
                Id=str(row.get('Id')),
                ProductId=str(row.get('ProductId')),
                UserId=str(row.get('UserId')),
                ProfileName=str(row.get('ProfileName')) if pd.notna(row.get('ProfileName')) else None,
                HelpfulnessNumerator=int(row.get('HelpfulnessNumerator')) if pd.notna(row.get('HelpfulnessNumerator')) else None,
                HelpfulnessDenominator=int(row.get('HelpfulnessDenominator')) if pd.notna(row.get('HelpfulnessDenominator')) else None,
                Score=int(row.get('Score')),
                Time=int(row.get('Time')) if pd.notna(row.get('Time')) else None,
                Summary=str(row.get('Summary')) if pd.notna(row.get('Summary')) else None,
                Text=str(row.get('Text'))
            ))
        return reviews
