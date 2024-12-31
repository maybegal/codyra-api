"""
This module defines the data models for challenges and feedback using Pydantic.
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Challenge(BaseModel):
    """
    Represents a programming challenge.
    """

    programming_language: str
    question: str
    answer: str
    notes: Optional[str] = ""


class Feedback(BaseModel):
    """
    Represents feedback for a challenge.
    """

    grade: int
    overview: str
    strategy: str
    solution: str
    code_solution: str
    growth_opportunities: str
    model: str = "GPT-4o"
    date: str = datetime.now().strftime("%m/%d/%Y")
    version: str = "1.00"
