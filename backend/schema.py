from pydantic import BaseModel
from datetime import date, time


class ShortPredictionRequest(BaseModel):
    city: str


class FuturePredictionRequest(BaseModel):
    city: str
    date: date
    hour: int