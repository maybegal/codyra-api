"""
This module defines the data models for challenges and feedback using Pydantic.
"""

from pydantic import BaseModel
from typing import Optional


# Represents a programming challenge with its details.
class Challenge(BaseModel):
    """
    Represents a programming challenge.
    """

    programming_language: str
    question: str
    answer: str
    notes: Optional[str] = ""


# Represents feedback for a challenge, including grade and various comments.
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
