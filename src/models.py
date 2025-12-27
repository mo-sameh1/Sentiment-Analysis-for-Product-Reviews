from pydantic import BaseModel, Field
from typing import Optional

class Review(BaseModel):
    Id: str
    ProductId: str
    UserId: str
    ProfileName: Optional[str] = None
    HelpfulnessNumerator: Optional[int] = None
    HelpfulnessDenominator: Optional[int] = None
    Score: int = Field(..., ge=1, le=5)
    Time: Optional[int] = None
    Summary: Optional[str] = None
    Text: str

class Sentiment(BaseModel):
    label: str
    confidence: float
