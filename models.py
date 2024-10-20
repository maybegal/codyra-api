from pydantic import BaseModel, Field
from typing import Optional


class Challenge(BaseModel):
    programming_language: str
    question: str
    answer: str
    notes: Optional[str] = ""


class FeedbackResponse(BaseModel):
    grade: int
    content: str
