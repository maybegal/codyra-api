from pydantic import BaseModel, Field
from typing import Optional, Union


class Challenge(BaseModel):
    programming_language: str
    question: str
    answer: str
    notes: Optional[str] = ""


class FeedbackResponse(BaseModel):
    feedback_type: str
    content: Union[str, int]