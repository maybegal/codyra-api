from pydantic import BaseModel
from typing import Optional


class Challenge(BaseModel):
    programming_language: str
    question: str
    answer: str
    notes: Optional[str] = ""


class Feedback(BaseModel):
    grade: int
    overview: str
    strategy: str
    solution: str
    code_solution: str
    growth_opportunities: str
